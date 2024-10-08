# utils.py
import io
import re
from PIL import Image 
from pdf2image import convert_from_bytes
from io import BytesIO
from .text_extractor_by_api import create_prompt

# =================================================Custom requirements =================================
# import io
# import re
# from PIL import Image , ImageEnhance, ImageFilter
# import cv2
# import pytesseract
# import fitz  # PyMuPDF
# import pandas as pd
# import numpy as np
# from pdf2image import convert_from_bytes
# from io import BytesIO
# import matplotlib.pyplot as plt

# API 
from .text_extractor_by_api import create_prompt

#-----------------------Spell Checker ----------------------------------------------------------------
# from spellchecker import SpellChecker

#  spell = SpellChecker()
# def text_correction(text):
#     corrected_text = ""
#     words = text.split(" ")
    
#     for word in words:
#         # Check if the word is potentially misspelled and starts with specific letters
#         if word[0] in ['R', 'A', 'P', 'S']:
#             # Check if the word is in the dictionary
#             if word in spell:
#                 corrected_text += word + " "
#             else:
#                 # Get the most likely correction
#                 correction = spell.correction(word)
#                 if correction:
#                     corrected_text += correction + " "
#                 else:
#                     corrected_text += word + " "  # Fallback to original word if no correction is found
#         else:
#             corrected_text += word + " "
    
#     return corrected_text.strip()
    
# -------------------------------- PDF to Image ----------------------------------------------------------------
#  Way : 1
# def pdf_to_images(pdf_data):
#     try:
#         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#         images_text = ""
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document.load_page(page_num)
#             pix = page.get_pixmap(matrix=fitz.Matrix(650 / 72, 650 / 72))  # Increase resolution with matrix
#             image_data = pix.tobytes(output="jpeg")
#             images_text += extract_text_from_image(image_data)
#         return images_text
#     except Exception as e:
#         print(f"Error converting PDF to images: {e}")
#         return ""

# Way : 2
# def pdf_to_images(pdf_data):
#     try:
#         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#         images_text = ""
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document.load_page(page_num)

#             # Increase resolution and convert page to pixmap
#             scaling_factor = 4.5  # Adjust this scaling factor as needed
#             pix = page.get_pixmap(matrix=fitz.Matrix(scaling_factor, scaling_factor))

#             # Convert pixmap to image
#             image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#             # Convert image to JPEG format
#             image_io = io.BytesIO()
#             image.save(image_io, format='JPEG')
#             image_data = image_io.getvalue()

#             # Extract text from the image
#             text = extract_text_from_image(image_data)
#             images_text += text + "\n"  # Add extracted text to the result

#         return images_text
#     except Exception as e:
#         print(f"Error converting PDF to images: {e}")
#         return ""


def pdf_to_page_extraction(file_data):
    try:
        pages = convert_from_bytes(file_data)
        pdf_text = ""
        for page in pages:
            with BytesIO() as image_stream:
                page.save(image_stream, format='JPEG')
                image_stream.seek(0)
                page_text = image_to_text_with_gimini(image_stream.getvalue())
                # Concatenate the extracted text and info
                pdf_text += page_text
        return pdf_text 
    except Exception as e:
        print(f"Error extracting text from PDF images: {e}")
        return ""
# -----------------------------Image to text extraction function(manually)-----------------------------------------------
# Way: 1
# def extract_text_from_image_only(image_data):
#     image = Image.open(io.BytesIO(image_data))
#     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
#     text = pytesseract.image_to_string(image)
#     return text


# # Way : 2
# def adjust_brightness_contrast(image, alpha, beta):
#     return cv2.addWeighted(image, alpha, image, 0, beta)

# def extract_text_from_image(image_data):
#     # Load image from bytes and convert to OpenCV format
#     image = Image.open(io.BytesIO(image_data))
#     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV

