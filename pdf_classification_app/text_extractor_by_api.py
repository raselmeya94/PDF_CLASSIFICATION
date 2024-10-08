import re
import pandas as pd
import json

# Function to create the extraction prompt
def create_prompt(text):
    # Check if the text contains Bengali characters
    
    # Define the base prompt with a focus on extraction
    base_prompt = f"""
    You are a document analysis assistant. Please analyze the following document text and extract relevant information in JSON format based on the document type. 

    - If the document is a TIN certificate, extract the following fields:
        - Certificate Type: "TIN Certificate"
        - TIN
        - Company Name
        - Registered Address/Permanent Address
        - Current Address
        - Previous TIN
        - Status
        - Date

    - If the document is a VAT certificate, extract the following fields:
        - Certificate Type: "VAT Certificate"
        - BIN
        - Name of the Entity
        - Trading Brand Name
        - Old BIN
        - e-TIN
        - Address
        - Issue Date
        - Effective Date
        - Type of Ownership
        - Major Area of Economic Activity

    - If the document is a Certificate of Incorporation, extract the following fields:
        - Certificate Type: "Certificate of Incorporation"
        - Certificate No
        - Company Name
        - Date of Incorporation
        - Company Type
        - Issue No
        - Issue Date

    - If the document is a Trade License, extract the following fields:
        - Certificate Type: "Trade License"
        - লাইসেন্স নং
        - ইস্যুর কর্তৃপক্ষ
        - ব্যবসা প্রতিষ্ঠানের নাম
        - প্রতিষ্ঠানের মালিকের নাম
        - ব্যবসার ধরণ
        - প্রতিষ্ঠানের ঠিকানা
        - এনআইডি/পাসপোর্ট/ডান্ম নিব: নং
        - ট্রেড লাইসেন্স এর মেয়াদ

    Ensure that the output is in JSON format, and if the input text is in Bengali, return the output in Bengali. If the input text is in English, return the output in English. Do not include any extra text outside of the JSON output.

    **Document Text:**
    {text.strip()}
    """
    
    return base_prompt


def extract_info_to_dataframe(text):
    json_string = text.strip()  
    # Remove the "Info::" prefix and any additional wrapping characters
    if json_string.startswith("```json") and json_string.endswith("```"):
        json_string = json_string[8:-3].strip()  # Remove the backticks and JSON marker

    data = json.loads(json_string)
    df = pd.DataFrame([data])
    return df
