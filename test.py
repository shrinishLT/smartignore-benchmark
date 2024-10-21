import logging
import numpy as np
from applitools.images import Eyes
from constants import  BASE_DIFF_URL, COMP_DIFF_URL, APPLITOOLS_API_KEY

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    logging.debug('Initializing Eyes SDK')
    eyes = Eyes()
    eyes.api_key = APPLITOOLS_API_KEY
    
    try:
        logging.debug(f'Opening Eyes session for test Static')
        eyes.open(app_name='Dummy App', test_name=f'Static-2')
        
        for i  in range(27,32):
            BASE_DIFF_URL = f'./dev/images/input/base/base{i}.png'
            COMP_DIFF_URL = f'./dev/images/input/compare/compare{i}.png'
            logging.debug(f'Checking image {i}: {COMP_DIFF_URL}')
            eyes.check_image(COMP_DIFF_URL, f'img {i}')
        
        eyes.close(True)
            
    except Exception as e:
        logging.error(f'Error during comparison for test {i}: {e}')
            
    logging.debug('Aborting Eyes session if not closed')    
    
    
            
            
            
        
        
