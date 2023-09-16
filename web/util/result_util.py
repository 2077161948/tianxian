import json
from django.http import HttpResponse


def result_json(msg, status, data):
    json_data = {
        'msg': msg,
        'status': status,
        'data': data
    }
    result = json.dumps(json_data,ensure_ascii=False)
    return HttpResponse(result,headers={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Methods":"*"})


def success_result_json(msg='', data=[]):
    return result_json(msg, 0, data)


def error_result_json(msg='', data=[]):
    return result_json(msg, -1, data)
