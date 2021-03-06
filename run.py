"""
  ___                       _                  ______ 
 / _ \                     | |                 | ___ \
/ /_\ \_ __ __ _  ___ _ __ | |_ _   _ _ __ ___ | |_/ /
|  _  | '__/ _` |/ _ \ '_ \| __| | | | '_ ` _ \| ___ \
| | | | | | (_| |  __/ | | | |_| |_| | | | | | | |_/ /
\_| |_/_|  \__, |\___|_| |_|\__|\__,_|_| |_| |_\____/ 
            __/ |                                     
           |___/

           Released on "November 19th, 2020"
"""

# Code by Dizzt#2468
Version = "Nightly 125"
Update_Date = "Oct 19, 2021"



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



####### 1. Config #######

# 1.1. Discord Bot Token
token = str(open("./config/token.txt","r+").read())

# 1.2. Prefix
prefix = str(open("./config/prefix.txt","r+").read())

# 1.3. Discord Bot State Text
game_mes = "Made by Dizztwo#2468 | {} | {} | Type '{}help' for help".format(Version, Update_Date, prefix)



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
        user_id = int(((a.split("data"))[1]).split(".txt")[0])
        rank_list.append(user_id)

    return rank_list

#2.9. others
def dt(i):
    dice = ['0', '<:dice1:897853296767819806>','<:dice2:897853296507752468>','<:dice3:897853296755236914>','<:dice4:897853297237569587>','<:dice5:897853296591646740>','<:dice6:897853297023664168>']
    return dice[i]

def numFont(i):
    num = ['<:0_:698008154541391955>', '<:1_:698008154822410311>', '<:2_:698008155157954561>', '<:3_:698008155292041306>', '<:4_:698008155661139989>', '<:5_:698008154943914076>', '<:6_:698008155308687361>', '<:7_:698008155371601962>', '<:8_:698008155308818453>', '<:9_:698008155396898867>']
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

client = commands.Bot(command_prefix=[prefix], case_insensitive=False)

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

    xp_gain = int(len(message.content)*0.3+7)
    coin_gain = int(1+len(message.content)*0.07)
    
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
    if message.content.startswith(prefix+"level") or message.content.startswith(prefix+"??????"):
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
        avatar_asset = name.avatar_url_as(format='jpg', size=AVATAR_SIZE)

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


    
# 3.3. Commands

# 3.3.1. Test Commands
@client.command()
async def test(ctx, arg):
    await ctx.channel.send(arg)

# 3.3.2. Dice
@client.command(aliases = ['?????????', '??????', 'random'])
async def dice(ctx, i=6, lan="kor"):
    if int(i) >= 1 and int(i) <= 65536:
        dice = random.randrange(1, int(i))

        if(lan == "kor"):
            await ctx.channel.send("1?????? {}?????? ???????????? ?????? ?????? ?????? **{}**!".format(i, numfont(dice, 7)))
        elif(lan == "eng"):
            await ctx.channel.send("The number I chose from 1 to {} is **{}**!".format(i, numfont(dice, 7)))
        else:
            await ctx.channel.send(":x: ????????? ????????? ?????????????????????.\nInvalid language specified.\n`CTX : dice <int=6:2~65536> <lan=kor:kor, end>`")
    else:
        await ctx.channel.send(":x: ???????????? ????????? ????????? ?????????????????????.\nYou have entered an integer out of range.\n`CTX : dice <int=6:2~65536> <lan=kor:kor, end>`")

# 3.3.3. Level Viewer

# 3.3.3.1. Level Icon Viewer
@client.command(aliases = ['?????????'], pass_context=True, case_insensitive=False)
async def icon(ctx, lv = None):
    user_lv = level(int(dataRead(ctx.author.id)))
    if lv == None:
        lv = user_lv
    try:
        if (int(lv) <= 120 or int(lv) <= user_lv) and int(lv) > 0:
            icon = "./rank/big/{}.png".format(lv)
            await ctx.channel.send(file=discord.File(icon))
        else:
            await ctx.channel.send(":x: ???????????? ????????? ????????? ?????????????????????. 1~150 ??? ???????????? ???????????? ??? ?????????, Level 120 ????????? ????????? ????????? ???????????? ????????? ????????? ????????? ???????????????.\nYou entered an integer out of range. You can enter a natural number from 1 to 150, and after Level 120, you can view only the icons corresponding to your level.\n`CTX : icon <int>`")
    except:
        await ctx.channel.send(":x: ????????????!\nType Error!\n`CTX : icon <int=(your_level):1 ~ 800+{(your_level)-800}*{(your_level)//800}>`")

