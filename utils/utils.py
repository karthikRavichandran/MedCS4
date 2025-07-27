import re
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
import logging
from functools import wraps
import yaml

# Configure logging (you can modify this as needed)
logging.basicConfig(level=logging.INFO)


current_dir = os.path.dirname(__file__)
project_root_dir = os.path.join(current_dir, '..')
# data_dir_path = os.path.join(current_dir, '..', 'data')

load_dotenv()

# Access the API key
API = os.getenv('API_KEY')
ORG_ID = os.getenv('ORG_ID')

client = OpenAI(
    api_key=API,
    organization=ORG_ID
)
def extract_dict_text_with_regex(text):
    # Define the regex pattern to match content inside <dict> and </dict> tags
    pattern = r'<dict>(.*?)<\/dict>'

    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)

    # If a match is found, return the text inside the <dict> tag
    if match:
        return match.group(1).strip()
    else:
        return "No <dict> tag found or no content inside <dict>"

def load_fs_example(yaml_path='fs_example_1.yaml'):
    with open(yaml_path, 'r') as file:
        fs_data = yaml.safe_load(file)
    return fs_data
def retry_on_exception(max_retries=5, delay=1, logger=None):
    """
    A decorator to retry a function up to `max_retries` times if it raises an exception.
    Logs the error each time.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    msg = f"[Attempt {retries + 1}] Success: {func.__name__} executed successfully."
                    if logger:
                        logger.info(msg)
                    else:
                        print(msg)
                    return result
                except Exception as e:
                    retries += 1
                    msg = f"[Attempt {retries}] Error: {e}"
                    if logger:
                        logger.error(msg)
                    else:
                        print(msg)
                    if retries == max_retries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# Example usage
# fs1_data = load_fs_example_1()
# print(fs1_data['few_shot_cn'][:300])  # preview first 300 chars
