import discord
from discord.ext import commands
import functions.sqlcontrol as q
import yaml
import functions.etcfunctions as etc

admin_login = []
with open('./config/admin.yml') as f:
    admins = yaml.load(f, Loader=yaml.FullLoader)


class Admins(commands.Cog):  # Cog를 상속하는 클래스를 선언

    def __init__(self, client: commands.Bot):  # 생성자 작성
        self.client = client

    # Admin Login [ID: 89]
    @commands.command()
    async def login(self, ctx, sid: str = None, spw: str = None):

        try:
            await ctx.message.delete()
        except:
            pass

        try:
            user = "UID" + str(ctx.author.id)

            if admins[user]['id'] == sid and admins[user]['pw'] == spw:
                global admin_login
                admin_login.append(ctx.author.id)
                await ctx.send(f"<@{ctx.author.id}> Logined!")
                print(admin_login)
            else:
                await ctx.send(f"<@{ctx.author.id}> Login Failed...")

        except:
            await ctx.send(f"<@{ctx.author.id}> no admin permissions allowed.")

    # Admin Logout [ID: 90]
    @commands.command()
    async def logout(self, ctx):
        if ctx.author.id in admin_login:
            admin_login.remove(ctx.author.id)
            await ctx.reply(f"<@{ctx.author.id}> Logouted!")
            print(admin_login)

    # XP Editing [ID: 91]
    @commands.hybrid_command(name='xp',
                             description="Give XP to selected user.")
    #@discord.app_commands.describe(user="User mention",amount="Write amount of XP to give")
    async def xp(self, ctx, user="all", amount=0):
        if (user == "all" or user == "전체") and ctx.author.id in admin_login:
            q.xpAddAll(int(amount))
            await ctx.reply(
                "**가입자 총원**은 성공적으로 **{}**의 경험치를 받았습니다!".format(amount))

        elif ctx.author.id in admin_login:
            u = int(etc.extractUid(user))
            q.xpAddById(u, int(amount))
            xp = q.readXpById(u)
            lv = etc.level(xp)
            xp1 = xp - etc.need_exp(lv - 1)
            xp2 = etc.need_exp(lv) - etc.need_exp(lv - 1)
            text = "[Level] {}, [XP] {:,d} / {:,d} ({:.2f}%), [Total] {:,d}".format(
                lv, xp1, xp2, 100 * xp1 / xp2, xp)
            await ctx.reply(
                "**{}**(은)는 성공적으로 **{}**의 경험치를 받았습니다!\n현재 경험치: {}".format(
                    q.readTagById(u), amount, text))

    # User List [ID: 92]
    @commands.command(aliases=['유저목록'])
    async def userlist(self, ctx):
        if ctx.author.id in admin_login:
            rank = q.userList()
            await ctx.send("출력을 시작합니다!")
            await ctx.send("총 데이터 수 : `{}`".format(len(rank)))
            for user in rank:
                await ctx.send(
                    "**{}**#{} ({}) | `{} / {}` | `Total : {:,d}`".format(
                        user[2],
                        str(user[1]).zfill(4), user[0], etc.level(user[3]),
                        etc.maxLevel(), user[3]))
            await ctx.send("출력이 끝났습니다!")

    # Rank List [ID: 93]
    @commands.command(aliases=['랭킹목록'])
    async def rankinglist(self, ctx):
        if ctx.author.id in admin_login:
            rank = q.xpRanking()
            rank_value = 1
            await ctx.send(":green_circle: 랭킹 리스트를 출력합니다! (시간이 오래 걸릴수도 있습니다)")

            for user in rank:
                await ctx.send(
                    "{} **{}**#{} | `{} / {}` | `Total : {:,d}`".format(
                        etc.numFont(rank_value), user[2],
                        str(user[1]).zfill(4), etc.level(user[3]),
                        etc.maxLevel(), user[3]))
                rank_value += 1

    # Valid Text [ID: 94]
    @commands.command()
    async def validtest(self, ctx):
        if ctx.author.id in admin_login:
            count = 1
            await ctx.send(
                ":green_circle: 유저 유효성 검사를 시작하겠습니다! (시간이 오래 걸릴수도 있습니다)")
            testarr = q.idList()
            for u in testarr:
                try:
                    user = await client.fetch_user(u[0])
                    await ctx.send(
                        f"`{count}/{len(testarr)}` :green_circle: Id:{u[0]} 테스트 성공!"
                    )
                except:
                    await ctx.send(
                        f"`{count}/{len(testarr)}` `(⩌Δ ⩌ ;)` Id:{u[0]} 는 올바른 데이터가 아닙니다!"
                    )
                count += 1

    # Skin Unlock [ID: 95]
    @commands.hybrid_command(name='unlock', description="Unlock user's skin")
    @discord.app_commands.describe(obj="User mention",
                                   skin="Integer only",
                                   lock="Binary only")
    async def unlock(self,
                     ctx,
                     obj: str = None,
                     skin: int = None,
                     lock: int = 1):
        if ctx.author.id in admin_login:
            try:
                user = etc.extractUid(obj)
            except:
                await ctx.reply("`(⩌Δ ⩌ ;)` Invalid User id...")
            Rank = etc.storageLineRead()
            user_name = q.readTagById(user)

            if lock == "1":
                if not q.readStorageById(user, skin):
                    q.storageModifyById(user, skin, 1)
                    await ctx.reply(
                        f":green_circle: **{user_name}** successfully unlocked `{Rank[skin - 1][0]}`!"
                    )
                else:
                    await ctx.reply(
                        f":exclamation: **{user_name}** already unlocked `{Rank[skin - 1][0]}`!"
                    )
            elif lock == "0":
                if q.readStorageById(user, skin):
                    q.storageModifyById(user, skin, 0)
                    await ctx.reply(
                        f":green_circle: **{user_name}** successfully locked `{Rank[skin - 1][0]}`!"
                    )
                else:
                    await ctx.reply(
                        f":exclamation: **{user_name}** already locked `{Rank[skin - 1][0]}`!"
                    )
            else:
                await ctx.reply("`(⩌Δ ⩌ ;)` Invalid option.")

    # Ultimate [ID: 96]
    @commands.command()
    async def ultimate(self,
                       ctx,
                       user: str = None,
                       option: str = None,
                       value: str = None):
        if ctx.author.id in admin_login:

            u = int(etc.extractUid(user))

            if option == 'xp':
                q.xpModifyById(u, int(value))
                await ctx.reply(
                    "`⸜(*◉ ᴗ ◉)⸝` Transformed data with magical powers...")

            elif option == 'money':
                q.moneyModifyById(u, int(value))
                await ctx.reply(
                    "`⸜(*◉ ᴗ ◉)⸝` Transformed data with magical powers...")

            elif option == 'skin':
                q.skinModifyById(u, int(value))
                await ctx.reply(
                    "`⸜(*◉ ᴗ ◉)⸝` Transformed data with magical powers...")

            elif option == 'discrim':
                q.discrimModifyById(u, int(value))
                await ctx.reply(
                    "`⸜(*◉ ᴗ ◉)⸝` Transformed data with magical powers...")

            elif option == 'nick':
                q.nickModifyById(u, str(value))
                await ctx.reply(
                    "`⸜(*◉ ᴗ ◉)⸝` Transformed data with magical powers...")

            elif option == 'create':
                q.newAccountById(u, str(value))
                await ctx.reply(
                    "`⸜(*◉ ᴗ ◉)⸝` Transformed data with magical powers...")

            else:
                await ctx.reply("Not allowed!")

        else:
            await ctx.reply("Not allowed!")

    # Money Editing [ID: 97]
    @commands.hybrid_command(name='money',
                             description="Give money to selected user.")
    #@discord.app_commands.describe(user="User mention",amount="Write amount of money to give")
    async def money(self, ctx, user: str = "all", amount: int = 0):
        if (user == "all" or user == "전체") and ctx.author.id in admin_login:
            q.moneyAddAll(amount)
            await ctx.reply(
                "**가입자 총원**은 성공적으로 **{}$**의 돈을 받았습니다!".format(amount))

        elif ctx.author.id in admin_login and type(user) is discord.Member:
            u = int(etc.extractUid(user))
            q.moneyAddById(u, amount)
            mn = q.readMoneyById(u)
            await ctx.reply(
                "**{}**(은)는 성공적으로 **{}$**의 돈을 받았습니다!\n현재 소지 금액: **{}**".format(
                    q.readTagById(u), amount, mn))


async def setup(client):  # setup 함수로 cog를 추가한다.
    await client.add_cog(Admins(client))
