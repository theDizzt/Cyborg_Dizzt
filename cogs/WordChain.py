import discord
from discord.ext import commands
import functions.sqlcontrol as q
import functions.etcfunctions as etc
import json
import re
import random
import requests

#끝말잇기 데이터 저장 및 크롤링 준비
header = {"user-agent": "Mozilla/5.0"}
chance = 5
ONEKILL_WORD = [
    '른', '녘', '늄', '랒', '읖', '릇', '쿄', '룅', '륨', '렁', '븀', '럴', '텝', '엌'
]
HISTORY_COM = []
HISTORY_USER = []
HISTORY = []


# 두음법칙 적용하기
def replace_sound_char(char):
    SOUND_LIST = {
        "라": "나",
        "락": "낙",
        "란": "난",
        "랄": "날",
        "람": "남",
        "랍": "납",
        "랑": "낭",
        "래": "내",
        "랭": "냉",
        "냑": "약",
        "략": "약",
        "냥": "양",
        "량": "양",
        "녀": "여",
        "려": "여",
        "녁": "역",
        "력": "역",
        "년": "연",
        "련": "연",
        "녈": "열",
        "렬": "열",
        "념": "염",
        "렴": "염",
        "렵": "엽",
        "녕": "영",
        "령": "영",
        "녜": "예",
        "례": "예",
        "로": "노",
        "록": "녹",
        "론": "논",
        "롱": "농",
        "뢰": "뇌",
        "뇨": "요",
        "료": "요",
        "룡": "용",
        "루": "누",
        "뉴": "유",
        "류": "유",
        "뉵": "육",
        "륙": "육",
        "륜": "윤",
        "률": "율",
        "륭": "융",
        "륵": "늑",
        "름": "늠",
        "릉": "능",
        "니": "이",
        "리": "이",
        "린": "인",
        "림": "임",
        "립": "입"
    }
    if char in SOUND_LIST:
        return SOUND_LIST[char]
    return char


# 단어찾기
def get_start_char_word(char):
    global HISTORY_COM
    query = f"{char}으로시작하는단어"
    url = f'https://ko.dict.naver.com/api3/koko/search?query={query}&range=word&shouldSearchOpen=false&page=1'
    r = requests.get(url, headers=header)
    j = r.json()
    items = j.get("searchResultMap", {}).get("searchResultListMap",
                                             {}).get("WORD",
                                                     {}).get("items", [])
    dicts = {}
    if len(items) > 0:
        for item in items:
            w = item.get("handleEntry")
            w_means = item.get("meansCollector")
            if len(w_means) == 0 or len(w) < 2:
                continue
            w_type = w_means[0].get("partOfSpeech")
            if w_type == "명사":
                mean = w_means[0].get("means")[0].get("value")
                mean = re.sub('(<([^>]+)>)', '', mean)
                if w not in HISTORY_COM:
                    dicts[w] = mean
    if len(dicts) > 0:
        rand_num = random.randint(0, len(dicts) - 1)
        _word, _value = [(k, v) for k, v in dicts.items()][rand_num]
        return {_word: _value}
    return None


# 게임 초기화
def init_game():
    global chance, HISTORY_COM, HISTORY_USER, HISTORY
    chance = 5
    HISTORY_COM = []
    HISTORY_USER = []
    HISTORY = []


# 존재하는 단어인지 검사하기
def check_word(word):
    #url = f'https://ko.dict.naver.com/api3/koko/search?query={word}&range=word'
    url = f"https://ko.dict.naver.com/api3/koko/search?query={word}&m=pc&range=entrySearch"
    r = requests.get(url, headers=header)
    r.encoding = 'utf-8'
    with open(r, 'r') as js:
        j = json.loads(js.read())
    #j = r.json()
    items = j.get("searchResultMap", {}).get("searchResultListMap",
                                             {}).get("WORD",
                                                     {}).get("items", [])
    result = {}
    if len(items) > 0:
        for item in items:
            _word = item.get("expEntry").strip()
            _word = re.sub('(<([^>]+)>)', '', _word)
            if _word != word:
                continue
            _mean = item.get("meansCollector")[0].get("means")[0].get("value")
            _type = item.get("meansCollector")[0].get("partOfSpeech")
            result["word"] = _word
            result["mean"] = re.sub('(<([^>]+)>)', '', _mean)
            result["type"] = _type
            break
    return result


def display_history():
    global HISTORY
    for c in HISTORY:
        print(f"{c} > ", end="")


class WordChain(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='끝말잇기', description="끝말잇기 챔피언에 도전해보자! (한국어 끝말잇기)")
    #@discord.app_commands.describe()
    async def wordchain_korean(self, ctx):

        global chance
        last_word = ""

        while True:
            user = ""

            #메세지 입력 체크
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            while chance > 0:
                await ctx.send(
                    f"`{q.readTag(ctx.author)}` 단어를 입력하세요 (q 입력시 종료):")
                input_word = await self.wait_for("message", check=check)
                user = input_word.content
                if user == "q":
                    break
                if len(user) <= 1:
                    await ctx.send(f"`{q.readTag(ctx.author)}` 포기합니까? (y/n):")
                    input_word = await self.wait_for("message", check=check)
                    yn = input_word.content
                    if yn == "y":
                        user = "q"
                        break
                    continue
                if user in HISTORY_USER:
                    chance -= 1
                    await ctx.send(
                        f"`{q.readTag(ctx.author)}` **{user}** 는 입력했던 단어 입니다.")
                    await ctx.send(
                        f"`{q.readTag(ctx.author)}` 는 총 **{chance}** 번의 기회가 남았습니다."
                    )
                    continue
                if user[-1] in ONEKILL_WORD:
                    await ctx.send(
                        f"`{q.readTag(ctx.author)}` 원킬 단어 입니다... 제가 졌네요...")
                    init_game()
                    continue

                r = check_word(user)
                if len(r) == 0:
                    chance -= 1
                    await ctx.send(
                        f"`{q.readTag(ctx.author)}` 존재하지 않는 단어입니다. **{chance}**번의 기회가 남았습니다."
                    )
                    continue
                if last_word != "":
                    if last_word != "" and user[0] != last_word[-1] and user[
                            0] != replace_sound_char(last_word[-1]):
                        if replace_sound_char(last_word[-1]) != last_word[-1]:
                            await ctx.send(
                                f'`{q.readTag(ctx.author)}` **{last_word[-1]}** 나 **{replace_sound_char(last_word[-1])}** 로 시작하는 단어야 합니다.'
                            )
                        else:
                            await ctx.send(
                                f'`{q.readTag(ctx.author)}` **{last_word[-1]}** 로 시작하는 단어야 합니다.'
                            )
                        await ctx.send(
                            f"`{q.readTag(ctx.author)}` **{chance}**의 기회가 남았습니다."
                        )
                        chance -= 1
                        continue
                await ctx.send(f"**{user}**: {r.get('mean')}")
                break

            if user == "q":
                await ctx.send("포기")
                break

            HISTORY_USER.append(user)
            HISTORY.append(user)
            chance = 5

            while True:
                words = get_start_char_word(user[-1])
                if words is None:
                    await ctx.send("승리!")
                    init_game()
                    break

                rand_num = random.randint(0, len(words) - 1)
                last_word, value = [(k, v) for k, v in words.items()][rand_num]
                if last_word in HISTORY_COM:
                    continue

                #display_history()
                await ctx.send(f" [[ {last_word} ]]")
                await ctx.send(f"{value}")
                HISTORY_COM.append(last_word)
                HISTORY.append(last_word)
                break


async def setup(client):
    await client.add_cog(WordChain(client))
