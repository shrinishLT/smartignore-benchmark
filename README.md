# Applitools Benchmark

## Setup Instructions

### Step 1: Prepare the URLs
1. First, run any to compare on smartUI.
2. from inspect in browser get the base and compare URLs.
3. Add these URLs to the `input array` in the `./dev/URLS/urls.json` file in the following format:

    ```json
    {
      "input": [
        ...,
        {
            "baseURL" : "baseURL",
            "compareURL" : "compareURL"
        } 
      ]
    }
    ```

### Step 2: Set Up the Virtual Environment
1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```
2. Activate the virtual environment:
    ```bash
    source ./venv/bin/activate
    ```

### Step 3: Install Dependencies
1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Step 4: Run the Tests
1. Execute the test script:
    ```bash
    python3 test.py
    ```

For now if images sizes are diff, then we crop the images for comparison.

Check results over here : https://eyes.applitools.com/app/test-results/00000251679172704040/?accountId=CfAK6A8gQUu241SoODU2OA__

email : vhanbatte@iitkgp.ac.in
password: Shrinish@123