from discord.ext import commands  # Bot Commands Frameworkのインポート
from discord_slash import cog_ext, SlashContext
from discord_slash.utils import manage_commands  # Allows us to manage the command settings.    
from .modules.reactionchannel import ReactionChannel
from .modules import settings
from logging import getLogger
from discord import Webhook, AsyncWebhookAdapter

import discord
import datetime
import asyncio
import aiohttp

logger = getLogger(__name__)

# コグとして用いるクラスを定義。
class ReactionChannelerCog(commands.Cog, name="リアク字チャンネラー(Discord)"):
    """
    リアク字チャンネラー(Discord)機能
    """
    guilds = [] if settings.ENABLE_SLASH_COMMAND_GUILD_ID_LIST is None else list(map(int, settings.ENABLE_SLASH_COMMAND_GUILD_ID_LIST.split(';')))
    SPLIT_SIZE = 1900
    TIMEOUT_TIME = 30.0

    # ReactionChannelerCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.reaction_channel = None

    # cogが準備できたら読み込みする
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"load reaction-channeler's guilds{self.bot.guilds}")
        self.reaction_channel = ReactionChannel(self.bot.guilds, self.bot)

    # リアク字チャンネラー(Discord)追加
    @cog_ext.cog_slash(
    name="reacji-channeler-add",
    description='Reacji Channelerを追加する',
    options=[
        manage_commands.create_option(name='reaction',
                                    description='リアク字(リアクション/絵文字)',
                                    option_type=3,
                                    required=True)
        ,   manage_commands.create_option(name='channel',
                                    description='転送先のチャンネル、または、転送に使用するWebhook',
                                    option_type=3,
                                    required=True)
    ])
    async def add(self, ctx:SlashContext, reaction:str=None, channel:str=None):
        self.add_guild(self, ctx, reaction, channel)

    @cog_ext.cog_slash(
    name="reacji-channeler-add_guild",
    guild_ids=guilds,
    description='Reacji Channelerを追加する',
    options=[
        manage_commands.create_option(name='reaction',
                                    description='リアク字(リアクション/絵文字)',
                                    option_type=3,
                                    required=True)
        ,   manage_commands.create_option(name='channel',
                                    description='転送先のチャンネル、または、転送に使用するWebhook',
                                    option_type=3,
                                    required=True)
    ])
    async def add_guild(self, ctx:SlashContext, reaction:str=None, channel:str=None):
        """
        リアク字チャンネラー(Discord)（＊）で反応する絵文字を追加します。
        ＊指定した絵文字でリアクションされた時、チャンネルに通知する機能のこと
        """
        msg = await self.reaction_channel.add(ctx, reaction, channel)
        await ctx.send(msg)

    # リアク字チャンネラー(Discord)確認
    @cog_ext.cog_slash(
    name="reacji-channeler-list",
    description='現在登録されているReacji Channelerを確認する',
    )
    async def list(self, ctx):
        self.list_guild(self, ctx)

    @cog_ext.cog_slash(
    name="reacji-channeler-list_guild",
    guild_ids=guilds,
    description='現在登録されているReacji Channelerを確認する',
    )
    async def list_guild(self, ctx):
        """
        リアク字チャンネラー(Discord)（＊）で反応する絵文字とチャンネルのリストを表示します。
        ＊指定した絵文字でリアクションされた時、チャンネルに通知する機能のこと
        """
        msg = await self.reaction_channel.list(ctx)
        await ctx.send(msg)

    # リアク字チャンネラー(Discord)削除（１種類）
    @cog_ext.cog_slash(
    name="reacji-channeler-delete",
    guild_ids=guilds,
    description='Reacji Channelerを削除する',
    options=[
        manage_commands.create_option(name='reaction',
                                    description='リアク字(リアクション/絵文字)',
                                    option_type=3,
                                    required=True)
        ,   manage_commands.create_option(name='channel',
                                    description='転送先のチャンネル、または、転送に使用するWebhook',
                                    option_type=3,
                                    required=True)
    ])
    async def delete(self, ctx, reaction:str=None, channel:str=None):
        self.delete_guild(self, ctx, reaction, channel)

    @cog_ext.cog_slash(
    name="reacji-channeler-delete_guild",
    guild_ids=guilds,
    description='Reacji Channelerを削除する',
    options=[
        manage_commands.create_option(name='reaction',
                                    description='リアク字(リアクション/絵文字)',
                                    option_type=3,
                                    required=True)
        ,   manage_commands.create_option(name='channel',
                                    description='転送先のチャンネル、または、転送に使用するWebhook',
                                    option_type=3,
                                    required=True)
    ])
    async def delete_guild(self, ctx, reaction:str=None, channel:str=None):
        """
        リアク字チャンネラー(Discord)（＊）で反応する絵文字、チャンネルの組み合わせを削除します
        絵文字、チャンネルの記載が必須です。存在しない組み合わせを消す場合でもエラーにはなりません
        ＊指定した絵文字でリアクションされた時、チャンネルに通知する機能のこと
        """
        msg = await self.reaction_channel.delete(ctx, reaction, channel)
        await ctx.send(msg)


    # リアク字チャンネラー(Discord)コマンド群
    @commands.group(aliases=['reacji','rj','rjch'], description='リアク字チャンネラー(Discord)を操作するコマンド（サブコマンド必須）')
    async def reacjiChanneler(self, ctx):
        """
        リアク字チャンネラー(Discord)を管理するコマンド群です。このコマンドだけでは管理できません。半角スペースの後、続けて以下のサブコマンドを入力ください。
        - リアク字チャンネラー(Discord)を**全て**削除したい場合は、`purge`を入力してください。
        """
        # サブコマンドが指定されていない場合、メッセージを送信する。
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')

    # リアク字チャンネラー(Discord)全削除
    @reacjiChanneler.command(aliases=['prg','pg'], description='Guildのリアク字チャンネラー(Discord)を全削除するサブコマンド')
    async def purge(self, ctx):
        """
        リアク字チャンネラー(Discord)（＊）で反応する絵文字を全て削除します。
        30秒以内に👌(ok_hand)のリアクションをつけないと実行されませんので、素早く対応ください。
        ＊指定した絵文字でリアクションされた時、チャンネルに通知する機能のこと
        """
        command_author = ctx.author
        # 念の為、確認する
        confirm_text = f'全てのリアク字チャンネラー(Discord)を削除しますか？\n 問題ない場合、30秒以内に👌(ok_hand)のリアクションをつけてください。\nあなたのコマンド：`{ctx.message.clean_content}`'
        await ctx.message.delete()
        confirm_msg = await ctx.channel.send(confirm_text)

        def check(reaction, user):
            return user == command_author and str(reaction.emoji) == '👌'

        # リアクション待ち
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=self.TIMEOUT_TIME, check=check)
        except asyncio.TimeoutError:
            await confirm_msg.reply('→リアクションがなかったので、リアク字チャンネラー(Discord)の全削除をキャンセルしました！')
        else:
            msg = await self.reaction_channel.purge(ctx)
            await confirm_msg.reply(msg)

    # リアクション追加時に実行されるイベントハンドラを定義
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        loop = asyncio.get_event_loop()
        if payload.member.bot:# BOTアカウントは無視する
            return
        if payload.emoji.name == '👌':# ok_handは確認に使っているので無視する
            return
        await self.reaction_channeler(payload)

    # リアクションをもとにチャンネルへ投稿する非同期関数を定義
    async def reaction_channeler(self, payload: discord.RawReactionActionEvent):
        # リアク字チャンネラー(Discord)を読み込む
        guild = self.bot.get_guild(payload.guild_id)
        await self.reaction_channel.set_rc(guild)

        # リアクションから絵文字を取り出す（ギルド絵文字への変換も行う）
        emoji = payload.emoji.name
        if payload.emoji.id is not None:
            emoji = f'<:{payload.emoji.name}:{payload.emoji.id}>'

        # 入力された絵文字でフィルターされたリストを生成する
        filtered_list = [rc for rc in self.reaction_channel.guild_reaction_channels if emoji in rc]

        logger.debug(f'*****emoji***** {emoji}')

        # フィルターされたリストがある分だけ、チャンネルへ投稿する
        for reaction in filtered_list:
            from_channel = guild.get_channel(payload.channel_id)
            message = await from_channel.fetch_message(payload.message_id)

            logger.debug('guild:'+ str(guild))
            logger.debug('from_channel: '+ str(from_channel))
            logger.debug('message: ' + str(message))

            # 設定によって、すでに登録されたリアクションは無視する
            if settings.FIRST_REACTION_CHECK:
                logger.debug('reactions:'+ str(message.reactions))
                logger.debug('reactions_type_count:'+ str(len(message.reactions)))
                for message_reaction in message.reactions:
                    if emoji == str(message_reaction) and message_reaction.count > 1:
                        logger.debug('Already reaction added. emoji_count:'+ str(message_reaction.count))
                        return

            contents = [message.clean_content[i: i+1980] for i in range(0, len(message.clean_content), 1980)]
            if len(contents) == 0:
                return
            elif len(contents) > 1:
                contents[0] += ' ＊長いので分割しました＊'

            is_webhook = False
            channel = ''
            # Webhookの場合
            if reaction[2] == '':
                is_webhook = True
                channel = f'{message.guild.name} / #{message.channel.name}'
            else:
                channel = f'<#{message.channel.id}>'

            embed = discord.Embed(description = contents[0], type='rich')
            embed.set_author(name=reaction[0] + ' :reaction_channeler', url='https://github.com/tetsuya-ki/discord-reacji-channeler/')
            embed.set_thumbnail(url=message.author.avatar_url)

            created_at = message.created_at.replace(tzinfo=datetime.timezone.utc)
            created_at_jst = created_at.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

            embed.add_field(name='作成日時', value=created_at_jst.strftime('%Y/%m/%d(%a) %H:%M:%S'))
            embed.add_field(name='元のチャンネル', value=channel)

            if len(contents) != 1 :
                embed.set_footer(text=contents[1] + ' ＊長いので分割しました(以降省略)＊')

            # リアク字チャンネラー(Discord)がWebhookだった場合の処理
            if is_webhook and '※' not in reaction[1]:
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(reaction[1], adapter=AsyncWebhookAdapter(session))
                    try:
                        await webhook.send('ReactionChanneler(Webhook): ' + message.jump_url, embed=embed, username='ReactionChanneler', avatar_url=message.author.avatar_url)
                    except (discord.HTTPException,discord.NotFound,discord.Forbidden,discord.InvalidArgument) as e:
                        logger.error(e)
            elif '※' in reaction[1]:
                logger.info('環境変数に登録されていないWebhookIDをもつWebhookのため、実行されませんでした。')
            # 通常のリアク字チャンネラー(Discord)機能の実行
            else:
                to_channel = guild.get_channel(int(reaction[2]))
                logger.debug('setting:'+str(reaction[2]))
                logger.debug('to_channel: '+str(to_channel))
                await to_channel.send(reaction[1] + ': ' + message.jump_url, embed=embed)

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(ReactionChannelerCog(bot)) # ReactionChannelerCogにBotを渡してインスタンス化し、Botにコグとして登録する