import discord
from discord.ext import commands
import functions.sqlcontrol as q
import yaml
import functions.etcfunctions as etc
from datetime import datetime

with open('./config/help.yml') as f:
    helps = yaml.load(f, Loader=yaml.FullLoader)

with open('./config/config.yml') as f:
    keys = yaml.load(f, Loader=yaml.FullLoader)

Version = keys['Version']['ver']
Update_Date = keys['Version']['date']


class Essential(commands.Cog):  # Cog를 상속하는 클래스를 선언

    def __init__(self, client: commands.Bot):  # 생성자 작성
        self.client = client

    # Help [ID: 00]
    @commands.hybrid_command(name='help',
                             description="Provides help for commands.")
    #@discord.app_commands.describe(command='Command to be explained.')
    async def help(self, ctx, command: str = "main"):
        if command == "main":
            embed = discord.Embed(
                title=":notebook_with_decorative_cover: **Help Section**",
                description=
                "Type `;help <command>` for more help. eg> `;help emblem`",
                color=0x78C1F3)

            embed.add_field(name=":stars: **Essentials**",
                            value=helps[command]['Essentials'],
                            inline=True)

            embed.add_field(name=":busts_in_silhouette: **User Profile**",
                            value=helps[command]['UserProfile'],
                            inline=True)

            embed.add_field(name=":dollar: **Economy**",
                            value=helps[command]['Economy'],
                            inline=True)

            embed.add_field(name=":magic_wand: **Miscellaneous**",
                            value=helps[command]['Miscellaneous'],
                            inline=True)

            embed.add_field(name=":8ball: **Mini Games**",
                            value=helps[command]['Minigame'],
                            inline=True)

            embed.add_field(
                name="<:pokeball:1145214279134482503> **Wagyumon Server**",
                value=helps[command]['WagyumonServer'],
                inline=True)

            embed.add_field(name=":crown: **Admin Features**",
                            value=helps[command]['AdminFeatures'],
                            inline=True)

            embed.add_field(name=":tools: **Admin Debugging**",
                            value=helps[command]['AdminDebugging'],
                            inline=True)

        else:
            try:
                embed = discord.Embed(
                    title=
                    f":notebook_with_decorative_cover: **{helps[command]['title']}** `ID: {helps[command]['id']}`",
                    description=
                    f"`{keys['Bot']['prefix']}{helps[command]['ctx']}`",
                    color=0xF2D7D9)

                embed.add_field(name="**Feature Description**",
                                value=helps[command]['discript'],
                                inline=False)
                if command == 'storage' or command == 'skin':
                    embed.add_field(
                        name="**Show skin list**",
                        value=
                        "`option` list | 목록\n`value` int type, enter a value for the page to view (default: 1).",
                        inline=False)

                    embed.add_field(
                        name="**Unlock skin**",
                        value=
                        "`option` unlock | 해금\n`value` int type, enter the id value of the skin you want to unlock (default: 1).",
                        inline=False)

                    embed.add_field(
                        name="**Change equipped skin**",
                        value=
                        "`option` change | 변경\n`value` int type, enter the id value of the skin you want to change (default: 1).",
                        inline=False)
                else:
                    embed.add_field(name="**Arguments**",
                                    value=helps[command]['args'],
                                    inline=False)
                    if command == 'translate':
                        embed.add_field(
                            name="**Language Code**",
                            value=
                            "`ko` Korean, `ja` Japanese, `zh-CN` Simplified Chinese, `zh-TW` Traditional Chinese, `hi` Hindi, `en` English, `es` Spanish, `fr` French, `de` German, `pt` Portuguese, `vi` Vietnamese, `id` Indonesian,  `fa` Persian, `ar` Arabic, `mm` Burmese, `th` Thai, `ru` Russian, `it` Italian",
                            inline=False)
            except:
                pass

        #Common Part
        embed.set_footer(text="Developed by Dizzt", icon_url="")
        await ctx.reply(
            ":green_circle: **{}**'s request completely loaded!!".format(
                q.readTag(ctx.author)),
            embed=embed)

    # Test Command [ID: 01]
    @commands.hybrid_command(name='test', description="Send test message.")
    #@discord.app_commands.describe(arg='Text Message')
    async def test(self, ctx, *, arg: str = "Hello World!"):
        await ctx.reply(arg)

    # Id Viewer [ID: 02]
    @commands.hybrid_command(
        name='myid',
        description="Show your discord user id and account creation date.")
    async def myid(self, ctx):
        uid = ctx.author.id
        udate = ctx.author.created_at.strftime("%a %#d %B %Y, %I:%M %p")
        await ctx.reply("ID: {}\nCreation date: {}".format(uid, udate))

    # Credits [ID: 03]
    @commands.hybrid_command(name='credits',
                             description="Show developers of this bot.")
    async def credits(self, ctx):
        embed = discord.Embed(
            title=":small_orange_diamond:**Credits**",
            description=
            "`People who helped with code writing, graphic design, beta testing, and error correction!!`",
            color=0xF8FDCF)
        embed.add_field(
            name="Director",
            value="**`Dizzt`** Overall code writing and graphic design",
            inline=False)
        embed.add_field(
            name="Programming",
            value="**`OperaSeria`**\n**`me the newb`**`\n**`최은비`**\n**`Mono`**",
            inline=False)
        embed.add_field(
            name="Testers",
            value=
            "**`와규`**\n**`SOF`**`\n**`히로프`**\n**`Doheeeee`**\n**`Coral_Whale`**",
            inline=False)
        embed.add_field(name="Special Thanks",
                        value="**`NTG`**\n**`HighStrike!!`**\n**`Logi`**",
                        inline=False)
        await ctx.reply(embed=embed)

    # Nickname [ID: 05]
    @commands.hybrid_command(name='nickname',
                             description="Change your nickname.")
    #@discord.app_commands.describe(name="Nickname to change")
    async def nickname(self, ctx, *, name: str = ""):
        user = ctx.author
        if name == "":
            await ctx.reply(
                "`(⩌Δ ⩌ ;)` Without a name, existence is worthless... A name is important to all dear ones..."
            )
        elif len(name) > 16:
            await ctx.reply(
                "`(⩌Δ ⩌ ;)` Nicknames are up to 16 characters long. Please choose something else..."
            )
        else:
            try:
                old = q.readTag(user)
                q.nickModify(user, name)
                new = q.readTag(user)
                await ctx.reply(
                    "`⸜(*◉ ᴗ ◉)⸝` By magic powers... your name has changed from `{}` to `{}`!"
                    .format(old, new))
            except:
                await ctx.reply("???")

    # Discrim [ID: 06]
    @commands.hybrid_command(name='discrim',
                             description="Show your discriminator.")
    async def discrim(self, ctx, option: str = 'mydiscrim'):
        user = ctx.author
        if option == 'mydiscrim':
            await ctx.reply(
                "Discriminator is an identification number randomly assigned to each user!\nYour number is **#{}**! `⸜(*◉ ᴗ ◉)⸝`"
                .format(q.readDiscrim(user)))

    # Bot Info [ID: 07]
    @commands.hybrid_command(name='argentumbot',
                             description="Bot related infomation")
    async def silver_bot(self, ctx):
        name = q.readTag(ctx.author)
        today = datetime.now()
        bday = datetime.strptime("20020801", "%Y%m%d")
        fday = datetime.strptime("20170520", "%Y%m%d")
        age = today.year - bday.year - ((today.month, today.day) <
                                        (bday.month, bday.day))

        embed = discord.Embed(
            title="Hello, I'm ArgentumBot",
            description=f"Current version: {Version} ({Update_Date})",
            color=0xCEDEBD)

        embed.set_thumbnail(url=commands.user.avatar.url)

        embed.add_field(name="NAME",
                        value="Cyborg Eunbi (aka ArgentumBot)",
                        inline=False)

        embed.add_field(name="BIRTHDAY",
                        value=f"August 1 ({age}-year-old)",
                        inline=False)

        embed.add_field(name="Start date of Operation",
                        value=f"May 20, 2017 ({(today-fday).days} days)",
                        inline=False)

        embed.set_footer(text="Developde by Dizzt", icon_url="")

        await ctx.reply(
            f":green_circle: **{name}**'s request completely loaded!!",
            embed=embed)


async def setup(client):
    await client.add_cog(Essential(client))
