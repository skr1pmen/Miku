from discord.ext import commands
import discord
from config import settings


class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = f"{member.mention} присоединился к серверу."
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(settings['logChannel'])
        await channel.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        msg = f"{member.mention} покинул сервер."
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(settings['logChannel'])
        await channel.send(msg)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot:
            msg = discord.Embed(title=f"{before.author.name} изменил сообщение.")
            msg.add_field(name=f"Было:", value=f"``{before.content}``", inline = False)
            msg.add_field(name=f"Стало:", value=f"``{after.content}``", inline = False)
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(settings['logChannel'])
            await channel.send(embed = msg)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            msg = discord.Embed(title=f"Сообщение {message.author.name} удалили.", description=f"{message.content}")
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(settings['logChannel'])
            await channel.send(embed = msg)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel is None:
            msg = f"{member.mention} присоединился к каналу {after.channel.mention}"
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(settings['logChannel'])
            await channel.send(msg)
        elif after.channel is None:
            msg = f"{member.mention} вышел из канала {before.channel.mention}"
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(settings['logChannel'])
            await channel.send(msg)
        elif before.channel != after.channel:
            msg = f"{member.mention} перешёл из канала {before.channel.mention} в канал {after.channel.mention}"
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(settings['logChannel'])
            await channel.send(msg)


def setup(bot):
    bot.add_cog(Logs(bot))