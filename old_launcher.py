"""
  ___                       _                  ______ 
 / _ \                     | |                 | ___ \
/ /_\ \_ __ __ _  ___ _ __ | |_ _   _ _ __ ___ | |_/ /
|  _  | '__/ _` |/ _ \ '_ \| __| | | | '_ ` _ \| ___ \
| | | | | | (_| |  __/ | | | |_| |_| | | | | | | |_/ /
\_| |_/_|  \__, |\___|_| |_|\__|\__,_|_| |_| |_\____/ 
            __/ |                                     
           |___/

           Released on "11. 19. 2023."
"""

# Code by Dizzt#0116
Version = "Nightly 144"
Update_Date = "Mar 15, 2021"



####### 0. Modules #######

# 0.1. Discord.py
import discord
from discord import ext
from discord.ext import commands
from discord.ext import tasks
import asyncio

# 0.2. Dir. Manager
import os
import json

# 0.3. Url Manager
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import warnings
import requests

# 0.4. Dynamic Images + Buffer
from PIL import Image, ImageDraw, ImageFont
import io

#0.5. CSV.
import csv

# 0.6. ect.
import unicodedata
import random
from time import sleep
from operator import itemgetter
import datetime
import yatch as y
import yaml
from papagoRequestClass import dataProcessStream



####### 1. Config #######

with open('config.yml') as f:
    keys = yaml.load(f, Loader=yaml.FullLoader)

# 1.1. Discord Bot Token
token = str(open("./config/token.txt","r+").read())

# 1.2. Prefix
prefix = str(open("./config/prefix.txt","r+").read())

# 1.3. Discord Bot State Text
game_mes = "Made by Dizztwo#2468 | {} | {} | Type '{}help' for help".format(Version, Update_Date, prefix)

# 1.4. Naver Open API application ID
client_id = keys['Keys']['client_id']

# 1.5. Naver Open API application token
client_secret = keys['Keys']['client_secret']

# 1.6. stream Instane
streamInstance = dataProcessStream(client_id,client_secret)



####### 2.Funtions #######

# 2.1. Data R/W

# 2.1.1. Create Data Dir.
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
createFolder('./data')
createFolder('./coin')

# 2.1.2 Read Data
def dataRead(user_id):
    file = open("./data/" + str(user_id) + ".txt","r+")
    if file != None:
        return file.read()
    else:
        return "0"
    file.close()

def dataWrite(user_id, value):
    file = open("./data/" + str(user_id) + ".txt","w+")
    if file == None:
        file.write("0")
    file.write(value)
    file.close()

def coinRead(user_id):
    file = open("./coin/" + str(user_id) + ".txt","r+")
    if file != None:
        return file.read()
    else:
        return "0"
    file.close()

def coinWrite(user_id, value):
    file = open("./coin/" + str(user_id) + ".txt","w+")
    if file == None:
        file.write("0")
    file.write(value)
    file.close()



# 2.2. Level System

# 2.2.1 Constants
final_lv = 200

# 2.2.2. XP Sheet Array
def xpList():
    file = open("./config/xp.txt","r")
    arr = []
    line = file.readline()
    arr.append(line.rstrip('\n'))
    while line:
        try:
            line = file.readline().rstrip('\n')
            arr.append(int(line))
        except:
            break
    file.close()
    return arr

xp_arr = xpList()
max_xp = xp_arr[final_lv-1]

# 2.2.3 Integer Level
def level(exp):
    if exp > max_xp:
        return final_lv
    else:
        i = 1
        while(1):
            if exp < xp_arr[i]:
                break
            else:
                i += 1
        return i

# 2.2.4. Required XP
def need_exp(i):
    return int(xp_arr[i])

# 2.2.5. Level Up (Boolean)
def level_up(temp, pres):
    if temp > final_lv:
        return False
    else:
        if need_exp(temp) < pres:
            return True
        else:
            return False