# 3.3.3.2. XP Editing
@client.command(aliases = ['?????????'], pass_context=True, case_insensitive=False)
async def xp(ctx, obj="all", amount = 0):
    if (obj == "all" or obj == "??????") and ctx.author.id == 262517377575550977:
        print("????????? ?????? ????????? : ", amount)
        for user_id in rankList():
            dataWrite(user_id, str(int(dataRead(user_id)) + amount))
            print(user_id, "??? ??????????????? ???????????? ???????????????!")

    elif ctx.author.id == 262517377575550977:
        obj = (obj.split("!")[1]).split(">")[0]
        user = await client.fetch_user(obj)
        dataWrite(obj, str(int(dataRead(obj)) + amount))
        await ctx.send("**{}**(???)??? ??????????????? **{}**??? ???????????? ???????????????!".format(user, amount))

# 3.3.3.3. Coin Editing
@client.command(aliases = ['??????'], pass_context=True, case_insensitive=False)
async def coin(ctx, obj="all", amount = 0):
    if (obj == "all" or obj == "??????") and ctx.author.id == 262517377575550977:
        print("????????? ?????? ?????? : ", amount)
        for user_id in rankList():
            coinWrite(user_id, str(int(coinRead(user_id)) + amount))
            print(user_id, "??? ??????????????? ?????? ???????????????!")

    elif ctx.author.id == 262517377575550977:
        obj = (obj.split("!")[1]).split(">")[0]
        user = await client.fetch_user(obj)
        coinWrite(obj, str(int(coinRead(obj)) + amount))
        await ctx.send("**{}**(???)??? ??????????????? **{}???**??? ???????????????!".format(user, amount))

