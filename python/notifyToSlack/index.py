#!/usr/bin/python3.9
import urllib.request
import urllib3
import json
import os

def lambda_handler(event, context):
    msg = event['Records'][0]['Sns']['Message']
    set_fileds = [{
        "title": "Aws Notification",
        "value": msg,
        "short": False
    }]

    data = {
        'attachments':  [{
            'color': 'danger',
            'fields': set_fileds
        }]
    }

    url = os.environ['HOOK_URL']
    method = 'POST'
    request_headers = { 'Content-Type': 'application/json; charset=utf-8' }
    body = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(
        url=url,
        data=body,
        method=method,
        headers=request_headers
    )

    urllib.request.urlopen(request)
