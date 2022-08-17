#!/usr/bin/python3.8
import urllib.request
import urllib3
import json
import os

def lambda_handler(event, context):
    msg = json.loads(event['Records'][0]['Sns']['Message'])

    body = ''

    if msg['notificationType'] == 'Bounce':
        emails = []
        for recipient in msg['bounce']['bouncedRecipients']:
            emails.append(recipient['emailAddress'])

        body = '(bounce) メールの不達が発生しました\n' + ('送信先メールアドレス : %s' % ','.join(emails))
    elif msg['notificationType'] == 'Complaint':
        emails = []
        for recipient in msg['complaint']['complainedRecipients']:
            emails.append(recipient['emailAddress'])

        body = '(complaint) 迷惑メールに振り分けられました\n' + ('送信先メールアドレス : %s' % ','.join(emails))
    else:
        exit()

    set_fileds = [{
        "title": "Aws SES Notification",
        "value": body,
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
