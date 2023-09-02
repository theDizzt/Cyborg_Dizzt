"""
 █████  ██████   ██████  ███████ ███    ██ ████████ ██    ██ ███    ███ 
██   ██ ██   ██ ██       ██      ████   ██    ██    ██    ██ ████  ████ 
███████ ██████  ██   ███ █████   ██ ██  ██    ██    ██    ██ ██ ████ ██ 
██   ██ ██   ██ ██    ██ ██      ██  ██ ██    ██    ██    ██ ██  ██  ██ 
██   ██ ██   ██  ██████  ███████ ██   ████    ██     ██████  ██      ██ 

           Code by 혜성(dizzt, Dizzt#0116)
           Start of Development: May 20, 2017
"""

####### 0. Modules #######

# 0.1. Discord.py
import discord
from discord.ext import commands
import asyncio

# 0.2. Fuctions
from functions.keep_alive import keep_alive
import functions.sqlcontrol as q
import functions.etcfunctions as etc
import functions.koreanbreak as kb

# 0.2. Dir. Manager
import os
"""
# 0.3. Url Manager
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
from urllib.parse import quote
import re
import warnings
import requests
import hgtk
"""

# 0.3. Dynamic Images + Buffer
from PIL import Image, ImageDraw, ImageFont
import io

# 0.4. ect.
import random as r  #난수 생성
import math as m
import time as t
from time import sleep
import datetime
import yaml
from tqdm import tqdm

####### 1. Config #######

# 1.0. Open Config & Admin file

with open('./config/config.yml') as f:
    keys = yaml.load(f, Loader=yaml.FullLoader)

# 1.1. Discord Bot
token = keys['Bot']['token']
prefix = keys['Bot']['prefix']
Version = keys['Version']['ver']
Update_Date = keys['Version']['date']
game_mes = f"Made by Dizzt | {Version} | {Update_Date} | Type '{prefix}help' for help"

# 1.4. Event Variables
xp_multi = 2.4

global history
apikey = '6A4B78176B66672E8D136E78D03D805A'
history = []

####### 2.Funtions #######

# 2.0. DB Init Setting
q.initSetting()

####### 3. Discord Bot Client #######

# 3.0. Create Discord Client

intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix,
                      intents=intents,
                      help_command=None,
                      sync_commands=True)

# 3.1. Discord Cogs Loading

# 3.2. Discord Bot Ready Events


@client.event  # Use these decorator to register an event.
async def on_ready(
):  # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(game_mes))
    print("New log in as {0.user}".format(client))


# 3.3. Voice Channel Event