#     enhanced_image = adjust_brightness_contrast(image, 1, 5)
#     # Save the enhanced image for debugging or further use
#     enhanced_image_path = "enhanced_image.png"
#     cv2.imwrite(enhanced_image_path, enhanced_image)
#     # Extract text from the preprocessed image
#     text = pytesseract.image_to_string(enhanced_image, lang = 'eng+ben')
#     return text

# def text_to_info_finder(text):
#     print("Extracted Text: ", text)
#     # corrected_text = text_correction(text)
#     # print("Corrected Text: ", corrected_text)
#     # text= corrected_text
#     document_type = "OTHER"
#     # Determine document type
#     if "TIN Certificate" in text or "Taxpayer's Identification Number (TIN) Certificate" in text:
#         document_type = "TIN"
#     elif "Value Added Tax" in text or "Value Added Tax Registration Certificate" in text or "Customs, Excise and VAT Commissionerate" in text:
#         document_type="VAT"
#     elif "Certificate of Incorporation" in text or " incorporated\nunder the Companies Act" in text:
#         document_type="INCORPORATE"
#     elif  "লাইসেন্স" in text or  "ই-ট্রেড লাইসেন্স" in text:
#         document_type="TRADE"
    
        


#     final_details = {}       
#     # Handle TIN Certificate
#     if document_type == "TIN":
#         tin_number = re.search(r'TIN\s*:?\s*(\d+)', text)
#         company_name =re.search(r"Name\s*[[:=\'»\s>\-;©]\s*([^\n]+)", text, re.IGNORECASE | re.DOTALL)
#         # registered_address =  re.search(r'Registered Address/Permanent Address\s*:?\s*(.+?)\s*\d+\s*Current Address\s*:', text, re.DOTALL)
#         # current_address = re.search(r'Current Address\s*[:=\'»\s>\-;©]*\s*(.*?)', text, re.DOTALL)
#         # registered_address =  re.search(r'Registered Address/Permanent Address\s*:?\s*(.+?)\s*\d+\s*Current Address\s*:', text, re.DOTALL)
#         registered_address = re.search(r'Registered Address/Permanent Address\s*[:=\'»\s>\-;©]*\s*(.*?PO\s*:\s*\d+)' , text, re.DOTALL| re.IGNORECASE)
#         current_address = re.search(r'Current Address\s*[:=\'»\s>\-;©]*\s*((?:.|\n)*?)(?:PO\s*:\s*\d+)?(?:\s*\n|$)', text, re.DOTALL) # ?\s*(?:\n|$)
#         previous_tin = re.search(r'Previous TIN\s*[[:=\'»\s>\-;]\s*([^\n]+)', text, re.DOTALL)
#         status =re.search(r'(?:Status|Staus|status|Satus)\s*[[:=\'»\s>\-;]\s*([^\n]+)', text, re.DOTALL)
#         # date = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*\d{1,2},\s*\d{4}', text, re.IGNORECASE)
#         date = re.search(r'Date\s*[[:=\'»\s>\-;]\s*([^\n]+)', text, re.IGNORECASE)
        

#         details = {
#             'Document Type': 'TIN Certificate',
#             'TIN': tin_number.group(1) if tin_number else None,
#             # 'Registration Number': registration_number.group(1) if registration_number else None,
#             'Company Name': company_name.group(1).strip() if company_name else None,
#             'Registered Address': registered_address.group(1).replace('\n', ' ').strip() if registered_address else None,
#             'Current Address': current_address.group(1).replace('\n', ' ').strip() if current_address else None,
#             'Previous TIN': previous_tin.group(1) if previous_tin else None,
#             'Status': status.group(1) if status else None,
#             'Date' : date.group(1) if date else None
#         }

#         final_details.update(details) 
    
#     elif document_type=="VAT":

