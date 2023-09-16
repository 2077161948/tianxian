import json
import os
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from corsheaders.middleware import CorsMiddleware

from tianxian.settings import MEDIA_ROOT
from web.service.word import pdf_service
from web.util.file_util import file_response
from web.util.result_util import success_result_json


# Create your views here.

def index(request):
    return HttpResponse('is ok')


@csrf_exempt
def pdf_to_word(request):
    file_result = pdf_service.PdfService(request).pdf_to_world()
    return file_response(file_result)


@csrf_exempt
def pdf_to_txt(request):
    txt = pdf_service.PdfService(request).text_pdf()
    return success_result_json('提取成功',txt)

