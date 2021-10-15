import discord
from discord import guild
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord_components.client import DiscordComponents
from config import settings
import random
import json
import string
import asyncio

class DefaultDiscordCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.bot)
        if settings['debug'] == True:
            print("Бот запущен в режиме Разработчика!")
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=settings['versionDebug']))
        else:
            print("Бот: {0}\nВерсия {0}: {1}\nДата создания: 8.03.2019\nДата перезапуска: 14.06.2021\nБот успешно запушен!" .format(self.bot.user.name,settings['version']))
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Версию {}".format(settings['version'])))

    @commands.Cog.listener()
    async def on_message(self, message):
        OffMat = ["Или мне кажется, или ты матекнулся {}?\nНадеюсь показалось, а то забаню!","Я конечно не профессионалка, но мне показалось что ты материшся {}","Не используй таких слов, хорошо {}?"]

        if 'габе жив' in message.content.lower():
            await message.channel.send("Габе Рип!!!")

        if 'мику рип' in message.content.lower():
            await message.channel.send("Сам Рип, так же как и Габе!!!")

        if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.content.split(' ')}.intersection(set(json.load(open('bot/textFile/cenz.json')))) != set():
            Mes = await message.channel.send(random.choice(OffMat).format(message.author.mention))
            await asyncio.sleep(30)
            await Mes.delete()

        if '@everyone' in message.content.lower():
            await message.add_reaction('👍')
            await message.add_reaction('👎')

        if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.content.split(' ')}\
        .intersection(set(json.load(open('bot/textFile/vk.json')))) != set():
            await asyncio.sleep(5)
            await message.add_reaction('<:VK:886578224275025961>')

        if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.content.split(' ')}\
        .intersection(set(json.load(open('bot/textFile/yt.json')))) != set():
            await asyncio.sleep(5)
            await message.add_reaction('<:YouTube:886325532302655578>')

        if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.content.split(' ')}\
        .intersection(set(json.load(open('bot/textFile/twitch.json')))) != set():
            await asyncio.sleep(5)
            await message.add_reaction('<:Twitch:886578298543550544>')

            await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = member.guild.get_role(role_id=547109093907628046)
        await member.add_roles(role)
        my_channel = self.bot.get_channel(550082377637036035)
        emb = discord.Embed(color=0x00d166)
        emb.add_field(name='У нас пополнение!',value=f'Приветствуем {member.mention}.')
        await my_channel.send(embed = emb)
        
        index1 = 0
        lines = []
        with open("bot/textFile/rules.txt", "r", encoding='UTF-8') as file:
            for line in file.readlines():
                line = line.strip()
                lines.append(line)
                index1 += 1
        emb = discord.Embed()
        emb.description = '\n'.join(lines)
        emb.title = 'В общем давай я расскажу тебе правила сервера.'
        emb.colour = 0x9932cc
        emb.set_author(name="Привет я Мику! Я управляющая этим сервером SkripMen.")
        emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
        await member.send(embed = emb)

def setup(bot):
    bot.add_cog(DefaultDiscordCommand(bot))