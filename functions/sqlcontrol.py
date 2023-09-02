# 0. Import modules
import discord
from discord.ext import commands
import sqlite3
import random as r

# 1. Connect DB
conn = sqlite3.connect('./data/user.db')
c = conn.cursor()

# 2. Sub Functions


# 2.1. Init Setting
def initSetting():
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS main(
    id INTEGER PRIMARY KEY,
    discrim INTEGER NOT NULL,
    nick TEXT NOT NULL,
    xp INTEGER NOT NULL,
    money INTEGER NOT NULL,
    skin INTEGER NOT NULL);"""

    c.execute(sql)
    conn.commit()

    sql = """CREATE TABLE IF NOT EXISTS storage(
    id INTEGER PRIMARY KEY);"""

    c.execute(sql)
    conn.commit()

    for i in range(1, 1025):
        try:
            sql = "ALTER TABLE storage ADD COLUMN {} [TINYINT] DEFAULT 0;".format(
                "id" + str(i))
            c.execute(sql)
            conn.commit()
        except:
            pass

    conn.close()


# 2.2. Backup Data
def initSetting2():
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS main(
    id INTEGER PRIMARY KEY,
    discrim INTEGER NOT NULL,
    nick TEXT NOT NULL,
    xp INTEGER NOT NULL,
    money INTEGER NOT NULL,
    skin INTEGER NOT NULL);"""

    c.execute(sql)
    conn.commit()

    sql = """CREATE TABLE IF NOT EXISTS storage(
    id INTEGER PRIMARY KEY);"""

    c.execute(sql)
    conn.commit()

    for i in range(1, 1024):
        try:
            sql = "ALTER TABLE storage ADD COLUMN {} [TINYINT] DEFAULT 0;".format(
                "id" + str(i))
            c.execute(sql)
            conn.commit()
        except:
            pass

    conn.close()


# 3. Actions


