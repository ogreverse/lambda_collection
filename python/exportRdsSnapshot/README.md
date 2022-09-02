# makeEbsSnapshot

[< 戻る](../../README.md)

RDSのSnapshotをS3に出力する。

## 概要

snapshotの作成後のイベントメッセージを受け取り、S3へparquet形式でexportする。

## 参考資料

- [Lambda(Python)でRDSスナップショットをS3にエクスポートする](https://qiita.com/hmdsg/items/a948b8e30eb5503438af)
- [DB snapshot events](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.Messages.html#USER_Events.Messages.snapshot)

## 動作環境

- Lambda (Python 3.9)
  - タイムアウト 1分
  - メモリ 128MB

## 事前準備

- SnapshotをS3にExportするためのIAM Roleを作成する。 (S3WritableRole)
  - Policy
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "VisualEditor0",
          "Effect": "Allow",
          "Action": [
            "s3:ListBucket",
            "s3:GetBucketLocation"
          ],
          "Resource": "arn:aws:s3:::*"
        },
        {
          "Sid": "VisualEditor1",
          "Effect": "Allow",
          "Action": [
            "s3:PutObject*",
            "s3:GetObject*",
            "s3:DeleteObject*"
          ],
          "Resource": [
            "arn:aws:s3:::my-s3-bucket",
            "arn:aws:s3:::my-s3-bucket/*"
          ]
        }
      ]
    }
    ```
- Lambda用のIAM Roleを作成する。 (RdsSnapshotExporter)
  - Policy
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "iam:PassRole",
            "rds:StartExportTask",
            "rds:DescribeDBSnapshots"
          ],
          "Resource": "*"
        }
      ]
    }
    ```
- KMSキーの作成
  - ※ 既にキーが作成されている場合は、キーポリシーのSid が 
    'Allow attachment of persistent resources' と 'Allow use of the key'
    のそれぞれのPrincipalにLambdaのIAM Roleを加える。 
  - カスタマー管理方キー
    - キーのタイプ : 対象
    - キー管理者 : 任意のユーザー
    - キーの使用アクセス許可 : 作成したLambdaのIAM Role

## 使用方法

1. RDS Snapshotが存在するリージョンでLambda関数を作成する。 (lambda_function.py)
  - Lambda用のIAM Roleを指定する。
  - タイムアウトの時間を設定する。 
2. 環境変数を設定する
  - TARGET_RDS_INSTANCES
    - 対象のRDSインスタンス名
  - S3_BUCKET_NAME
    - 出力先のS3バケット名
  - IAM_ROLE_ARN
    - S3エクスポートする際に使用するIAM RoleのARN 
  - KMS_KEY_ID
    - KMSキーのID
      - ARNの `arn:aws:kms:[region]:[AWS ID]:key/` 以降の末尾についている
3. テストしてS3のbucketに吐き出されるか確認する。 
  - **注意** タスク起動後、バックグラウンドで30分以上出力の処理に時間がかかるのでテストを連打しないこと。

## テスト用のjsonファイル `test.json` について

開発時に使用したRDSからイベント通知されたメッセージを想定したものを用意している。
適宜、`['Records'][0]['Sns']['Message']` の内容を変更して使用すること。

## Tips

- RDSのExportタスクの確認用コマンド
  - `$ aws rds describe-export-tasks`