# 2.2.6. Processbar (Currently Unused)
def process_bar(ratio):

    xpBar = ["<:bar0:802500348018163753>","<:bar1:802500348324347924>","<:bar2:802500348030746636>","<:bar3:802500348227878913>","<:bar4:802500348463153152>","<:bar5:802500348584525874>","<:bar6:802500348434055208>","<:bar7:802500348111224833>","<:bar8:802500348458696724>","<:bar9:802500348472197130>","<:bar10:802500348492120104>"]

    cons = int((ratio*100)//10)
    detail = int((ratio*100)%10)
    str_process = "<:barleft:802500348441788437>" + xpBar[10] * cons + xpBar[detail] + xpBar[0] * (9 - cons) + "<:barright:802500348164964373>"
    return str_process

# 2.2.7. Xp Limit
def point_range(value):
    if value < 2000:
        return value
    else:
        return 2000

# 2.2.8. Save Rankings
def rankList():

    path = "./data"
    file_list = os.listdir(path)

    rank_list = []

    for a in file_list:
        user_id = int(a.split(".txt")[0])
        rank_list.append(user_id)

    return rank_list

#2.9. others

def dt(i):
    dice = ['0', '<:d1:1085510731669180456>', '<:d2:1085510735527944223>', '<:d3:1085510738057121839>', '<:d4:1085510742146560130>', '<:d5:1085510746143719524>', '<:d6:1085510749759221760>', '<:d7:1085510753580240976>', '<:d8:1085510757736775710>']
    return dice[i]

def dt6(i):
    dice = ['0', '<:dice1:897853296767819806>','<:dice2:897853296507752468>','<:dice3:897853296755236914>','<:dice4:897853297237569587>','<:dice5:897853296591646740>','<:dice6:897853297023664168>']
    return dice[i]

def numFont(i):
    num = ['<:n0:1085510761637482526>', '<:n1:1085510763315208252>', '<:n2:1085510766221860864>', '<:n3:1085510767895400549>', '<:n4:1085510771087265802>', '<:n5:1085510773016633444>', '<:n6:1085510776867000380>', '<:n7:1085510779954012231>', '<:n8:1085510783116513340>', '<:n9:1085510786564247644>']
    result = ''
    for c in str(i):
        result += num[int(c)]
    return result

def iv(i):
    if i == -1:
        return ":black_large_square:"
    else:
        return ":white_check_mark:"

def iv2(i):
    if i < 63:
        return ":black_large_square:"
    else:
        return ":white_check_mark:"



####### 3. Discord Bot Client #######

# 3.1. Create Discord Client

intents = discord.Intents.all()

client = commands.Bot(command_prefix=prefix, intents = intents)

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game_mes))
    print("New log in as {0.user}".format(client))

# 3.2. Message Event
@client.event

async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)

# 3.2.1. XP System

    xp_gain = int(len(message.content)*0.25+10)
    coin_gain = int(1+len(message.content)*0.05)
    
    try:
        temp_lv = level(int(dataRead(message.author.id)))
        dataWrite(message.author.id, str(int(dataRead(message.author.id)) + xp_gain))
        coinWrite(message.author.id, str(int(coinRead(message.author.id)) + coin_gain))
        
        if level_up(temp_lv, int(dataRead(message.author.id))): 

            background_image = Image.open("./rank/up.png").convert('RGBA')
            rank_image_1 = Image.open("./rank/icon/{}.png".format(temp_lv)).convert('RGBA')
            rank_image_2 = Image.open("./rank/icon/{}.png".format(temp_lv+1)).convert('RGBA')

            AVATAR_SIZE = 64

            image = background_image.copy()
            image_width, image_height = image.size

            rank1 = rank_image_1.copy()
            rank2 = rank_image_2.copy()

            rectangle_image = Image.new('RGBA', (image_width, image_height))
            rectangle_draw = ImageDraw.Draw(rectangle_image)

            image = Image.alpha_composite(image, rectangle_image)

            draw = ImageDraw.Draw(image)

            avatar_asset = message.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)

            buffer_avatar = io.BytesIO()
            await avatar_asset.save(buffer_avatar)
            buffer_avatar.seek(0)

            avatar_image = Image.open(buffer_avatar)

            avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) #
            image.paste(avatar_image, (28, 28))
            image.paste(rank1, (108, 62), mask=rank1)
            image.paste(rank2, (168, 62), mask=rank2)

            buffer_output = io.BytesIO()
            image.save(buffer_output, format='PNG')
            buffer_output.seek(0)

            await message.channel.send(file=discord.File(buffer_output, 'myimage.png'))

    except:
        dataWrite(message.author.id, str(xp_gain))
        coinWrite(message.author.id, str(int(coin_gain + 5000)))


