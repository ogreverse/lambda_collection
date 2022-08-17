# README

SESでBounceやComplaintが発生した際に,SNSからの通知をSlackへ通知を送る。

## Slack Web Hook URL 取得先

Lambdaの環境変数 `HOOK_URL` に以下で取得したWeb Hook URLを設定する。

[https://api.slack.com/apps](https://api.slack.com/apps)

(1) App Name "SlackNotification" を選択する。
(2) 左カラムメニューのIncoming Webhooks を選択する。
(3) "Add New Webhook to Workspace" から追加する。

## テスト実行時に使用するjsonファイル

`test.json`  
