import re
from openai import OpenAI
import os
from dotenv import load_dotenv
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

import yaml

def load_fs_example(yaml_path='fs_example_1.yaml'):
    with open(yaml_path, 'r') as file:
        fs_data = yaml.safe_load(file)
    return fs_data

# Example usage
# fs1_data = load_fs_example_1()
# print(fs1_data['few_shot_cn'][:300])  # preview first 300 chars
