# moveExportedRdsSnapshot

[< 戻る](../../README.md)

`exportRdsSnapshot`のLambda FunctionによりS3に出力されたsnapshotのデータを、パーテーションで分けたディレクトリへ移動する。

## 概要

S3 bucketのPUTイベントメッセージを受け取り、同じS3 bucket内のディレクトリへ移動する。

## 参考資料

- [Lambda(Python)でRDSスナップショットをS3にエクスポートする](https://qiita.com/hmdsg/items/a948b8e30eb5503438af)
- [DB snapshot events](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.Messages.html#USER_Events.Messages.snapshot)

## 動作環境

- Lambda (Python 3.9)
  - タイムアウト 1分
  - メモリ 128MB

## 使用方法

1. SNSに通知先を作成する。
    - トピックを作成する。
        - 通知メッセージを確認するためには一旦Emailを通知先にする。
    - S3のSNSへの操作を許可する。
        - SNSトピックのアクセスポリシーのStatementに追加する。 (`[]`内のIDは必要に応じて書き換える)
        ```
        {
          "Sid": "s3-statement-id",
          "Effect": "Allow",
          "Principal": {
            "Service": "s3.amazonaws.com"
          },
          "Action": "SNS:Publish",
          "Resource": "arn:aws:sns:ap-northeast-1:[account-id]:exported-rds-snapshot-put",
          "Condition": {
            "StringEquals": {
              "aws:SourceAccount": "[bucket-owner-account-id]"
            },
            "ArnLike": {
              "aws:SourceArn": "arn:aws:s3:::[bucket-name]"
            }
          }
        },
        ```
2. S3イベントを通知する。
    - S3バケットのプロパティの「イベント通知」からイベントを作成する。
    - 設定
        - イベント名 "exported-snapshot-put"
        - サフィックス ".parquet"
        - イベントタイプ
            - オブジェクトの作成 → PUT
        - 送信先
            - SNSトピック "exported-rds-snapshot-put"
3. Lambda Functionで利用するIAM Roleの作成
    - S3の権限を与える。
4. Lambda Functionを作成する。
    - [Githubリポジトリ](https://github.com/ogreverse/lambda_collection/tree/main/python/moveExportedRdsSnapshot) 
    - 基本的な情報
        - 関数名: "moveRDSSnapshot"
        - ランタイム Python3.9
    - 実行時間, Roleを設定する。
5. SNSの通知先にLambda関数を設定する。

## テスト用のjsonファイル `test.json` について

開発時に使用したRDSからイベント通知されたメッセージを想定したものを用意している。
適宜、`['Records'][0]['Sns']['Message']` の内容を変更して使用すること。
