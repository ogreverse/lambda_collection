import json
import urllib.parse
import boto3
import re
from datetime import datetime
from dateutil import tz

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # バケットとキーを取得
    from_bucket = message['Records'][0]['s3']['bucket']['name']
    from_key = urllib.parse.unquote_plus(message['Records'][0]['s3']['object']['key'], encoding='utf-8')

    # パーティションであれば処理しない
    if (bool(re.match('.*\/[2][0-9]{3}\/[0-1][0-9]\/[0-3][0-9]', from_key))):
        print('date ok')
        return

    # parquet形式でなければ終了
    if (bool(re.match('.*\.parquet', from_key)) is False):
        print('ng')
        return

    # テーブル名を取り出す
    # (参考) ファイルパス: [スナップショット名]/[DB名]/[DB名].[テーブル名]/[ファイル名].gz.parquet
    db_name = from_key.split('/')[-3]
    table_name = from_key.split('/')[-2].split('.')[-1:][0]

    # 日時を取り出す
    # UTCからJSTに変換を行う
    event_time = message['Records'][0]['eventTime']
    utc = datetime.strptime(event_time.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Tokyo')
    utc = utc.replace(tzinfo=from_zone)
    jst = utc.astimezone(to_zone).strftime('%Y-%m-%dT%H:%M:%S')

    split_event_time = jst.split('T')
    date_list = split_event_time[0].split('-')
    date_text = '%s/%s/%s' % (date_list[0], date_list[1], date_list[2])
    hour_text = split_event_time[1].split(':')[0]

    # コピー先のバケットとファイルパスを指定
    to_bucket = from_bucket
    to_filepath = '%s/%s/%s/%s/%s.parquet' % (db_name, table_name, date_text, hour_text, table_name)

    # 各変数を出力
    print(from_bucket)
    print(from_key)
    print(to_bucket)
    print(to_filepath)

    try:
        # コンテンツのタイプの確認
        # response = s3.get_object(Bucket=from_bucket, Key=from_key)
        # print("CONTENT TYPE: " + response['ContentType'])

        # 実際のコピーコマンド
        s3.copy_object(Bucket=to_bucket, Key=to_filepath, CopySource={'Bucket': from_bucket, 'Key': from_key})

        # 元のファイルを削除
        s3.delete_object(Bucket=from_bucket, Key=from_key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e