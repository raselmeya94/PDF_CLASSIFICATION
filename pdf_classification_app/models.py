from django.db import models
from .utils import extract_text_from_file 
from .text_extractor_by_api import extract_info_to_dataframe 
import json

class PDF_Info_Extractor(models.Model):
    def file_to_text_info(self, file_data, file_type):

        try:
            extracted_text , info  = extract_text_from_file(file_data, file_type)
            df = extract_info_to_dataframe(info) 
            # Convert DataFrame to a dictionary
            df_dict = df.to_dict(orient='records')  
            # Prepare the response dictionary
            response_dict = {
                'extracted_text': extracted_text,
                'information': df_dict
                } 
            # Convert the dictionary to a JSON string
            response_json = json.dumps(response_dict)

            return response_json
        except Exception as e:
            # Handle exceptions and return an error message as JSON
            error_info = {
                'error': str(e)
            }
            return json.dumps(error_info)