#         BIN = re.search(r"BIN\s*:?\s*(\d{9}-\d{4})", text, re.DOTALL)
#         name_of_entity = re.search(r"Name\s+of\s+the\s+Entity\s*[:='\s>\s]*\s*(.*?)\s*(?=\n|$)", text, re.IGNORECASE | re.DOTALL) #re.search(r"Name\s+of\s+the\s+Entity\s*:?\s*(.*?)(?= Trading)", text, re.DOTALL)
#         trading_brand_name = re.search(r"Trading\s+Brand\s+Name\s*[:='\s>\s]*\s*([^:='\s>\n][^:='\n]*?)(?=\n|$)", text, re.IGNORECASE | re.DOTALL) # re.search(r"Trading\s+Brand\s+Name\s*[:='\s>\s]*\s*(.*?)(?=\n|$)", text, re.IGNORECASE | re.DOTALL)
#         old_bin = re.search(r"Old\s+BIN\s*[:='\s]*\s*([^:='\s\n][^:='\n]*?)(?=\n|$)", text, re.IGNORECASE | re.DOTALL) # re.search(r"Old\s+BIN\s*:?\s*(\d+)", text)
#         etin = re.search(r"e-TIN\s*:?\s*(\d+)", text)
#         # etin = re.search(r"(?:e-TIN\s*:?\s*(\d+))|((\d+)\s*e-TIN)", text)
#         address = re.search(r"Address\s*:?\s*(.*?)(?=\n(?:Issue\s+Date)|$)", text, re.IGNORECASE | re.DOTALL)
#         issue_date = re.search(r"Issue Date\s*:?\s*(\d{2}/\d{2}/\d{4})", text)
#         effective_date = re.search(r"(?:Bfective Date|Effective Date)\s*:?\s*(\d{2}/\d{2}/\d{4}|\d{2}/\d{4})", text)
#         type_of_ownership = re.search(r"Type\s+of\s+Ownership\s*:?\s*(.*?)(?=Major)", text, re.DOTALL)
#         major_area_of_activity = re.search(r"Major\s+Area\s+of\s+Economic\s+Activity\s*:?\s*(.*?)(?=\n|\Z)", text, re.IGNORECASE | re.DOTALL) #re.search(r"Major\s+Area\s+of\s+Economic\s+Activity\s*:?\s*(.*?)(?=This)", text, re.DOTALL)

#         details = {
#             'Document Type': 'VAT Certificate',
#             'BIN': BIN.group(1) if BIN else None,
#             'Name of the Entity': name_of_entity.group(1).strip() if name_of_entity else None,
#             'Trading Brand Name': trading_brand_name.group(1).strip() if trading_brand_name else None,
#             'Old BIN': old_bin.group(1) if old_bin else None,
#             'e-TIN': etin.group(1) if etin else None,
#             'Address': address.group(1).strip() if address else None,
#             'Issue Date': issue_date.group(1) if issue_date else None,
#             'Effective Date': effective_date.group(1) if effective_date else None,
#             'Type of Ownership': type_of_ownership.group(1).strip() if type_of_ownership else None,
#             'Major Area of Economic Activity': major_area_of_activity.group(1).strip() if major_area_of_activity else None,
#         }
#         final_details.update(details)



#     elif document_type=="INCORPORATE":
#         certificate_no = re.search(r"No\.?\s*(C-\d+/\d{4})", text, re.DOTALL)
#         company_name = re.search(r"I hereby certify that\s+(.*?)\s+is", text, re.DOTALL)
#         date_of_incorporation = re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text, re.DOTALL)
#         limited_company_type = re.search(r"that\s*the\s*Company\s*is\s+(Limited|Private Limited)", text, re.DOTALL| re.IGNORECASE)
#         issue_no = re.search(r"Issue\s+No\.\s*(\d+)", text, re.DOTALL)
#         issue_date = re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text, re.DOTALL)

#         details = {
#             'Document Type': 'Incorporation Certificate',
#             'Certificate No.': certificate_no.group(1).strip() if certificate_no else None,
#             'Company Name': company_name.group(1).strip() if company_name else None,
#             'Date of Incorporation': date_of_incorporation.group(1) if date_of_incorporation else None,
#             'Company Type': limited_company_type.group(1) if limited_company_type else None,
#             'Issue Number': issue_no.group(1) if issue_no else None,
#             'Issue Date': issue_date.group(1) if issue_date else None,
#         }

