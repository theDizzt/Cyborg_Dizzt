import os
import discord

# 1.3.1 최고 레벨
final_lv = 240

# 1.3.2 앰블럼 이름 데이터
arr_emblem = [[
    'Initial', 'Scarlet', 'Amber', 'Topaz', 'Chlorophyll', 'Aquatic',
    'Sapphire', 'Violette', 'Cosmic', 'Ultimate'
],
              [
                  'Square', 'Ring', 'Trigon', 'Stelle', 'Hexagon', 'Diamond',
                  'Hexagram', 'Insignia', 'Plasma', 'Collar', 'Cardioid',
                  'Fluid', 'Flame', 'Bolt', 'Solarus', 'Polyphemus', 'Spiral',
                  'Physis', 'Elementum', 'Nebula', 'Aeternum', 'Libertas',
                  'Iustitia', 'Transcendence'
              ]]


# 1.3.3 경험치 데이터
def xpList():
    file = open("./config/xp.txt", "r")
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
max_xp = xp_arr[final_lv - 1]

# 2.3. 경험치 관련


# 2.3.1 최고 레벨 출력
def maxLevel():
    return final_lv


# 2.3.2 정수 레벨 출력
def level(exp):
    if exp > max_xp:
        return final_lv
    else:
        i = 1
        while (1):
            if exp < xp_arr[i]:
                break
            else:
                i += 1
        return i


# 2.3.3. Required XP
def need_exp(i):
    return int(xp_arr[i])


# 2.3.4. Level Up (Boolean)
def level_up(temp, pres):
    if temp > final_lv:
        return False
    else:
        if need_exp(temp) < pres:
            return True
        else:
            return False


# 2.3.5. emblem name
def emblemName(lv):
    return "{} {} Emblem".format(arr_emblem[0][int((lv - 1) % 10)],
                                 arr_emblem[1][int((lv - 1) / 10)])


def checkBox(s):
    if s == 0:
        return ":black_large_square:"
    elif s == 1:
        return ":white_check_mark:"
    else:
        return ":question:"


# 2.2. Storage List Read
def storageLineRead():
    file = open("./config/storage.txt", "r", encoding='UTF8')
    temp = []
    for data in file.readlines():
        temp.append(data.split(" - "))

    return temp


# 2.3. voice
def voiceRead(user: discord.Member = None):
    file = open("./data/voice/" + str(user.id) + ".txt", "r+")
    if file != None:
        return int(file.read())
    else:
        pass
    file.close()


def voiceWrite(user: discord.Member = None, value: int = None):
    file = open("./data/voice/" + str(user.id) + ".txt", "w+")
    if file == None:
        pass
    file.write(str(value))
    file.close()


def voiceDelete(user: discord.Member = None):
    file = "./data/voice/" + str(user.id) + ".txt"
    if os.path.isfile(file):
        os.remove(file)


# 2.4.3. Number Font
def numFont(i):
    #old
    """
    num = [
        '<:n0:1085510761637482526>', '<:n1:1085510763315208252>',
        '<:n2:1085510766221860864>', '<:n3:1085510767895400549>',
        '<:n4:1085510771087265802>', '<:n5:1085510773016633444>',
        '<:n6:1085510776867000380>', '<:n7:1085510779954012231>',
        '<:n8:1085510783116513340>', '<:n9:1085510786564247644>'
    ]
    """
    num = [
        '<:g0:1135109310536482866>', '<:g1:1135109312180650055>',
        '<:g2:1135109315657744505>', '<:g3:1135109319206117416>',
        '<:g4:1135109323006152814>', '<:g5:1135109324847456296>',
        '<:g6:1135109328710402189>', '<:g7:1135109331927453737>',
        '<:g8:1135109335274491944>', '<:g9:1135109339447840798>'
    ]
    result = ''
    for c in str(i):
        result += num[int(c)]
    return result


# 2.4.5. uid Extract
def extractUid(author):
    return int(author[2:][:-1])
