import asyncio
import os
import discord
from discord import guild
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get
# import youtube_dl
# import os
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import youtube_dl



class VoiceCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    server, server_id, name_channel = None,None,None
    global domains
    domains = ['https://www.youtube.com/','http://www.youtube.com/','https://youtu.be/','http://youtu.be/']

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
    
    # @commands.command()
    # async def play(self,ctx, url):
    #     await ctx.message.author.voice.channel.connect(reconnect=False)
    #     YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    #     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    #     voice = get(self.bot.voice_clients, guild=ctx.guild)
    #     # print(voice)
    #     with YoutubeDL(YDL_OPTIONS) as ydl:
    #         info = ydl.extract_info(url, download=False)
    #     URL = info['formats'][0]['url']
    #     voice.play(FFmpegPCMAudio(executable="music/ffmpeg.exe", source =URL, **FFMPEG_OPTIONS))
    #     voice.is_playing()


def setup(bot):
    bot.add_cog(VoiceCommands(bot))