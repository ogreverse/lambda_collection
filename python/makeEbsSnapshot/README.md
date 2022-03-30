# makeEbsSnapshot

[< 戻る](../../README.md)

自動的にEC2のボリュームのスナップショットを作成する。

## 概要

特定のタグを含むEBSボリュームのスナップショットを作成する。

[参考資料](https://inaba-serverdesign.jp/blog/20180330/aws_ec2_create_snapshot_lambda.html)

## 動作環境

- Lambda (Python 3.6)
  - タイムアウト 1分
  - メモリ 256MB

## 使用方法

- (1) EBSボリュームが存在するリージョンでLambda関数を作成する。 (lambda_function.py)
- (2) 対象とするボリュームのタグで、<br>
  `Key: <TAGKEYの文字列>, Value: <保存世代数>` <br>
  を設定する。<br>
  ※ EC2ではなくEC2のボリュームのタグに設定するので注意。
- (3) EventBridgeにてLambdaを実行するルールを作成する。
  - 日本時間深夜0時に実行するためのcron式 `0 15 * * ? *`