# 3.3.1. Voice Leveling
@client.event
async def on_voice_state_update(member, before, after):

    if not before.channel and after.channel:
        voicetime = int(t.time())
        etc.voiceDelete(member)
        etc.voiceWrite(member, voicetime)
        print("{} joined voice channel! (Time: {})".format(member, voicetime))

    elif before.channel and not after.channel:

        voicetime = int(t.time()) - etc.voiceRead(member)

        xp_gain = int((voicetime * 0.25 + 3) * xp_multi)
        money_gain = int(voicetime // 20)

        try:
            q.xpAdd(member, xp_gain)
            q.moneyAdd(member, money_gain)

        except:
            q.newAccount(member)
            q.newStorage(member)
            q.xpAdd(member, xp_gain)
            q.moneyAdd(member, money_gain)

        etc.voiceDelete(member)
        print("{} left voice channel! | {}s | +{}XP | +{}$".format(
            member, voicetime, xp_gain, money_gain))


# 3.4. Message Event
@client.event
async def on_message(
        message):  # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)

    # 3.2.1. XP System
    count = kb.count_break_korean(message.content)
    xp_gain = int((count * 0.25 + 3) * xp_multi)
    money_gain = r.randint(1, 10)

    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    now_time = now.strftime('%Y/%m/%d %H:%M:%S')

    global temp_xp, temp_lv

    try:
        temp_xp = q.readXp(message.author)
        temp_lv = etc.level(temp_xp)

    except:
        q.newAccount(message.author)
        q.newStorage(message.author)
        temp_xp = 0
        temp_lv = 1

    q.xpAdd(message.author, xp_gain)
    q.moneyAdd(message.author, money_gain)

    if etc.level_up(temp_lv, temp_xp + xp_gain):

        background_image = Image.open("./config/rankcard/rankup.png").convert(
            'RGBA')
        rank_image_1 = Image.open(
            "./config/rankcard/emblem/{}.png".format(temp_lv)).convert('RGBA')
        rank_image_2 = Image.open(
            "./config/rankcard/emblem/{}.png".format(temp_lv +
                                                     1)).convert('RGBA')

        rank_image_1 = rank_image_1.resize((60, 60))
        rank_image_2 = rank_image_2.resize((60, 60))

        image = background_image.copy()
        image_width, image_height = image.size

        rank1 = rank_image_1.copy()
        rank2 = rank_image_2.copy()

        rectangle_image = Image.new('RGBA', (image_width, image_height))

        image = Image.alpha_composite(image, rectangle_image)

        draw = ImageDraw.Draw(image)

        avatar_asset = message.author.avatar

        buffer_avatar = io.BytesIO()
        await avatar_asset.save(buffer_avatar)
        buffer_avatar.seek(0)

        avatar_image = Image.open(buffer_avatar)

        avatar_image = avatar_image.resize((96, 96))
        image.paste(avatar_image, (8, 8))
        image.paste(rank1, (112, 44), mask=rank1)
        image.paste(rank2, (188, 44), mask=rank2)

        buffer_output = io.BytesIO()
        image.save(buffer_output, format='PNG')
        buffer_output.seek(0)

        await message.channel.send(
            "<@{}> 는 `레벨 {}`에 도달했습니다!\nYou reached `Level {}`!".format(
                message.author.id, temp_lv + 1, temp_lv + 1))

        await message.channel.send(
            file=discord.File(buffer_output, 'myimage.png'))

        if temp_lv + 1 == 91:
            await message.channel.send(
                "`{}`/n레벨 91 달성을 진심으로 축하드립니다! 모든 혜택을 누릴 수 있는 레벨에 도달하기 까지 많을 시간을 함께 해 주셔서 진심으로 감사합니다!/nCongratulations on achieving level 91! Thank you so much for spending a lot of time with me before you reach the level where you can enjoy all the benefits!"
                .format(message.author))

    if message.content == ";39187":
        print("Test Start")

    # 3.4.2. Message Contents Logs
    print(f"{message.author} | {now_time} | +{xp_gain}XP | +${money_gain}")
    #print(message.content)

    #지우지 말 것
    await client.process_commands(message)

    #이것도
    if message.author == client.user:
        return

    #뇌절방지
    if message.content.find("헉") != -1:
        q.xpAdd(message.author, -100)
        await message.channel.send("뇌절방지 캠패인: 경험치 100점이 차감됩니다.")

    if message.content.find("헊") != -1:
        q.xpAdd(message.author, -150)
        await message.channel.send("뇌절방지 캠패인: 경험치 150점이 차감됩니다.")

    if message.content.find("헠") != -1:
        q.xpAdd(message.author, -150)
        await message.channel.send("뇌절방지 캠패인: 경험치 150점이 차감됩니다.")

    #주원이 괴롭히기
    if message.content.startswith("주원"):
        await message.channel.send("왜 불러?", tts=True)

    if message.content.startswith("김주원"):
        await message.channel.send("왜 불러?", tts=True)

    if message.content.startswith("주웡"):
        await message.channel.send("왜 불러?", tts=True)

    if message.content.startswith("김주웡"):
        await message.channel.send("왜 불러?", tts=True)

    if message.content.startswith("곰국"):
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/526648786605441024/789690716224880640/36e3370a1834456c.png",
            tts=True)

    if message.content.startswith("논문"):
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/526648786605441024/789690716224880640/36e3370a1834456c.png",
            tts=True)

    #이스터에그!!
    if message.content == "stellaforce":

        await message.delete()
        choice = 6

        if q.readStorage(message.author, choice) == 0:
            q.storageModify(message.author, choice, 1)

    if message.content == "당근꼴등":
        choice = 20

        if q.readStorage(message.author, choice) == 0:
            q.storageModify(message.author, choice, 1)

        await message.channel.send("박당근의 골프잇 전적: 29판중 0승 29패 응~ 당근~")
        await message.channel.send("https://youtu.be/X0VGxuq9_sw?t=112")
        await message.channel.send("https://youtu.be/0mdWdL-0fZY?t=1346")
        await message.channel.send(
            "`;skin change 20`을 입력하여 특전을 확인하당근 `( ˃ ⩌˂)`")

    if message.content == "invincible eun-bi choi":
        choice = 21

        if q.readStorage(message.author, choice) == 0:
            q.storageModify(message.author, choice, 1)