# 3.3.4. Yatch
@client.command(aliases = ['??????'], pass_context=True, case_insensitive=False)
async def yatch(ctx, betting, id2 = None, id3 = None, id4 = None):
    player = []
    moneylist = []
    names = []
    player.append(ctx.author.id)
    final = []

    if id2 != None:
        try:
            player.append((((id2.split("!"))[1]).split(">"))[0])
        except:
            pass

    if id3 != None:
        try:
            player.append((((id3.split("!"))[1]).split(">"))[0])
        except:
            pass

    if id4 != None:
        try:
            player.append((((id4.split("!"))[1]).split(">"))[0])
        except:
            pass
        
    embed1 = discord.Embed(title="**?????? ????????? ????????? ??????**", description="`?????????: {} / 4`".format(len(player)), color=0x009900)
    for p in player:
        user = await client.fetch_user(p)
        moneylist.append(int(coinRead(p)))
        names.append(user)
        embed1.add_field(name="**{}** (Lv. {})".format(user, level(int(dataRead(p)))), value="`??????` **{}** ???".format(format(int(coinRead(p)), ',')), inline=False)


    await ctx.send(":green_circle: **????????? ??? ?????????????????????!**")
    await ctx.send(embed=embed1)
    
    if int(betting) < 0:
        betting = "0"
        await ctx.send("**`Warning`** ??????????????? 0????????? ?????? **0???**?????? ?????????????????????!")
    elif int(betting) > min(moneylist):
        betting = str(min(moneylist))
        await ctx.send("**`Warning`** ??????????????? **{}???**?????? ?????????????????????!".format(format(min(moneylist),',')))

    await ctx.send("**5????????? ?????????  ???????????????!**")
    sleep(5)

    for p in player:
        coinWrite(p, str(int(coinRead(p)) - int(betting)))
        
    await ctx.send("?????? **{}???**??? ?????????????????????. ????????? ????????? ???????????????!".format(format(int(betting), ',')))
    sleep(3)

    for r in range(13):
        embed2 = discord.Embed(title="**Yatch Gayme**", description="`?????????: {} / 13`".format(r+1), color=0x009900)
        for i in range(len(player)):
            embed2.add_field(name="**{}** (Lv. {})".format(names[i], level(int(dataRead(player[i])))), value=numFont(y.scoreCalc(y.dataArray(i+1), 0)), inline=False)
        await ctx.send(embed=embed2)
        
        for p in range(len(player)):
            sleep(3)
            user = await client.fetch_user(player[p])
            await ctx.send(":green_circle: **{}**??? ???????????????! ??? ???????????? ???????????? ???????????????!".format(user))

            temp2 = y.dataArray(p+1)
            totals = y.scoreCalc(temp2, 0)
            bonuss = y.scoreCalc(temp2, 1)
            
            embed = discord.Embed(title="**{}??? ??????**".format(user), description="`?????????: {} / 13`".format(r+1), color=0xff0000)
            embed.add_field(name="Upper Section", value="`1` Ones {}\n`2` Twos {}\n`3` Threes {}\n`4` Fours {}\n`5` Fives {}\n`6` Sixs {}\n`Sp` Above 63 (+60p) `{}/63` {}".format(iv(temp2[0]),iv(temp2[1]),iv(temp2[2]),iv(temp2[3]),iv(temp2[4]),iv(temp2[5]),bonuss, iv2(bonuss)), inline=False)
            embed.add_field(name="Lower Section", value="`7` 3 Kinds {}\n`8` 4 Kinds {}\n`9` Full House (+25p) {}\n`10` S-Straight (+30p) {}\n`11` L-Straight (+40p) {}\n`12` Chance {}\n`13` Yatch (+50p) {}".format(iv(temp2[6]),iv(temp2[7]),iv(temp2[8]),iv(temp2[9]),iv(temp2[10]),iv(temp2[11]),iv(temp2[12])), inline=False)
            embed.add_field(name="Score", value=numFont(totals), inline=False)
            await ctx.send(embed=embed)
            
            sleep(1)
            templ = y.rollDice()
            await ctx.send("{} {} {} {} {}".format(dt(templ[0]), dt(templ[1]), dt(templ[2]), dt(templ[3]), dt(templ[4])))

            await ctx.send("`{}` ?????? ?????? ???????????? ????????? ????????? ?????????! ???????????? 60??? ????????????! (ex> `k 1 2 4` ????????? 1, 2, 4??? ???????????? ?????? ?????????)".format(user))

            def check1(m):
                return m.content.startswith('k')
            
            try:
                msg = await client.wait_for('message', timeout=60.0 , check=check1)
                keep = msg.content.split(" ")[1:]
                print(keep)
                for i in keep:
                    templ = y.rollDice(int(i))
            except:
                 await ctx.send("`{}` 60??? ??????! ?????? ????????? ??? ??????".format(user))
            
            await ctx.send("{} {} {} {} {}".format(dt(templ[0]), dt(templ[1]), dt(templ[2]), dt(templ[3]), dt(templ[4])))

            temp2 = y.dataArray(p+1)
            totals = y.scoreCalc(temp2, 0)
            bonuss = y.scoreCalc(temp2, 1)

            embed = discord.Embed(title="**{}??? ??????**".format(user), description="`?????????: {} / 13`".format(r+1), color=0x009900)
            embed.add_field(name="Upper Section", value="`1` Ones {}\n`2` Twos {}\n`3` Threes {}\n`4` Fours {}\n`5` Fives {}\n`6` Sixs {}\n`Sp` Above 63 (+60p) `{}/63` {}".format(iv(temp2[0]),iv(temp2[1]),iv(temp2[2]),iv(temp2[3]),iv(temp2[4]),iv(temp2[5]),bonuss, iv2(bonuss)), inline=False)
            embed.add_field(name="Lower Section", value="`7` 3 Kinds {}\n`8` 4 Kinds {}\n`9` Full House (+25p) {}\n`10` S-Straight (+30p) {}\n`11` L-Straight (+40p) {}\n`12` Chance {}\n`13` Yatch (+50p) {}".format(iv(temp2[6]),iv(temp2[7]),iv(temp2[8]),iv(temp2[9]),iv(temp2[10]),iv(temp2[11]),iv(temp2[12])), inline=False)
            embed.add_field(name="Score", value=numFont(totals), inline=False)
            await ctx.send(embed=embed)

            while(1):
                await ctx.send("`{}` ????????? ????????? ?????? ????????? ????????? ?????????. (ex> `r 12` ????????? 12??????(??????)??? ?????? ??????)".format(user))

                def check1(m):
                    return m.content.startswith('r')
            
                try:
                    msg = await client.wait_for('message', timeout=60.0 , check=check1)
                    rec = int(msg.content.split(" ")[1])
                    print(rec)
                    if temp2[rec-1] == -1:
                        y.selectScore(rec, templ, y.dataArray(p+1))
                        await ctx.send("`{}` {}?????? ????????? ?????? ???????????????!".format(user, rec))
                        break
                except:
                    pass

    embed3 = discord.Embed(title="**Yatch Gayme**", description="`?????? ?????????`", color=0x009900)
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
    await ctx.send(":first_place:**{}** ?????? {}????????? ?????????????????????!\n??????????????? **{}???** ?????????! (3%??? ??????)".format(names[w], numFont(max(final)), format(int(0.97*len(player)*int(betting)), ',')))
            
        

# 3.4. Run Bot
client.run(token)
