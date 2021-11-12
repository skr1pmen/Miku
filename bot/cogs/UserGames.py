import discord
from discord.ext import commands
import json
import asyncio

class UserGameStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, prev, cur):
        games = json.load(open('bot/textFile/GamesList.json'))
        role = discord.utils.get(cur.guild.roles, name="🎮Геймер")
        if cur.activity and cur.activity.name.lower() in games:
                await cur.add_roles(role)
        # elif prev.activity and prev.activity.name.lower() in games and not cur.activity:
        #         if role in cur.roles:
        #             await cur.remove_roles(role)

def setup(bot):
    bot.add_cog(UserGameStatus(bot))