#         final_details.update(details)
#     # Trade License
#     elif document_type == "TRADE":
#         issue_date = re.search(r'ইস্যুর তারিখ\s*:\s*([\d/]+)', text, re.DOTALL)
#         city_corporation_name = re.search(r'(ঢাকা উত্তর সিটি কর্পোরেশন|ঢাকা দক্ষিণ সিটি কর্পোরেশন)', text, re.DOTALL) #|চট্টগ্রাম সিটি কর্পোরেশন|খুলনা সিটি কর্পোরেশন|রাজশাহী সিটি কর্পোরেশন|বরিশাল সিটি কর্পোরেশন|সিলেট সিটি কর্পোরেশন|রংপুর সিটি কর্পোরেশন
#         license_number = re.search(r'লাইসেন্স নং\s*:\s*([\d/]+)', text, re.DOTALL)
#         business_name = re.search(r'ব্যবসা প্রতিষ্ঠানের নাম\s*([^\n]+)', text, re.DOTALL)
#         owner_name = re.search(r'প্রতিষ্ঠানের মালিকের নাম\s*([^\n]+)', text, re.DOTALL)
#         business_type = re.search(r'ব্যবসার ধরণ\s*([^\n]+)', text, re.DOTALL)
#         business_address = re.search(r'প্রতিষ্ঠানের ঠিকানা\s*([^\n]+)', text, re.DOTALL)
#         nid_passport_dln_number = re.search(r'এনআইডি/পাসপোর্ট/ডান্ম নিব: নং\s*([\d]+)', text, re.DOTALL)
#         trade_license_expiry_date = re.search(r'ট্রেড লাইসেন্স এর মেয়াদ\s*([\d]+[^\d,]+, \d{4})', text, re.DOTALL)

#         details = {
#             'Document Type': 'Trade Certificate',
#             'Issue Date': issue_date.group(1).strip() if issue_date else None,
#             'City Corporation Name': city_corporation_name.group(1).strip() if city_corporation_name else None,
#             'License Number': license_number.group(1).strip() if license_number else None,
#             'Business Name': business_name.group(1).strip() if business_name else None,
#             'Owner Name': owner_name.group(1).strip() if owner_name else None,
#             'Business Type': business_type.group(1).strip() if business_type else None,
#             'Business Address': business_address.group(1).strip() if business_address else None,
#             'NID/Passport/B Number': nid_passport_dln_number.group(1).strip() if nid_passport_dln_number else None,
#             'Trade License Expiry Date': trade_license_expiry_date.group(1).strip() if trade_license_expiry_date else None,
#         }

#         final_details = details
#     print("Info:: " , text)
#     final_details= API_INFO_EXTRACTOR(text)
    
#     return final_details
    
#====================================Using Gemini API================================

# Gimini API Call
import google.generativeai as genai
API_KEY="AIzaSyDnL3F7x_xh-BYsx_144N06FHBKhDTFCCc"
genai.configure(api_key= API_KEY)

def image_to_text_with_gimini(image_data):
    # Load image from bytes and convert to OpenCV format
    image = Image.open(io.BytesIO(image_data))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(["Extract Full Text without Special", image])
    return response.text

def extract_info_with_gemini(text):
    try:
        prompt = create_prompt(text)

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([prompt])
        return response.text if response else None
    except Exception as e:
        print(f"Error in Gemini Info Extraction: {e}")
        return ""

def extract_text_from_file(file_data, file_type):
    try:
        if file_type == 'image':
            image_text= image_to_text_with_gimini(file_data)
            info=extract_info_with_gemini(image_text)
            return image_text , info
        elif file_type == 'pdf':

            pdf_text=pdf_to_page_extraction(file_data)
            info=extract_info_with_gemini(pdf_text)

            return pdf_text , info


        else:
            return ""
    except Exception as e:
        print(f"Error extracting text from file: {e}")
        return ""
