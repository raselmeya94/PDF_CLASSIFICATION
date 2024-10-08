# views.py
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .utils import extract_text_from_file
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import PDF_Info_Extractor
import base64
import json
import magic
import imghdr
from django.conf import settings
from .text_extractor_by_api import extract_info_to_dataframe 

def upload_file(request):
    # print("Output: " , request.FILES.getlist('files'))
    data = [] # Dictionary to store data for the template
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_files = request.FILES.getlist('files')

        # uploaded_files: InMemoryUploadedFile = form.cleaned_data['files']

        for uploaded_file in uploaded_files:
            file_data = uploaded_file.read()
            file_type = uploaded_file.content_type
            # print(uploaded_file.name )
            #

            if file_type.startswith('image'):
                file_type = 'image'
            elif file_type == 'application/pdf':
                file_type = 'pdf'
            else:
                print("Sorry File Type Don't Match")
                # return render(request, 'index.html', {
                #     'form': form,
                #     'error': 'Unsupported file type for: {}'.format(uploaded_file.name)
                # })
            #
            extracted_text, info = extract_text_from_file(file_data, file_type)
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            # Generate DataFrame and HTML for each file
            df = extract_info_to_dataframe(info)
            # df_info=pd.DataFrame([df])
            df_html =df.to_html(index=False)
            # print(uploaded_file.size)

            data.append({
                'filename': uploaded_file.name,
                'file_size': str(round(uploaded_file.size / 1024 , 2))+" KB",
                'uploaded_file_data':encoded_file,
                'extracted_text': extracted_text,
                'file_type': file_type,
                'df_html': df_html,
            })
            # data.append({
            #     uploaded_file.name: {
            #         'uploaded_file_data': encoded_file,
            #         'extracted_text': extracted_text,
            #         'file_type': file_type,
            #         'df_html': None
            #     }
            # })



        return render(request, 'index.html', {'form': form, 'data': data })


    else:
        form = UploadFileForm()
        return render(request, 'index.html', {'form': form, })



# API  
@csrf_exempt
def classified_pdf_information(request):
    if request.method == 'POST':
        try:
            files = []
            content_length = int(request.META.get('CONTENT_LENGTH', 0))
            if content_length > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
                return JsonResponse({'error': 'Total file size exceeds the limit'}, status=400)

            # android porposed ( body: raw)
            data = json.loads(request.body.decode('utf-8'))
            base64_data_list = data.get('file_data', [])
            # Check for base64 encoded data in request.POST
            # if 'file_data' in request.POST:
            #     base64_data_list = request.POST.getlist('file_data')
            if base64_data_list:
                
                for encoded_file in base64_data_list:
                    try:
                        decoded_file = base64.b64decode(encoded_file)
                        files.append(decoded_file)
                    except base64.binascii.Error:
                        return HttpResponse({"status":"Error decoding base64 file. Please ensure it is properly encoded."}, status=400)
            
            # Check for files in request.FILES
            # if 'file_data' in request.FILES:
            #     files.extend(request.FILES.getlist('file_data'))
            
            # Check if files were retrieved
            if not files:
                return HttpResponse({"status":"No files uploaded. Please check your 'file_data' key and ensure files are attached."}, status=400)
            
            
            # Check if the number of files exceeds the limit
            if len(files) > settings.DATA_UPLOAD_MAX_NUMBER_FILES:
                return JsonResponse({'error': 'Too many files'}, status=400)
            
            response_data = {"status": "success", "data": []}
            for file in files:
                if isinstance(file, bytes):
                    file_data = file

                    # Determine file type using python-magic
                    mime = magic.Magic(mime=True)
                    file_type = mime.from_buffer(file_data)

                    if file_type.startswith('image'):
                        file_type = 'image'
                    elif file_type == 'application/pdf':
                        file_type = 'pdf'
                    else:
                        return HttpResponse({"status":"Error File Format!! Please make sure files are image or pdf."}, status=400)
                else:
                    file_type = file.content_type
                    file_data = file.read()
                    if file_type.startswith('image'):
                        file_type = 'image'
                    elif file_type == 'application/pdf':
                        file_type = 'pdf'
                    else:
                        return HttpResponse({"status":"Error File Format!! Please make sure files are image or pdf."}, status=400)
                
                info_extractor = PDF_Info_Extractor()
                final_info = info_extractor.file_to_text_info(file_data, file_type)
                final_info_json = json.loads(final_info)  # Convert JSON string back to dictionary

                response_data["data"].append(final_info_json)

            return JsonResponse(response_data, safe=False)
        except Exception as e:
            return HttpResponse(str(e), status=400)  # Handle any exceptions
    else:
        return HttpResponse("Method not allowed", status=405)
