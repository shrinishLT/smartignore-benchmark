import json
import os
import logging
import cv2
import numpy as np
from applitools.images import Eyes, Target
import requests
from constants import SMART_IGNORE_STAGE_URL, BASE_DIFF_URL, COMP_DIFF_URL, APPLITOOLS_API_KEY, USERNAME

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Helper function to crop the image to the target size
def crop_to_match(image, target_height, target_width):
    height, width, _ = image.shape
    start_x = (width - target_width) // 2
    start_y = (height - target_height) // 2
    return image[start_y:start_y + target_height, start_x:start_x + target_width]

# Helper function to download an image from a URL
def download_image(url, local_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        raise Exception(f'Failed to download image from {url}')

# Function to process images before comparison
def process_images(base_url, compare_url, i):
    base_image_path = f'./dev/URLs/input/base/base{i}.png'
    compare_image_path = f'./dev/URLs/input/compare/compare{i}.png'
    
    # Download images
    download_image(base_url, base_image_path)
    download_image(compare_url, compare_image_path)
    
    # Load images
    base_image = cv2.imread(base_image_path)
    compare_image = cv2.imread(compare_image_path)

    if base_image is None or compare_image is None:
        raise FileNotFoundError('One or both of the image files were not found or could not be loaded')

    base_height, base_width = base_image.shape[:2]
    compare_height, compare_width = compare_image.shape[:2]

    # Crop images if dimensions do not match
    if base_height != compare_height or base_width != compare_width:
        if base_height > compare_height:
            base_image = crop_to_match(base_image, compare_height, compare_width)
        else:
            compare_image = crop_to_match(compare_image, base_height, base_width)

    # Save the processed images
    processed_base_path = f'./dev/proc_URLs/base/base{i}.png'
    processed_compare_path = f'./dev/proc_URLs/comp/comp{i}.png'
    cv2.imwrite(processed_base_path, base_image)
    cv2.imwrite(processed_compare_path, compare_image)

    return processed_base_path, processed_compare_path

# Make POST request to Applitools:
def applitools_request(basePath, compPath, eyes, index):
    logging.debug(f'Checking base image {index + 1}: {basePath}')
    eyes.check_image(basePath, f'img {index + 1}')
    logging.debug(f'Checking comparison image {index + 1}: {compPath}')
    eyes.check_image(compPath, f'img {index + 1}')

# Main function
def main():
    logging.debug('Initializing Eyes SDK')
    eyes = Eyes()
    eyes.api_key = APPLITOOLS_API_KEY

    logging.debug('Opening JSON file')
    URL_PATH = os.path.join(os.getcwd(), './dev/URLs/urls.json')
    with open(URL_PATH, 'r') as file:
        data = json.load(file)

    logging.debug('Starting URL comparison')
    for i, entry in enumerate(data["input"]):
        base_url = entry["baseURL"]
        compare_url = entry["compareURL"]
        
        logging.debug(f'Opening Eyes session for test {i+1}')
        eyes.open(app_name='Dummy App', test_name=f'Test-diff-{i+1}')
        
        try:
            # Process images to match dimensions
            processed_base_path, processed_compare_path = process_images(base_url, compare_url,i)
            
            # Perform Applitools comparison
            applitools_request(processed_base_path, processed_compare_path, eyes, i)
            
            logging.debug(f'Closing Eyes session for test {i+1}')
            eyes.close(True)
        except Exception as e:
            logging.error(f'Error during comparison for test {i+1}: {e}')
    
    # End the test
    logging.debug('Aborting Eyes session if not closed')
    eyes.abort_if_not_closed()

if __name__ == '__main__':
    main()