# 3.2.2. Message Contents Logs      
    print(str(message.author) + " : " + str(message.content) + " [+{}XP]".format(xp_gain))
    #print(str(message.author) + " [+{}XP]".format(xp_gain))

    if message.author == client.user:
        return

# 3.2.3. Rankcard
    if message.content.startswith(prefix+"level") or message.content.startswith(prefix+"레벨"):
        if len(message.content.split(" ")) == 1:
            obj = message.author.id
            name = message.author
        else:
            try:
                obj = (((message.content.split("!"))[1]).split(">"))[0]
                name = await client.fetch_user(obj)
            except:
                obj = None
                name = None

        sleep(2)

        v0 = int(dataRead(obj))
        lv = level(v0)

        if lv >= final_lv:
            v1 = 1
            v2 = 1
        else:
            v1 = v0 - need_exp(lv-1)
            v2 = need_exp(lv) - need_exp(lv-1)

        p1 = str(int(v1*100/v2))
        p2 = str(int((v1*10000/v2)%100))
        pc = p1 + "." + ("0"*(2-len(p2))) + p2 + "%"

        if lv > 120:
            background_image = Image.open("./rank/temp121.png").convert('RGBA')
        else:
            background_image = Image.open("./rank/temp.png").convert('RGBA')
        rank_image = Image.open("./rank/icon/{}.png".format(lv)).convert('RGBA')

        AVATAR_SIZE = 64

        #duplicate image
        image = background_image.copy()
        image_width, image_height = image.size
        rank = rank_image.copy()
        rank_width, rank_height = rank.size

        #draw on image
        rect_x0 = 28.8
        rect_y0 = 101

        rect_x1 = 28.8 + 326.4 * round(v1/v2, 2)
        rect_y1 = 115

        rectangle_image = Image.new('RGBA', (image_width, image_height))
        rectangle_draw = ImageDraw.Draw(rectangle_image)

        rectangle_draw.rectangle((rect_x0, rect_y0, rect_x1, rect_y1), fill=(0,255,255,191))

        # put rectangle on original image
        image = Image.alpha_composite(image, rectangle_image)

        # create object for drawing
        draw = ImageDraw.Draw(image)

        # draw text in center
        text1 = str(name)
        text2 = "Balance: {} h".format(format(int(coinRead(obj)), ','))
        text2.encode("utf-8")
        text3 = "Total XP : {}".format(format(v0, ','))
        text4 = "{} / {} ({})".format(v1, v2, pc)
        
        #font1 = ImageFont.truetype("./font/Cafe24Ohsquare.ttf", 20)
        #font2 = ImageFont.truetype("./font/Cafe24Ohsquareair.ttf", 12)

        font1 = ImageFont.truetype("./font/hs.ttf", 20)
        font2 = ImageFont.truetype("./font/hs.ttf", 12)

        tw1, th1 = draw.textsize(text1, font=font1)
        tw1, th1 = draw.textsize(text1, font=font2)
        tw3, th3 = draw.textsize(text3, font=font2)
        tw4, th4 = draw.textsize(text4, font=font2)
        
        x1 = 132
        y1 = 20+(36 - th1)//2

        x2 = 102
        y2 = 66

        x3 = 102
        y3 = 81

        x4 = (384 - tw4)//2
        y4 = 103

        draw.text((x1, y1), text1, fill=(255,255,255,255), font=font1)
        draw.text((x2, y2), text2, fill=(255,255,255,255), font=font2)
        draw.text((x3, y3), text3, fill=(255,255,255,255), font=font2)
        draw.text((x4, y4), text4, fill=(0,0,0,255), font=font2)

        #avatar
        avatar_asset = name.avatar.with_size(64)

        # read JPG from server to buffer (file-like object)
        buffer_avatar = io.BytesIO()
        await avatar_asset.save(buffer_avatar)
        buffer_avatar.seek(0)

        # read JPG from buffer to Image
        avatar_image = Image.open(buffer_avatar)

        # resize it
        avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE))
        image.paste(avatar_image, (28, 28))
        image.paste(rank, (98, 26), mask=rank)

        #sending image
        buffer_output = io.BytesIO()
        image.save(buffer_output, format='PNG')
        buffer_output.seek(0)

        await message.channel.send(file=discord.File(buffer_output, 'myimage.png'))

    await client.process_commands(message)

    def sendmsg(resultPackage) -> discord.Embed:
        if resultPackage['status']["code"] < 300:
            embed = discord.Embed(title=f"Translate | {resultPackage['data']['ntl']['name']} -> {resultPackage['data']['tl']['name']}",description="", color=0x5CD1E5)
            embed.add_field(name=f"{resultPackage['data']['ntl']['name']} to translate", value=resultPackage['data']['ntl']['text'],inline=False)
            embed.add_field(name=f"Translated {resultPackage['data']['tl']['name']}", value=resultPackage['data']['tl']['text'],inline=False)
            embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
            embed.set_footer(text="Service provided by Hoplin. API provided by Naver Open API",icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            return embed
        else:
            embed = discord.Embed(title="Error Code", description=resultPackage['status']['code'],color=0x5CD1E5)
            return embed

# 3.2.4. 번역기
    #To user who sent message
    # await message.author.send(msg)
    
    print(message.content)
    if message.author == client.user:
        return

#3.2.4.1. 한영번역
    if message.content.startswith(prefix+"ke"):
        #띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                resultPackage = streamInstance.returnQuery(trsText)
                embedInstance = sendmsg(resultPackage)
                await message.channel.send("Translate complete", embed=embedInstance)
        except HTTPError as e:
            await message.channel.send(f"Translate Failed. HTTPError Occured : {e}")

#3.2.4.2. 영한번역
    if message.content.startswith(prefix+"ek"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                resultPackage = streamInstance.returnQuery(trsText)
                embedInstance = sendmsg(resultPackage)
                await message.channel.send("Translate complete", embed=embedInstance)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

#3.2.4.3. 영중번역
    if message.content.startswith(prefix+"!한일번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                resultPackage = streamInstance.returnQuery(trsText)
                embedInstance = sendmsg(resultPackage)
                await message.channel.send("Translate complete", embed=embedInstance)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

#3.2.4.4. 중영번역
    if message.content.startswith(prefix+"!일한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                resultPackage = streamInstance.returnQuery(trsText)
                embedInstance = sendmsg(resultPackage)
                await message.channel.send("Translate complete", embed=embedInstance)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

#3.2.4.5. 한중번역
    if message.content.startswith(prefix+"kc"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                resultPackage = streamInstance.returnQuery(trsText)
                embedInstance = sendmsg(resultPackage)
                await message.channel.send("Translate complete", embed=embedInstance)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

#3.2.4.6. 중한번역
    if message.content.startswith(prefix+"ck"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                resultPackage = streamInstance.returnQuery(trsText)
                embedInstance = sendmsg(resultPackage)
                await message.channel.send("Translate complete", embed=embedInstance)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")


    
# 3.3. Commands

# 3.3.1. Test Commands + Essentials
@client.command()
async def test(ctx, arg):
    await ctx.channel.send(arg)

@client.command(aliases = ['제작자'])
async def credits(ctx):
    embed = discord.Embed(title=":small_orange_diamond:**Credits**", description="`People who helped with code writing, graphic design, beta testing, and error correction!!`", color=0xffff72)
    embed.add_field(name="Director", value="**`Dizztwo`**`#2468` Overall code writing and graphic design", inline=False)
    embed.add_field(name="Programming", value="**`OperaSeria`**`#9602`\n**`me the newb`**`#4049`\n**`Silverly`**`#0956`\n**`Mono`**`#1150`", inline=False)
    embed.add_field(name="Testers", value="**`와규`**`#1518`\n**`SOF`**`#1021`\n**`히로프`**`#0768`\n**`Doheeeee`**`#0388`\n**`Coral_Whale`**`#4555`", inline=False)
    embed.add_field(name="Special Thanks", value="**`NTG`**`#3163`\n**`HighStrike!!`**`#4351`\n**`Logi`**`#4916`", inline=False)
    await ctx.send(embed=embed)

# 3.3.2. Dice
@client.command(aliases = ['주사위', '랜덤', 'random'])
async def dice(ctx, i=6, lan="kor"):
    if int(i) >= 1 and int(i) <= 65536:
        dice = random.randrange(1, int(i))

        if(lan == "kor"):
            await ctx.channel.send("1부터 {}까지 자연수중 내가 고른 수는 **{}**!".format(i, numfont(dice, 7)))
        elif(lan == "eng"):
            await ctx.channel.send("The number I chose from 1 to {} is **{}**!".format(i, numfont(dice, 7)))
        else:
            await ctx.channel.send(":x: 잘못된 언어를 지정하였습니다.\nInvalid language specified.\n`CTX : dice <int=6:2~65536> <lan=kor:kor, end>`")
    else:
        await ctx.channel.send(":x: 범위에서 벗어난 정수를 입력하였습니다.\nYou have entered an integer out of range.\n`CTX : dice <int=6:2~65536> <lan=kor:kor, end>`")

# 3.3.3. Level Viewer

# 3.3.3.1. Level Icon Viewer
@client.command(aliases = ['아이콘'], pass_context=True, case_insensitive=False)
async def icon(ctx, lv = None):
    user_lv = level(int(dataRead(ctx.author.id)))
    if lv == None:
        lv = user_lv
    try:
        if int(lv) <= 200 and int(lv) > 0:
            icon = "./rank/big/{}.png".format(lv)
            await ctx.channel.send(file=discord.File(icon))
        else:
            await ctx.channel.send(":x: 범위에서 벗어난 정수를 입력하였습니다. 1~200 의 자연수를 입력받을 수 있습니다.\nYou entered an integer out of range. You can enter a natural number from 1 to 200.\n`CTX : icon <int: 1~200>`")
    except:
        await ctx.channel.send(":x: 타입오류!\nType Error!\n")

# 3.3.3.2. XP Editing
@client.command(aliases = ['경험치'], pass_context=True, case_insensitive=False)
async def xp(ctx, obj="all", amount = 0):
    if (obj == "all" or obj == "전체") and ctx.author.id == 262517377575550977:
        print("전체가 받을 경험치 : ", amount)
        for user_id in rankList():
            dataWrite(user_id, str(int(dataRead(user_id)) + amount))
            print(user_id, "는 성공적으로 경험치를 받았습니다!")

    elif ctx.author.id == 262517377575550977:
        obj = (obj.split("!")[1]).split(">")[0]
        user = await client.fetch_user(obj)
        dataWrite(obj, str(int(dataRead(obj)) + amount))
        await ctx.send("**{}**(은)는 성공적으로 **{}**의 경험치를 받았습니다!".format(user, amount))

# 3.3.3.3. Coin Editing
@client.command(aliases = ['코인'], pass_context=True, case_insensitive=False)
async def coin(ctx, obj="all", amount = 0):
    if (obj == "all" or obj == "전체") and ctx.author.id == 262517377575550977:
        print("전체가 받을 코인 : ", amount)
        for user_id in rankList():
            coinWrite(user_id, str(int(coinRead(user_id)) + amount))
            print(user_id, "는 성공적으로 코인 받았습니다!")

    elif ctx.author.id == 262517377575550977:
        obj = (obj.split("!")[1]).split(">")[0]
        user = await client.fetch_user(obj)
        coinWrite(obj, str(int(coinRead(obj)) + amount))
        await ctx.send("**{}**(은)는 성공적으로 **{}ℏ**를 받았습니다!".format(user, amount))

#야추 자극 명령어
@client.command(aliases = ['야추켜라'], pass_context=True, case_insensitive=False)
async def yachtgogo(ctx, user, count=1):
    for i in range(count):
        await ctx.send(user+" 빨리 야추 켜라")
        sleep(1)

# 3.3.4. Yatch
@client.command(aliases = ['야추'], pass_context=True, case_insensitive=False)
async def yatch(ctx, betting, id2 = None, id3 = None, id4 = None, id5 = None, id6 = None, id7 = None, id8 = None):
    player = []
    moneylist = []
    names = []
    player.append(ctx.author.id)
    final = []

    if id2 != None:
        try:
            player.append(id2[2:][:-1])
        except:
            pass

    if id3 != None:
        try:
            player.append(id3[2:][:-1])
        except:
            pass

    if id4 != None:
        try:
            player.append(id4[2:][:-1])
        except:
            pass
    
    if id5 != None:
        try:
            player.append(id5[2:][:-1])
        except:
            pass

    if id6 != None:
        try:
            player.append(id6[2:][:-1])
        except:
            pass

    if id7 != None:
        try:
            player.append(id7[2:][:-1])
        except:
            pass
    
    if id8 != None:
        try:
            player.append(id8[2:][:-1])
        except:
            pass
        
    embed1 = discord.Embed(title="**야추 다이스 참가자 목록**", description="`인원수: {} / 8`".format(len(player)), color=0x009900)
    for p in player:
        user = await client.fetch_user(p)
        moneylist.append(int(coinRead(p)))
        names.append(user)
        embed1.add_field(name="**{}** (Lv. {})".format(user, level(int(dataRead(p)))), value="`자본` **{}** ℏ".format(format(int(coinRead(p)), ',')), inline=False)

    await ctx.send(":green_circle: **게이ㅁ 이 준비되었습니다!**")
    await ctx.send(embed=embed1)
    
    if int(betting) < 0:
        betting = "0"
        await ctx.send("**`Warning`** 베팅금액이 0원보다 적어 **0원**으로 변경되었습니다!")

    elif int(betting) > min(moneylist):
        betting = str(min(moneylist))
        await ctx.send("**`Warning`** 베팅금액이 **{}원**으로 변경되었습니다!".format(format(min(moneylist),',')))

    await ctx.send("**5초후에 수금이  시작됩니다!**")
    sleep(5)

    for p in player:
        coinWrite(p, str(int(coinRead(p)) - int(betting)))
        
    await ctx.send("인당 **{}ℏ**가 베팅되었습니다. 잠시후 게임이 시작됩니다!".format(format(int(betting), ',')))
    sleep(3)

    for r in range(17):
        embed2 = discord.Embed(title="**Yatch Gayme**", description="`라운드: {} / 17`".format(r+1), color=0x009900)

        for i in range(len(player)):
            embed2.add_field(name="**{}** (Lv. {})".format(names[i], level(int(dataRead(player[i])))), value=numFont(y.scoreCalc(y.dataArray(i+1), 0)), inline=False)

        await ctx.send(embed=embed2)
        
        for p in range(len(player)):
            sleep(3)
            user = await client.fetch_user(player[p])
            await ctx.send(":green_circle: **{}**의 차례입니다! 첫 주사위는 자동으로 굴러갑니다!".format(user))

            temp2 = y.dataArray(p+1)
            totals = y.scoreCalc(temp2, 0)
            bonuss = y.scoreCalc(temp2, 1)
            
            embed = discord.Embed(title="**{}의 점수**".format(user), description="`라운드: {} / 17`".format(r+1), color=0xff0000)
            embed.add_field(name="Upper Section", value="`1` Ones {} {}\n`2` Twos {} {}\n`3` Threes {} {}\n`4` Fours {} {}\n`5` Fives {} {}\n`6` Sixes {} {}\n `7` Sevens {} {}\n `8` Eights {} {}\n`Sp` Above 84 (+55p) `{}/84` {}".format(iv(temp2[0]), temp2[0], iv(temp2[1]), temp2[1], iv(temp2[2]),temp2[2], iv(temp2[3]),temp2[3], iv(temp2[4]),temp2[4], iv(temp2[5]),temp2[5], iv(temp2[6]),temp2[6], iv(temp2[7]),temp2[7], bonuss, iv2(bonuss)), inline=False)
            embed.add_field(name="Lower Section", value="`9` 3 Kinds {} {}\n`10` 4 Kinds {} {}\n`11` Full House (+32p) {} {}\n`12` S-Straight (+26p) {} {}\n`13` L-Straight (+39p) {} {}\n`14` Unique {} {}\n`15` Chance {} {}\n`16` Royal-Straight (+55p) {} {}\n`17` Yatch (+77p) {} {}".format(iv(temp2[8]),temp2[8], iv(temp2[9]),temp2[9], iv(temp2[10]),temp2[10], iv(temp2[11]),temp2[11], iv(temp2[12]),temp2[12], iv(temp2[13]),temp2[13], iv(temp2[14]),temp2[14], iv(temp2[15]),temp2[15], iv(temp2[16]),temp2[16]), inline=False)
            embed.add_field(name="Score", value=numFont(totals)+"/600", inline=False)
            await ctx.send(embed=embed)
            
            sleep(1)
            templ = y.rollDice()
            await ctx.send("{} {} {} {} {}".format(dt(templ[0]), dt(templ[1]), dt(templ[2]), dt(templ[3]), dt(templ[4])))

            await ctx.send("**[1/2]** `{}` 다시 던질 주사위의 번호를 선택해 주세요! 제한시간 60초 있습니다! (ex> `k 1 2 4` 입력시 1, 2, 4번 주사위가 다시 던져짐)".format(user))

            def check1(m):
                return m.content.startswith('k')
            
            try:
                msg = await client.wait_for('message', timeout=60.0 , check=check1)
                keep = msg.content.split(" ")[1:]
                print(keep)
                for i in keep:
                    templ = y.rollDice(int(i))
            except:
                 await ctx.send("`{}` 60초 초과! 혹은 이상한 값 입력".format(user))
            
            await ctx.send("{} {} {} {} {}".format(dt(templ[0]), dt(templ[1]), dt(templ[2]), dt(templ[3]), dt(templ[4])))

            await ctx.send("**[2/2]** `{}` 다시 던질 주사위의 번호를 선택해 주세요! 제한시간 60초 있습니다! (ex> `k 1 2 4` 입력시 1, 2, 4번 주사위가 다시 던져짐)".format(user))

            def check1(m):
                return m.content.startswith('k')
            
            try:
                msg = await client.wait_for('message', timeout=60.0 , check=check1)
                keep = msg.content.split(" ")[1:]
                print(keep)
                for i in keep:
                    templ = y.rollDice(int(i))
            except:
                 await ctx.send("`{}` 60초 초과! 혹은 이상한 값 입력".format(user))
            
            await ctx.send("{} {} {} {} {}".format(dt(templ[0]), dt(templ[1]), dt(templ[2]), dt(templ[3]), dt(templ[4])))

            temp2 = y.dataArray(p+1)
            totals = y.scoreCalc(temp2, 0)
            bonuss = y.scoreCalc(temp2, 1)

            embed = discord.Embed(title="**{}의 점수**".format(user), description="`라운드: {} / 17`".format(r+1), color=0x009900)
            embed.add_field(name="Upper Section", value="`1` Ones {} {}\n`2` Twos {} {}\n`3` Threes {} {}\n`4` Fours {} {}\n`5` Fives {} {}\n`6` Sixes {} {}\n `7` Sevens {} {}\n `8` Eights {} {}\n`Sp` Above 84 (+55p) `{}/84` {}".format(iv(temp2[0]), temp2[0], iv(temp2[1]), temp2[1], iv(temp2[2]),temp2[2], iv(temp2[3]),temp2[3], iv(temp2[4]),temp2[4], iv(temp2[5]),temp2[5], iv(temp2[6]),temp2[6], iv(temp2[7]),temp2[7], bonuss, iv2(bonuss)), inline=False)
            embed.add_field(name="Lower Section", value="`9` 3 Kinds {} {}\n`10` 4 Kinds {} {}\n`11` Full House (+32p) {} {}\n`12` S-Straight (+26p) {} {}\n`13` L-Straight (+39p) {} {}\n`14` Unique {} {}\n`15` Chance {} {}\n`16` Royal-Straight (+55p) {} {}\n`17` Yatch (+77p) {} {}".format(iv(temp2[8]),temp2[8], iv(temp2[9]),temp2[9], iv(temp2[10]),temp2[10], iv(temp2[11]),temp2[11], iv(temp2[12]),temp2[12], iv(temp2[13]),temp2[13], iv(temp2[14]),temp2[14], iv(temp2[15]),temp2[15],iv(temp2[16]),temp2[16]), inline=False)
            embed.add_field(name="Score", value=numFont(totals)+"/600", inline=False)
            await ctx.send(embed=embed)

            while(1):
                await ctx.send("`{}` 점수를 기록할 곳의 번호를 입력해 주세요. (ex> `r 6` 입력시 6번 칸(Sixes)에 점수 기록)".format(user))

                def check1(m):
                    return m.content.startswith('r')
            
                try:
                    msg = await client.wait_for('message', timeout=60.0 , check=check1)
                    rec = int(msg.content.split(" ")[1])
                    print(rec)
                    if temp2[rec-1] == -1:
                        y.selectScore(rec, templ, y.dataArray(p+1))
                        await ctx.send("`{}` {}번에 점수가 기록 되었습니다!".format(user, rec))
                        break
                except:
                    pass

    embed3 = discord.Embed(title="**Yatch Gayme**", description="`최종 스코어`", color=0x009900)
    for i in range(len(player)):
        final.append(y.scoreCalc(y.dataArray(i+1)))
        embed3.add_field(name="**{}** (Lv. {})".format(names[i], level(int(dataRead(player[i])))), value=numFont(y.scoreCalc(y.dataArray(i+1), 0)), inline=False)
    await ctx.send(embed=embed3)
    w = final.index(max(final))
    winner = player[w]
    coinWrite(winner, str(int(coinRead(winner)) + int(0.97*len(player)*int(betting))))
    for p in player:
        dataWrite(p, str(int(dataRead(p)) + int(betting)))
    dataWrite(winner, str(int(dataRead(winner)) + int(betting)))
    y.resetScore()
    await ctx.send(":first_place:**{}** 님이 {}점으로 우승하셨습니다!\n최종상금은 **{}ℏ** 입니다! (3%는 세금)".format(names[w], numFont(max(final)), format(int(0.97*len(player)*int(betting)), ',')))
            
        

# 3.4. Run Bot
client.run(token)
