import os
import uuid
import zipfile
from datetime import datetime
import random

from django.http import HttpResponseRedirect

from tianxian.settings import MEDIA_ROOT


def upload_file(request):
    if request.method == 'POST':
        try:
            file_list = request.FILES.getlist('file_list')
            result = []
            if file_list:
                for file in file_list:
                    item = {}
                    date = datetime.now().strftime('%y%m%d%H%M%S') + str(random.randint(100000, 9999999))
                    filename = f'{date}_{file.name}'
                    path = os.path.join(MEDIA_ROOT, filename)
                    item['name'] = filename
                    item['path'] = path
                    item['filetype'] = filename.split('.')[-1]
                    with open(path, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                    result.append(item)
                return result
        except Exception as e:
            print(e)
            return []
    return []


def result_file(result_file_path):
    if len(result_file_path) == 1:
        return result_file_path[0]
    else:
        name = f'{uuid.uuid4()}.zip'
        zip_file_path = os.path.join(MEDIA_ROOT, name)
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in result_file_path:
                zipf.write(item['path'])
        return {'name': name, 'path': zip_file_path}


def file_response(file_result):
    response = HttpResponseRedirect(file_result['name'])
    response['Content-Disposition'] = f'attachment; filename={file_result["name"]}'
    response['Content-Length'] = os.path.getsize(file_result['path'])
    response['Content-Type'] = 'application/octet-stream'
    with open(file_result['path'], 'rb') as file:
        while True:
            chunk = file.read(1024)
            if not chunk:
                break
            response.write(chunk)
    return response
