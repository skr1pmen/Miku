import discord
from discord.ext import commands
from discord.utils import get



class VoiceCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

#Команда_connect
    @commands.command(pass_context=True)
    async def connect(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f'{channel}')

#Команда_disconnect
    @commands.command(pass_context=True)
    async def disconnect(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
        else:
            voice = await channel.connect()

def setup(bot):
    bot.add_cog(VoiceCommands(bot))