# 4. Commands


# 4.1. Sync
@client.hybrid_command(name='sync',
                       description="Sync commands to the current server.")
async def sync(ctx):
    await client.tree.sync()
    await ctx.reply("`⸜(*◉ ᴗ ◉)⸝` Synced commands to the current server!")


# 3.3.10. Yatch
@client.command(aliases=['야추'], pass_context=True, case_insensitive=False)
async def yatch(ctx,
                betting: int = 0,
                user2: discord.Member = None,
                user3: discord.Member = None,
                user4: discord.Member = None,
                user5: discord.Member = None,
                user6: discord.Member = None):
    player = []
    moneylist = []
    names = []
    player.append(ctx.author.id)
    final = []

    if user2 != None:
        player.append(user2.id)

    if user3 != None:
        player.append(user3.id)

    if user4 != None:
        player.append(user4.id)

    if user5 != None:
        player.append(user5.id)

    if user6 != None:
        player.append(user6.id)

    embed1 = discord.Embed(title="**야추 다이스 참가자 목록**",
                           description="`인원수: {} / 6`".format(len(player)),
                           color=0x009900)
    for p in player:
        names.append(q.readTagById(p))
        moneylist.append(q.readMoneyById(p))
        embed1.add_field(name="**{}** (Lv. {})".format(
            q.readTagById(p), etc.level(q.readXpById(p))),
                         value="`자본` **${:,d}**".format(q.readMoneyById(p)),
                         inline=False)

    await ctx.send(":green_circle: **게이ㅁ 이 준비되었습니다!**")
    await ctx.send(embed=embed1)

    if betting < 0:
        betting = 0
        await ctx.send("**`Warning`** 베팅금액이 0원보다 적어 **0원**으로 변경되었습니다!")

    elif betting > min(moneylist):
        betting = min(moneylist)
        await ctx.send(
            "**`Warning`** 베팅금액이 **{:,d}원**으로 변경되었습니다!".format(betting))

    await ctx.send("**5초후에 수금이  시작됩니다!**")
    t.sleep(5)

    for p in player:
        q.moneyAddById(p, betting * (-1))

    await ctx.send("인당 **${:,d}**가 베팅되었습니다. 잠시후 게임이 시작됩니다!".format(betting))
    t.sleep(3)

    for rn in range(13):
        embed2 = discord.Embed(title="**Yatch Gay-me**",
                               description="`라운드: {} / 13`".format(rn + 1),
                               color=0x00ff00)

        for i in range(len(player)):
            embed2.add_field(name="**{}** (Lv. {})".format(
                names[i], etc.level(q.readXpById(player[i]))),
                             value=etc.numFont(
                                 y.scoreCalc(y.dataArray(i + 1), 0)),
                             inline=False)

        await ctx.send(embed=embed2)

        for p in range(len(player)):
            t.sleep(3)
            await ctx.send(
                ":green_circle: **{}**의 차례입니다! 첫 주사위는 자동으로 굴러갑니다!".format(
                    names[p]))

            temp2 = y.dataArray(p + 1)
            totals = y.scoreCalc(temp2, 0)
            bonuss = y.scoreCalc(temp2, 1)

            embed = discord.Embed(title="**{}의 점수**".format(names[p]),
                                  description="`라운드: {} / 13`".format(rn + 1),
                                  color=0xffff72)
            embed.add_field(
                name="Upper Section",
                value=
                "`1` Ones {} {}\n`2` Twos {} {}\n`3` Threes {} {}\n`4` Fours {} {}\n`5` Fives {} {}\n`6` Sixes {} {}\n`Sp` Above 63 (+35p) `{}/63` {}"
                .format(iv(temp2[0]), temp2[0], iv(temp2[1]), temp2[1],
                        iv(temp2[2]), temp2[2], iv(temp2[3]), temp2[3],
                        iv(temp2[4]), temp2[4], iv(temp2[5]), temp2[5], bonuss,
                        iv2(bonuss)),
                inline=False)
            embed.add_field(
                name="Lower Section",
                value=
                "`7` 3 Kinds {} {}\n`8` 4 Kinds {} {}\n`9` Full House (+25p) {} {}\n`10` S-Straight (+20p) {} {}\n`11` L-Straight (+30p) {} {}\n`12` Chance {} {}\n`13` Yatch (+50p) {} {}"
                .format(iv(temp2[6]), temp2[6], iv(temp2[7]), temp2[7],
                        iv(temp2[8]), temp2[8], iv(temp2[9]), temp2[9],
                        iv(temp2[10]), temp2[10], iv(temp2[11]), temp2[11],
                        iv(temp2[12]), temp2[12]),
                inline=False)
            embed.add_field(name="Score",
                            value=etc.numFont(totals) + "/325",
                            inline=False)
            await ctx.send(embed=embed)

            t.sleep(1)
            templ = y.rollDice()
            await ctx.send("{} {} {} {} {}".format(dt6(templ[0]),
                                                   dt6(templ[1]),
                                                   dt6(templ[2]),
                                                   dt6(templ[3]),
                                                   dt6(templ[4])))

            await ctx.send(
                "**[1/2]** `{}` 다시 던질 주사위의 번호를 선택해 주세요! 제한시간 60초 있습니다! (ex> `k 1 2 4` 입력시 1, 2, 4번 주사위가 다시 던져짐)"
                .format(names[p]))

            def check1(m):
                return m.content.startswith('k')

            try:
                msg = await client.wait_for('message',
                                            timeout=60.0,
                                            check=check1)
                keep = msg.content.split(" ")[1:]
                print(keep)
                for i in keep:
                    templ = y.rollDice(int(i))
            except:
                if msg.content.split(
                        " ")[1] == "h" and msg.author.id in admin_login:
                    keep = msg.content.split(" ")[2:]
                    for i in range(5):
                        templ[i] = int(keep[i])
                    await ctx.send("`ς(>‿<.)` 저는 항상 승자에 편에 입답니다!")
                else:
                    await ctx.send("`{}` 60초 초과! 혹은 이상한 값 입력".format(names[p]))

            await ctx.send("{} {} {} {} {}".format(dt6(templ[0]),
                                                   dt6(templ[1]),
                                                   dt6(templ[2]),
                                                   dt6(templ[3]),
                                                   dt6(templ[4])))

            await ctx.send(
                "**[2/2]** `{}` 다시 던질 주사위의 번호를 선택해 주세요! 제한시간 60초 있습니다! (ex> `k 1 2 4` 입력시 1, 2, 4번 주사위가 다시 던져짐)"
                .format(names[p]))

            def check1(ms):
                return ms.content.startswith('k')

            try:
                msg = await client.wait_for('message',
                                            timeout=60.0,
                                            check=check1)
                keep = msg.content.split(" ")[1:]
                print(keep)
                for i in keep:
                    templ = y.rollDice(int(i))
            except:
                if msg.content.split(
                        " ")[1] == "h" and msg.author.id in admin_login:
                    keep = msg.content.split(" ")[2:]
                    for i in range(5):
                        templ[i] = int(keep[i])
                    await ctx.send("`ς(>‿<.)` 저는 항상 승자에 편에 있답니다!")
                else:
                    await ctx.send("`{}` 60초 초과! 혹은 이상한 값 입력".format(names[p]))

            await ctx.send("{} {} {} {} {}".format(dt6(templ[0]),
                                                   dt6(templ[1]),
                                                   dt6(templ[2]),
                                                   dt6(templ[3]),
                                                   dt6(templ[4])))

            temp2 = y.dataArray(p + 1)
            totals = y.scoreCalc(temp2, 0)
            bonuss = y.scoreCalc(temp2, 1)

            embed = discord.Embed(title="**{}의 점수**".format(names[p]),
                                  description="`라운드: {} / 13`".format(rn + 1),
                                  color=0x009900)
            embed.add_field(
                name="Upper Section",
                value=
                "`1` Ones {} {}\n`2` Twos {} {}\n`3` Threes {} {}\n`4` Fours {} {}\n`5` Fives {} {}\n`6` Sixes {} {}\n`Sp` Above 63 (+35p) `{}/63` {}"
                .format(iv(temp2[0]), temp2[0], iv(temp2[1]), temp2[1],
                        iv(temp2[2]), temp2[2], iv(temp2[3]), temp2[3],
                        iv(temp2[4]), temp2[4], iv(temp2[5]), temp2[5], bonuss,
                        iv2(bonuss)),
                inline=False)
            embed.add_field(
                name="Lower Section",
                value=
                "`7` 3 Kinds {} {}\n`8` 4 Kinds {} {}\n`9` Full House (+25p) {} {}\n`10` S-Straight (+20p) {} {}\n`11` L-Straight (+30p) {} {}\n`12` Chance {} {}\n`13` Yatch (+50p) {} {}"
                .format(iv(temp2[6]), temp2[6], iv(temp2[7]), temp2[7],
                        iv(temp2[8]), temp2[8], iv(temp2[9]), temp2[9],
                        iv(temp2[10]), temp2[10], iv(temp2[11]), temp2[11],
                        iv(temp2[12]), temp2[12]),
                inline=False)
            embed.add_field(name="Score",
                            value=etc.numFont(totals) + "/325",
                            inline=False)
            await ctx.send(embed=embed)

            while (1):
                await ctx.send(
                    "`{}` 점수를 기록할 곳의 번호를 입력해 주세요. (ex> `r 6` 입력시 6번 칸(Sixes)에 점수 기록)"
                    .format(names[p]))

                def check1(m):
                    return m.content.startswith('r')

                try:
                    msg = await client.wait_for('message',
                                                timeout=60.0,
                                                check=check1)
                    rec = int(msg.content.split(" ")[1])
                    print(rec)
                    if temp2[rec - 1] == -1:
                        y.selectScore(rec, templ, y.dataArray(p + 1))
                        await ctx.send("`{}` {}번에 점수가 기록 되었습니다!".format(
                            names[p], rec))
                        break
                except:
                    pass

    embed3 = discord.Embed(title="**Yatch Gay-me**",
                           description="`최종 스코어`",
                           color=0x00ff00)

    for i in range(len(player)):
        final.append(y.scoreCalc(y.dataArray(i + 1)))
        embed3.add_field(name="**{}** (Lv. {})".format(
            names[i], x.level(q.readXpById(player[i]))),
                         value=etc.numFont(y.scoreCalc(y.dataArray(i + 1), 0)),
                         inline=False)

    await ctx.send(embed=embed3)
    w = final.index(max(final))
    winner = player[w]
    prize = int(0.97 * len(player) * betting)
    q.moneyAddById(winner, prize)
    for i in range(len(player)):
        q.xpAddById(player[i], 10 * final[i])
    q.xpAddById(winner, 1500)
    y.resetScore()
    await ctx.send(
        ":first_place:**{}** 님이 {}점으로 우승하셨습니다!\n최종상금은 **${}** 입니다! (3%는 세금)".
        format(names[w], etc.numFont(max(final)),
               format(int(0.97 * len(player) * betting), ',')))


async def load_extensions():
    # cogs 폴더의 절대 경로 얻기
    # Pycharm에서 바로 상대 경로를 사용하면 오류가 발생하기 때문에 따로 절대경로를 얻어야한다.
    cogs_path = 'cogs'
    abs_cogs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 cogs_path)

    # cogs 폴더에 존재하는 cogs(.py파일) 로드
    for c in tqdm(os.listdir(abs_cogs_path)):
        if c.endswith(".py"):
            await client.load_extension(f"cogs.{c.split('.')[0]}"
                                        )  # .py 부분을 떼고 cog의 이름만 추출


async def main():
    async with client:
        await load_extensions()
        await client.start(token)


keep_alive()
asyncio.run(main())
