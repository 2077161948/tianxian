import json
import os
from datetime import datetime


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from corsheaders.middleware import CorsMiddleware

from tianxian.settings import MEDIA_ROOT
from web.util.result_util import success_result_json


# Create your views here.

def index(request):
    return HttpResponse('is ok')


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('file')
            if file:
                date = datetime.now().strftime('%y%m%d%H%M%S')
                filename = f'{date}_{file.name}'
                path = os.path.join(MEDIA_ROOT, filename)
                with open(path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                return success_result_json('上传成功')
        except Exception as e:
            return success_result_json('上传失败')
    return success_result_json('上传失败')


def pdf_to_word(request):
    params = request.content_params()
    return HttpResponse(params)
