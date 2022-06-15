import boto3
import json
import os
from datetime import datetime

client = boto3.client('rds')

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    event_id = message['Event ID']

    # 手動スナップショット取得
    EVENT_ID_MANUAL_CREATED = 'RDS-EVENT-0042'
    # 自動スナップショット取得
    EVENT_ID_AUTOMATED_CREATED = 'RDS-EVENT-0091'

    if EVENT_ID_MANUAL_CREATED in event_id == False and EVENT_ID_AUTOMATED_CREATED in event_id == False:
        return

    source_id = message['Source ID']
    try:
        result = client.describe_db_snapshots(DBSnapshotIdentifier=source_id)

        # ターゲット外のインスタンスであれば終了
        db_instance_identifier = result['DBSnapshots'][0]['DBInstanceIdentifier']
        if (db_instance_identifier in os.environ['TARGET_RDS_INSTANCES'].split(',')) == False:
            return

        # snapshot ARNを取得
        snapshot_arn = result['DBSnapshots'][0]['DBSnapshotArn']
    except client.exceptions.DBSnapshotNotFoundFault:
        print('スナップショットなし')

    export_task_identifier='exporting_snapshot_' + datetime.now().strftime("%Y%m%d%H%M%S")

    response = client.start_export_task(
        ExportTaskIdentifier=export_task_identifier,
        SourceArn=snapshot_arn,
        S3BucketName=os.environ['S3_BUCKET_NAME'],
        IamRoleArn=os.environ['IAM_ROLE_ARN'],
        KmsKeyId=os.environ['KMS_KEY_ID'],
    )