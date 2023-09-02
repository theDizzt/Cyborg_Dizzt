import discord
from discord.ext import commands
import functions.sqlcontrol as q
import functions.etcfunctions as etc

codelist = {
    "CODINFUN!!": 7,
    "dasihanbeon": 8,
    "heart": 9,
    "20200402": 10,
    "sectorform": 11,
    "agility": 12,
    "crossfooting": 13,
    "obliqueroot": 14,
    "avoidnsketch": 15,
    "safetysecurity": 16,
    "deadlycrystal": 17,
    "waiter": 18,
    "hassiumelement": 23
}


class InputCode(discord.ui.Modal, title='Input Special Code!!'):
    name = discord.ui.TextInput(label='Input',
                                style=discord.TextStyle.short,
                                placeholder='Input your special code...',
                                required=True)
    """
    answer = discord.ui.TextInput(
        label='한줄소개',
        style=discord.TextStyle.long,
        placeholder='아무말이나 입력해주세요',
        required=False,
        max_length=300,
    )"""

    async def on_submit(self, ctx):
        result = codelist.get(self.name.value)
        if result == None:
            await ctx.reply(
                "`(⩌Δ ⩌ ;)` This code does not exist. Please double check that there are no typos!"
            )
        else:
            if q.readStorage(ctx.author, result) == 1:
                await ctx.reply(
                    "`(⩌Δ ⩌ ;)` You have already unlocked this skin!")
            else:
                q.storageModify(ctx.author, result, 1)
                await ctx.reply(
                    ":green_circle: Code entered! Your reward has been received."
                )


class SpecialCode(commands.Cog):  # Cog를 상속하는 클래스를 선언

    def __init__(self, client: commands.Bot):  # 생성자 작성
        self.client = client

    # 3.3.99. Event Code
    @commands.hybrid_command(name='code', description="사전입니다.")
    async def code(self, ctx):
        await ctx.interaction.response.send_modal(InputCode())


async def setup(client):
    await client.add_cog(SpecialCode(client))
