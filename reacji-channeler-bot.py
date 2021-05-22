from discord.ext import commands  # Bot Commands Frameworkをインポート
from discord_slash import SlashCommand
from cogs.modules import settings
from logging import basicConfig, getLogger

import discord
# 先頭に下記を追加
import keep_alive

basicConfig(level=settings.LOG_LEVEL)
LOG = getLogger(__name__)

# 読み込むCogの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.reactionchannelercog'
]

class ReacjiChannelerBot(commands.Bot):
    # MyBotのコンストラクタ。
    def __init__(self, command_prefix, intents):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix, case_insensitive=True, intents=intents)
        slash = SlashCommand(self, sync_commands=True)

        # INITIAL_EXTENSIONSに格納されている名前から、コグを読み込む。
        for cog in INITIAL_EXTENSIONS:
            self.load_extension(cog)

    async def on_ready(self):
        LOG.info('We have logged in as {0.user}'.format(self))

# ReacjiChannelerBotのインスタンス化および起動処理。
if __name__ == '__main__':
    intents = discord.Intents.all()
    intents.typing = False
    intents.members = False # 保管用チャンネルを作成する際、オーナーを見るため必要
    intents.presences = False

    bot = ReacjiChannelerBot(command_prefix='/', intents=intents)

    # start a server
    keep_alive.keep_alive()
    bot.run(settings.DISCORD_TOKEN)