# 3.1. Add data
def newAccount(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()

    INSERT_SQL = 'INSERT INTO main (id, discrim, nick, xp, money, skin) VALUES (?,?,?,?,?,?);'
    discrim = r.randint(0, 10000)

    data = ((user.id, discrim, user.name, 0, 0, 1))
    c.execute(INSERT_SQL, data)
    conn.commit()

    conn.close()


def newAccountById(user: int = None, name: str = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()

    INSERT_SQL = 'INSERT INTO main (id, discrim, nick, xp, money, skin) VALUES (?,?,?,?,?,?);'
    discrim = r.randint(0, 10000)

    data = ((user, discrim, name, 0, 0, 1))
    c.execute(INSERT_SQL, data)
    conn.commit()

    conn.close()


# 3.2. Write data

# 3.2.1. Xp Modifier


# 3.2.1.1. Xp Value Edit
def xpModify(user: discord.Member = None, amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET xp = ? WHERE id = ?", (amount, user.id))
    conn.commit()
    c.close()


def xpModifyById(user: int = None, amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET xp = ? WHERE id = ?", (amount, user))
    conn.commit()
    c.close()


# 3.2.1.2. Xp Add
def xpAdd(user: discord.Member = None, amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET xp = xp + ? WHERE id = ?", (amount, user.id))
    conn.commit()
    c.close()


def xpAddById(user: int = None, amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET xp = xp + ? WHERE id = ?", (amount, user))
    conn.commit()
    c.close()


# 3.2.1.3. Xp Add All
def xpAddAll(amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET xp = xp + ?", (amount, ))
    conn.commit()
    c.close()


# 3.2.2. Money Modifier


# 3.2.2.1. Money Value Edit
def moneyModify(user: discord.Member = None, amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET money = ? WHERE id = ?", (amount, user.id))
    conn.commit()
    c.close()


def moneyModifyById(user: int = None, amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET money = ? WHERE id = ?", (amount, user))
    conn.commit()
    c.close()


# 3.2.2.2. Money Add
def moneyAdd(user: discord.Member = None, amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET money = money + ? WHERE id = ?",
              (amount, user.id))
    conn.commit()
    c.close()


def moneyAddById(user: int = None, amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET money = money + ? WHERE id = ?", (amount, user))
    conn.commit()
    c.close()


# 3.2.1.3. Xp Add All
def moneyAddAll(amount: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET money = money + ?", (amount, ))
    conn.commit()
    c.close()


# 3.2.3. Tag Modifier


# 3.2.3.1. Nickname Edit
def nickModify(user: discord.Member = None, name: str = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET nick = ? WHERE id = ?", (name, user.id))
    conn.commit()
    c.close()


def nickModifyById(user: int = None, name: str = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET nick = ? WHERE id = ?", (name, user))
    conn.commit()
    c.close()


# 3.2.3.2. Discrim Edit
def discrimModify(user: discord.Member = None, value: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET discrim = ? WHERE id = ?", (value, user.id))
    conn.commit()
    c.close()


def discrimModifyById(user: int = None, value: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET discrim = ? WHERE id = ?", (value, user))
    conn.commit()
    c.close()


# 3.2.4. Skin Value Edit
def skinModify(user: discord.Member = None, value: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET skin = ? WHERE id = ?", (value, user.id))
    conn.commit()
    c.close()


def skinModifyById(user: int = None, value: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE main SET skin = ? WHERE id = ?", (value, user))
    conn.commit()
    c.close()


# 3.3. Read data


# 3.3.1. Read All
def readAll(user: discord.Member):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute('SELECT * FROM main WHERE id=?;', (user.id))
    result = c.fetchall()
    return result


# 3.3.2. Read Name


# 3.3.2.1. Name only
def readNick(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT nick FROM main WHERE id = ?"
    c.execute(sql, (user.id, ))
    result = c.fetchone()[0]
    return str(result)


def readNickById(user: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT nick FROM main WHERE id = ?"
    c.execute(sql, (user, ))
    result = c.fetchone()[0]
    return str(result)


# 3.3.2.2. Discrim only
def readDiscrim(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT discrim FROM main WHERE id = ?"
    c.execute(sql, (user.id, ))
    result = c.fetchone()[0]
    return str(result).zfill(4)


def readDiscrimById(user: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT discrim FROM main WHERE id = ?"
    c.execute(sql, (user, ))
    result = c.fetchone()[0]
    return str(result).zfill(4)


# 3.3.2.3. Full Tag
def readTag(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT nick, discrim FROM main WHERE id = ?"
    c.execute(sql, (user.id, ))
    temp = c.fetchone()
    result = str(temp[0]) + "#" + str(temp[1]).zfill(4)
    return result


def readTagById(user: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT nick, discrim FROM main WHERE id = ?"
    c.execute(sql, (user, ))
    temp = c.fetchone()
    result = str(temp[0]) + "#" + str(temp[1]).zfill(4)
    return result


# 3.3.3. Read Xp
def readXp(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT xp FROM main WHERE id = ?"
    c.execute(sql, (user.id, ))
    result = c.fetchone()[0]
    return result


def readXpById(user: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT xp FROM main WHERE id = ?"
    c.execute(sql, (user, ))
    result = c.fetchone()[0]
    return result


# 3.3.4. Read Money
def readMoney(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT money FROM main WHERE id = ?"
    c.execute(sql, (user.id, ))
    result = c.fetchone()[0]
    return result


def readMoneyById(user: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT money FROM main WHERE id = ?"
    c.execute(sql, (user, ))
    result = c.fetchone()[0]
    return result


# 3.3.5. Read Skin
def readSkin(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT skin FROM main WHERE id = ?"
    c.execute(sql, (user.id, ))
    result = c.fetchone()[0]
    return result


def readSkinById(user: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT skin FROM main WHERE id = ?"
    c.execute(sql, (user, ))
    result = c.fetchone()[0]
    return result


# 3.4. List & Ranking


# 3.4.1. User List
def userList():
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT * FROM main"
    c.execute(sql)
    result = c.fetchall()
    return result


# 3.4.2. User id List
def idList():
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT id FROM main"
    c.execute(sql)
    result = c.fetchall()
    return result


# 3.4.3. XP Ranking
def xpRanking():
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT *, RANK() OVER (ORDER BY xp DESC) ranking FROM main;"
    c.execute(sql)
    result = c.fetchall()
    return result


# 3.4.4. Money Ranking
def moneyRanking():
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT *, RANK() OVER (ORDER BY money DESC) ranking FROM main;"
    c.execute(sql)
    result = c.fetchall()
    return result


# 3.5. Skin Data


# 3.5.0. Drop table
def dropStorage():
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()

    INSERT_SQL = 'DROP TABLE IF EXISTS storage;'
    c.execute(INSERT_SQL)
    conn.commit()

    conn.close()


# 3.5.1 Add data
def newStorage(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()

    INSERT_SQL = 'INSERT INTO storage (id) VALUES (?);'

    data = ((user.id))
    c.execute(INSERT_SQL, data)
    conn.commit()

    c.execute("UPDATE storage SET id1 = ? WHERE id = ?", (1, user.id))

    for i in range(2, 1025):
        c.execute(
            "UPDATE storage SET {} = ? WHERE id = ?".format("id" + str(i)),
            (0, user.id))

    conn.commit()

    conn.close()


def newStorageById(user: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()

    INSERT_SQL = 'INSERT INTO storage (id) VALUES (?);'

    c.execute(INSERT_SQL, (user, ))
    conn.commit()

    c.execute("UPDATE storage SET id1 = ? WHERE id = ?", (1, user))

    for i in range(2, 1025):
        c.execute(
            "UPDATE storage SET {} = ? WHERE id = ?".format("id" + str(i)),
            (0, user))

    conn.commit()

    conn.close()


# 3.5.2. Xp Data Write
def storageModify(user: discord.Member = None,
                  id: int = None,
                  value: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE storage SET {} = ? WHERE id = ?".format("id" + str(id)),
              (value, user.id))
    conn.commit()
    c.close()


def storageModifyById(user: int = None, id: int = None, value: int = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    c.execute("UPDATE storage SET {} = ? WHERE id = ?".format("id" + str(id)),
              (value, user))
    conn.commit()
    c.close()


# 3.5.3. Read Storage
def readStorage(user: discord.Member = None, id: str = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT {} FROM storage WHERE id = ?;".format("id" + str(id))
    c.execute(sql, (user.id, ))
    result = c.fetchone()[0]
    return result


def readStorageById(user: int = None, id: str = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT {} FROM storage WHERE id = ?;".format("id" + str(id))
    c.execute(sql, (user, ))
    result = c.fetchone()[0]
    return result


# 3.5.4. User Storage List
def storageList(user: discord.Member = None):
    conn = sqlite3.connect('./data/user.db')
    c = conn.cursor()
    sql = "SELECT * FROM storage WHERE id = ?;"
    c.execute(sql, (user.id, ))
    result = c.fetchone()
    return result
