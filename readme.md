# このBotについて

SlackのReacji Channeler(リアク字チャンネラー)っぽい機能が使えるBotです。

## Table of Contesnts

1. [機能](#機能)

- [このBotについて](#このbotについて)
  - [Table of Contesnts](#table-of-contesnts)
  - [機能](#機能)
    - [リアク字チャンネラー(Discord)カテゴリ(reactionchannelercog.pyで実装)](#リアク字チャンネラーdiscordカテゴリreactionchannelercogpyで実装)
  - [環境変数の説明](#環境変数の説明)
  - [ローカルでの動かし方](#ローカルでの動かし方)
  - [ローカルでの動かし方(Poetry)](#ローカルでの動かし方poetry)
    - [古い方法](#古い方法)

1. [環境変数の説明](#環境変数の説明)

1. [ローカルでの動かし方](#ローカルでの動かし方)

## 機能

### リアク字チャンネラー(Discord)カテゴリ(reactionchannelercog.pyで実装)

`/reactionChanneler` リアク字チャンネラー(Discord)を操作するコマンド（サブコマンド必須）。Slackのリアク字チャンネラーからインスパイアされ、作成したもの。

- リアク字チャンネラー(Discord)追加・・・このリポジトリではスラッシュコマンドが有効なので少し雰囲気が違います  
![image(reactionChanneler_add)](https://github.com/tetsuya-ki/images/blob/main/discord-bot-heroku/reactionChanneler_add.png?raw=true)

- リアク字チャンネラー(Discord)削除・・・このリポジトリではスラッシュコマンドが有効なので少し雰囲気が違います  
![image(reactionChanneler_delete)](https://github.com/tetsuya-ki/images/blob/main/discord-bot-heroku/reactionChanneler_delete.png?raw=true)

- リアク字チャンネラー(Discord)表示・・・このリポジトリではスラッシュコマンドが有効なので少し雰囲気が違います  
![image(reactionChanneler_list)](https://github.com/tetsuya-ki/images/blob/main/discord-bot-heroku/reactionChanneler_list.png?raw=true)

- リアク字チャンネラー(Discord)全削除  
![image(reactionChanneler_purge)](https://github.com/tetsuya-ki/images/blob/main/discord-bot-heroku/reactionChanneler_purge.png?raw=true)

- リアク字チャンネラー(Discord)の対象のリアクションを追加すると、  
![image(reactionChanneler)](https://github.com/tetsuya-ki/images/blob/main/discord-bot-heroku/event_reaction.png?raw=True)

- あらかじめ指定されたチャンネルへリンクが投稿される  
![image(reactionChanneler-2)](https://github.com/tetsuya-ki/images/blob/main/discord-bot-heroku/event_reaction_added.png?raw=True)

- [環境変数](#環境変数の説明)で設定しておけば、別のギルドのチャンネルへリンクを投稿することもできる
![image(reactionChanneler-3)](<https://github.com/tetsuya-ki/images/blob/main/discord-bot-heroku/event_reaction_added(webhook).png?raw=True>)

## 環境変数の説明

- DISCORD_TOKEN = "discord_bot_token"
  - ここにDiscord Botのトークンを貼り付ける(とても重要。これをしないと動かない)
- APPLICATION_ID="99999999"
  - あなたのBotの`APPLICATION ID`を指定する(スラッシュコマンドを使う上で設定が必須となります)
  - [開発者ポータル](https://discord.com/developers/applications/)の該当Botの`General Information`の上部にある、`APPLICATION ID`
- LOG_LEVEL = INFO
  - ログレベルを設定したい場合、設定する。デフォルトはWARNING。DEBUG, INFO, WARNING, ERRORが設定可能
- IS_HEROKU = True
  - Herokuで動かす場合、Trueとする（discordのチャンネルを使用し、リアクションチャネラーのデータが消えないように試みる（`reacji_channel_control`を作成し、そこにjsonデータを添付することでデータを保持する））
- FIRST_REACTION_CHECK = True
  - すでにリアクションが付けられた物について、**リアク字チャンネラー(Discord)を発動しないかどうか**の設定。基本的にはTrueがオススメ。寂しいときはFalseでもOK（何回だってチャンネルに転記されちゃいますが！）
- REACJI_CHANNELER_PERMIT_WEBHOOK_ID = "webhook_id"
  - リアク字チャンネラー(Discord)機能の拡張設定。ここにWebhook IDか「all」という文字列を記載すると、リアク字チャンネラー(Discord)機能でWebhookが使用できる
    - リアクションを設定するだけで、別のギルドにメッセージを転送することができるようになる
  - この環境変数にWebhook IDがない、または、allが記載されていない場合、登録は可能だが、実際に実行はされない
    - 勝手にリアク字チャンネラー(Discord)を登録され情報が流出することを防ぐため、環境変数で指定がない限り実行されないようにする(少し面倒かもしれない)
- ENABLE_SLASH_COMMAND_GUILD_ID
  - スラッシュコマンドを有効にするギルドID(複数ある場合は「;」を間に挟むこと/それぞれのギルドにスラッシュコマンドを許可されたこのBotが必要(どこかのギルドに登録されていない場合、または、登録されていてもスラッシュコマンドが許可されていない場合、エラーとなります))
  - 例
    - 1件の場合: ENABLE_SLASH_COMMAND_GUILD_ID=18471289371923
    - 2件の場合: ENABLE_SLASH_COMMAND_GUILD_ID=18471289371923;1389103890128390

## ローカルでの動かし方

## ローカルでの動かし方(Poetry)

1. Install Poetry  
<https://python-poetry.org/docs/#installation>

2. Install modules  
`poetry install`

3. create .env  
`.env.sample`を参考に`.env`を作成する  
Botは[こちら](https://discord.com/developers/applications)で作成し、トークンを取得する（トークンは厳重に管理すること！）  
＊環境変数を修正する際は、[環境変数の説明](#環境変数の説明)を参照すること！

4. Start Bot  
`poetry run python reacji-channeler-bot.py`

### 古い方法

- 詳しくは[wiki](https://github.com/tetsuya-ki/discord-bot-heroku/wiki)を参照ください！

1. Install modules

    Mac: `pip3 install -r requirements.txt`  
    Windows: `py -3 pip install -r requirements.txt`

2. create .env  
`.env.sample`を参考に`.env`を作成する  
Botは[こちら](https://discord.com/developers/applications)で作成し、トークンを取得する（トークンは厳重に管理すること！）  
＊環境変数を修正する際は、[環境変数の説明](#環境変数の説明)を参照すること！

3. Start Bot

    Mac: `python3 reacji-channeler-bot.py`  
    Windows: `py -3 reacji-channeler-bot.py`
