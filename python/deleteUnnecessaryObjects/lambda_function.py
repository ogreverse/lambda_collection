import json
import boto3
import re
import os

s3 = boto3.client('s3')
bucket_name = os.environ['S3_BUCKET_NAME']


def lambda_handler(event, context):
    res = s3.list_objects(Bucket = bucket_name, Delimiter = '/')
    target_dir_objs = []
    for dir_obj in res['CommonPrefixes']:
        target = dir_obj['Prefix']
        if re.search(r'-20[0-9]{12}/$', target) is not None:
            print(target)
            objects = s3.list_objects(Bucket = bucket_name, Prefix = target, Delimiter = '/')
            has_parquet = search_parquet_file(objects)
            if not has_parquet:
                # parquetファイルがない場合はスナップショットが出力されたディレクトリを削除する
                delete_objects(target)


def search_parquet_file(objects):
    """
    再帰的にparquetファイルを探索する
    """
    has_parquet = False
    if 'Contents' in objects.keys():
        # ファイルがある場合
        for obj in objects['Contents']:
            if re.search(r'.parquet$', obj['Key']) is not None:
                print('parquet file detected ' + obj['Key'])
                return True

    if 'CommonPrefixes' in objects.keys():
        # nestしてる場合
        for obj in objects['CommonPrefixes']:
            nest_objects = s3.list_objects(Bucket = bucket_name, Prefix = obj['Prefix'], Delimiter = '/')
            has_parquet = has_parquet or search_parquet_file(nest_objects)

    return has_parquet


def delete_objects(target):
    """
    指定したKey以下にあるObjectを削除する
    """
    objects = s3.list_objects(Bucket = bucket_name, Prefix = target)
    if 'Contents' in objects.keys():
        for obj in objects['Contents']:
            response = s3.delete_object(Bucket = bucket_name, Key = obj['Key'])
            print(response)
            print('delete ' + target)