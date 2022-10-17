# makeEbsSnapshot

[< 戻る](../../README.md)

RDSのSnapshotをS3に出力する。

## 概要

S3の指定したbucket内でsnapshotが出力されたディレクトリを探し、parquetファイルがなければ削除する

## 動作環境

- Lambda (Python 3.9)
  - タイムアウト 1分
  - メモリ 128MB

## 使用方法

1. S3Bucketが存在するリージョンでLambda関数を作成する。 (lambda_function.py)
  - Lambda用のIAM RoleをLambda関数と一緒に新たに作成する。
  - タイムアウトの時間を設定する。

2. 1で作成したIAM Roleにs3に関するPolicyを追加する
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3bucketPolicy",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject*",
                "s3:DeleteObject*",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::{bucket_name}",
                "arn:aws:s3:::{bucket_name}/*"
            ]
        }
    ]
}
```
3. 環境変数を設定する
  - S3_BUCKET_NAME
    - 出力先のS3バケット名
4. テストしてS3のオブジェクトが削除されるか確認する 
  - **注意** テストする際は削除の箇所をオブジェクトをprintするなどで削除が走らないようにして削除したいオブジェクトのパスが出力されるのを確認して
から実際に削除するのが安全

## テスト用のjsonファイル `test.json` について
空のJSONで良い
