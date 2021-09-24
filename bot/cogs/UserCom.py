import asyncio
from itertools import cycle
from operator import setitem
import discord
from discord.ext import commands
import random
import psycopg2
from config import settings
import json
import requests
from PIL import Image, ImageFont, ImageDraw, ImageChops
import io

RandChoslo = ["Random.org","рандомайзеру","серверу"]
Color = [0x000080,0x00ced1,0x00ffff,0x006400,0x00ff7f,0x7fff00,0x00fa9a,0xffd700,0x8b4513,0xb22222,0xff0000,0xff1493,0xd02090,0x9400d3,0x8a2be2]

def circle(pfp,size = (215,215)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

class UserCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
#Соединение с БД
    global connection
    global cursor
    connection = psycopg2.connect(
        dbname='d7npuuht675g6t',
        user='dfelpwutbrsdwj',
        password='84d0cfdcf95f22787066edbc6cac37e900a64943ad8629d9ad30e325c6e797cc',
        host='ec2-44-198-223-154.compute-1.amazonaws.com')
    cursor = connection.cursor()

#Команда_clear
    @commands.command(pass_context=True, aliases=['чист', 'clear'])
    @commands.has_any_role('Бето-тестер','🔰 Бог','🔘 Админ','👑 Царь')
    async def __clear(self, ctx, limit: int = None):
        if limit != None:
            if limit < 0:
                emb = discord.Embed(color=0xa62019)
                emb.add_field(name='❌ Ошибка команды ``.clear``!',value=f'Что {ctx.author.mention}, дохрена умный? Сам попробуй удалить {limit} сообщений.')
                Mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(30)
                await Mes.delete()
            elif limit >= 100:
                emb = discord.Embed(color=0xa62019)
                emb.add_field(name='❌ Ошибка команды ``.clear``!',value=f'Ты превысил лимит количевства удаляемых сообщений.')
                Mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(30)
                await Mes.delete()
            else:
                await ctx.channel.purge(limit=limit+1)
                emb = discord.Embed(color=0x00d166)
                emb.add_field(name='✅ Успешно!',value=f'{ctx.author.mention} удалил {limit} сообщений.')
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(30)
                await Mes.delete()
                exit
        else:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка команды ``.clear``!',value='Необходимо ввести число!')
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(30)
            await Mes.delete()

    @__clear.error
    async def __clear_error(self, ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.clear``:",value="Вы не можете этого сделать! (У вас недостаточно прав)")
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(10)
        await Mes.delete()

#Команда_rand
#   @slash.slash(name='rand',description='Мику даст рандомное число в диапозоне который ты скажешь.',options=[
#     {'name':'one', "description": "Первое число", "type": 4, "requied": False},
#     {'name':'two',"description": "Второе число", "type": 4, "requied": False}
#     ],guild_ids = guild_ids)
    @commands.command(pass_context=True, aliases=['ранд', 'rand'])
    async def __rand(self, ctx, one, two):
        try:
            one= int(one)
            two= int(two)
            arg = random.randint(one,two)
        except ValueError:
            emb = discord.Embed(title= "",color = 0xff0000)
            emb.add_field(name="Ошибка команды ``.rand``:",value="Введены неправильные зачения, повтори попытку.")
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(10)
            await Mes.delete()
        else:
            servis = random.choice(RandChoslo)
            randMes = await ctx.send('Подключаюсь к {}'.format(servis))
            await ctx.message.delete()
            await asyncio.sleep(random.random())
            await randMes.edit(content='Подключаюсь к {} |'.format(servis))
            await asyncio.sleep(random.random())
            await randMes.edit(content='Подключаюсь к {} /'.format(servis))
            await asyncio.sleep(random.random())
            await randMes.edit(content='Подключаюсь к {} —'.format(servis))
            await asyncio.sleep(random.random())
            await randMes.edit(content='Подключаюсь к {} \\'.format(servis))
            await asyncio.sleep(random.random())
            await randMes.edit(content='Подключаюсь к {} |'.format(servis))
            await asyncio.sleep(random.random())
            await randMes.edit(content='Подключаюсь к {} /'.format(servis))
            await asyncio.sleep(random.random())
            await randMes.edit(content='Подключаюсь к {} —'.format(servis))
            await asyncio.sleep(random.random())
            await randMes.edit(content='Подключаюсь к {} \\'.format(servis))
            await asyncio.sleep(0.5)
            await randMes.edit(content="Твоё число: "+str(arg))
    @__rand.error
    async def __rand_error(self, ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.rand``:",value="Ты забыл ввести число, повтори попытку.")
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(10)
        await Mes.delete()  

#Команда_info
    @commands.command(pass_context= True, aliases=['инфо', 'info'])
    async def __info(self, ctx,member: discord.Member = None):
        if member is None:
            member = ctx.author
        name,nick,id,status = str(member),member.display_name,str(member.id),str(member.status).upper()
        created_at = member.created_at.strftime("%a %b\n%B %Y")
        joined_at = member.joined_at.strftime("%a %b\n%B %Y")
        cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id))
        money = str(cursor.fetchone()[0])
        roles = str(len(member.roles)-1)
        base = Image.open('img/base.png').convert('RGBA')
        background = Image.open('img/bg.png').convert('RGBA')
        pfp = member.avatar_url_as(size = 256)
        data = io.BytesIO(await pfp.read())
        pfp = Image.open(data).convert('RGBA')
        name = f"{name[:16]}..." if len(name)>16 else name
        nick = f"AKA:{nick[:17]}..." if len(nick)>17 else f"AKA:{nick}"
        draw = ImageDraw.Draw(base)
        pfp = circle(pfp,size=(215,215))

        font = ImageFont.truetype('img/arial.ttf', size=38)
        AKAfont = ImageFont.truetype('img/arial.ttf', size=30)
        subfont = ImageFont.truetype('img/arial.ttf', size=25)

        draw.text((280,240),name,font=font)
        draw.text((270,315),nick,font=AKAfont)
        draw.text((65,490),id,font=subfont)
        draw.text((405,490),status,font=subfont)

        draw.text((65,632),created_at,font=subfont)
        draw.text((405,632),joined_at,font=subfont)
        draw.text((65,770),money,font=subfont)
        draw.text((405,770),roles,font=subfont)
        base.paste(pfp,(56,158),pfp)

        background.paste(base,(0,0),base)

        with io.BytesIO() as a:
            background.save(a,"png")
            a.seek(0)
            await ctx.message.delete()
            await ctx.send(file = discord.File(a, "profile.png"))

#Комада_rules
    @commands.command(pass_context=True, aliases=['правила', 'rules'])
    async def __rules(self, ctx):
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
        emb.set_author(name="Привет я Мику! Я управляющая этим сервером.\nНе считая Skrip_men и его команды Aдминов конечно.")
        emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
        await ctx.send('{}, я выслала правила тебе в личку'.format(ctx.author.mention))
        await ctx.author.send(embed = emb)
        await ctx.message.delete()

#Команда_help
    @commands.command(pass_context=True, aliases=['хелп', 'help'])
    async def __help(self, ctx, command = None):
        if command == None:
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Доступные команды")
            emb.add_field(name="rules",value="Мику расскажет правила сервера у вас в личке")
            emb.add_field(name="info",value="Выдает краткую информацию о пользователе ``.info @Miku#8252``.")
            emb.add_field(name="clear",value="Удаляет сообщения в чате ``.clear 5``.")
            emb.add_field(name="about",value="Мику расскажет о себе у вас в личке")
            emb.add_field(name="rand",value="Мику выдаст тебе рандомное число в заданном тобой диапозоне чисел ``.rand 1 9999``.")
            emb.add_field(name="status",value="Позволяет менять статус Мику")
            emb.add_field(name="ban",value="Команда блокировки бользователя на сервере")
            emb.add_field(name="unban",value="Команда разблокировки бользователя на сервере с помощью id")
            emb.add_field(name="banlist",value="Команда вывода вписка всех забаненых пользователей сервера")
            emb.add_field(name="kick",value="Команда кика пользователя с сервера с возможностью возвращения")
            emb.add_field(name="mute",value="Команда блокирует голос и возможность писать в чат токсичным пользователям")
            emb.add_field(name="invite",value="Команда отправляет пользователям приглащение на сервер с помощью id")
            emb.add_field(name="balance",value="Команда для вывода баланса на сервере")
            emb.add_field(name="shop",value="Команда открывает магазин доступных для покупки ролей")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "info":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда info")
            emb.add_field(name="info",value="Выдает краткую информацию о пользователе ``.info @Miku#8252``.")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "rand":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда rand")
            emb.add_field(name="rand",value="Мику выдаст тебе рандомное число в заданном тобой диапозоне чисел ``.rand 1 9999``.")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "rules":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда rules")
            emb.add_field(name="rules",value="Мику расскажет правила сервера у вас в личке")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "delete":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда clear")
            emb.add_field(name="clear",value="Удаляет сообщения в чате ``.clear 5``.")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "about":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда about")
            emb.add_field(name="about",value="Мику расскажет о себе")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "status":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда status")
            emb.add_field(name="status",value="Позволяет менять статус Мику")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "ban":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда ban")
            emb.add_field(name="ban",value="Команда блокировки бользователя на сервере")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "unban":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда unban")
            emb.add_field(name="unban",value="Команда разблокировки бользователя на сервере с помощью id")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "banlist":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда banlist")
            emb.add_field(name="banlist",value="Команда вывода вписка всех забаненых пользователей сервера")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "kick":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда kick")
            emb.add_field(name="kick",value="Команда кика пользователя с сервера с возможностью возвращения")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "mute":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда mute")
            emb.add_field(name="mute",value="Команда блокирует голос и возможность писать в чат токсичным пользователям")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "invite":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда invite")
            emb.add_field(name="invite",value="Команда отправляет пользователям приглащение на сервер с помощью id")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "youtube":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда youtube")
            emb.add_field(name="youtube",value="Создание лобии для просмотра YouTube прямо в дискорде")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "chess":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда chess")
            emb.add_field(name="chess",value="Создание лобии для игры в Шахматы прямо в дискорде")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "balance":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда balance")
            emb.add_field(name="balance",value="Команда для вывода баланса на сервере")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()
        elif command == "shop":
            emb = discord.Embed(title= "",color = 0xffff00)
            emb.set_author(name= "Команда shop")
            emb.add_field(name="shop",value="Команда открывает магазин доступных для покупки ролей")
            emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
            await ctx.send(embed = emb)
            await ctx.message.delete()

#Команда_about
    @commands.command(pass_context=True, aliases=['ктоты', 'about'])
    async def __about(self, ctx):
        emb= discord.Embed(title="",color = 0x00bfff)
        emb.set_author(name= "Мику Хацунэ\nHatsune Miku", url="https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BA%D1%83_%D0%A5%D0%B0%D1%86%D1%83%D0%BD%D1%8D")
        emb.add_field(name="1.Кто ты ?",value="Я японская виртуальная певица, созданная компанией Crypton Future Media 31 августа 2007 года.\nШутка, на самом деле я Бот созданный для управления сервером Skrip_men")
        emb.add_field(name="2.Зачем ты нужна ?",value="Как я уже сказала, я нужна для помощи в управлении сервером Skrip_men")
        emb.add_field(name="3.Когда создана ?",value="Моей официальной датой создания является 8 марта 2019\n(вот я вас мужиков трести в 2 раза больше буду в марте)...Хехе...мда неловко получиловь")
        emb.add_field(name="4.Кто тебя написал и на каком языке ?",value="Я была написана Skrip_men'ом, на языке Python")
        emb.add_field(name="__Версия бота:__",value=f"{settings['version']}")
        emb.add_field(name="__Помошь в создании:__",value="alex_jonas,Southpaw,STRAYKERRR")

        emb.set_thumbnail(url= "https://raw.githubusercontent.com/SkripMen/mikubotskripmen/master/%D0%90%D0%92%D0%90%D0%A2%D0%90%D0%A0%D0%9C%D0%98%D0%9A%D0%A3.png")
        emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
        await ctx.author.send(embed = emb)
        await ctx.message.delete()

#Команда_status
    @commands.command(pass_content=True, aliases=['статус', 'status'])
    async def __status(self, ctx, act = None, name = None, url = None):
        if act == None and name == None and url == None:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Версию {settings['version']}"))
            emb = discord.Embed(title = 'Статус Мику', colot = 0x00ff00)
            emb.add_field(name='Подробности:',value='Статус боты был изменён на дефолтный!')
            await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(15)
            await emb.delete()
        elif act == "game":
            if name != None:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="{}".format(name)))
                emb = discord.Embed(title = 'Статус Мику', colot = 0x00ff00)
                emb.add_field(name='Подробности:',value='Статус боты был изменён на \"Играет в {}\"'.format(name))
                await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(15)
                await emb.delete()
            else:
                emb = discord.Embed(title = 'Статус Мику', colot = 0x00ff00)
                emb.add_field(name='Ошибка:',value='Вы не указала навание игры!')
                await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(15)
                await emb.delete()
                return
        elif act == "stream":
            if name != None:
                if url != None:
                    await self.bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Streaming(name=name, url=url))
                    emb = discord.Embed(title = 'Статус Мику', colot = 0x00ff00)
                    emb.add_field(name='Подробности:',value='Статус боты был изменён на \"Стримит {}\"'.format(name))
                    await ctx.send(embed = emb)
                    await ctx.message.delete()
                    await asyncio.sleep(15)
                    await emb.delete()
                else:
                    emb = discord.Embed(title = 'Статус Мику', colot = 0x00ff00)
                    emb.add_field(name='Ошибка:',value='Вы не указали ссылку на стрим!')
                    await ctx.send(embed = emb)
                    await ctx.message.delete()
                    await asyncio.sleep(15)
                    await emb.delete()
                    return
            else:
                emb = discord.Embed(title = 'Статус Мику', colot = 0x00ff00)
                emb.add_field(name='Ошибка:',value='Вы не указали кого мы будем смотреть!')
                await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(15)
                await emb.delete()
                return
        elif act == "Skrip_men":
            await self.bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Streaming(name="Skr1pMen", url="https://www.twitch.tv/Skr1pmen"))
            emb = discord.Embed(title = 'Статус Мику', colot = 0x00ff00)
            emb.add_field(name='Подробности:',value='Статус боты был изменён на \"Стримит Skr1pMen\"')
            await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(15)
            await emb.delete()

#Команда_invite
    @commands.command(pass_context=True, aliases=['инвайт', 'invite'])
    async def __invite(self, ctx, member:discord.Member):
        invitelink = await ctx.channel.create_invite(max_uses=1,unique=True)
        await member.send("Вы были приглашены на сервер! Вот ссылочка на него: {}".format(invitelink))
        await ctx.message.delete()
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Успешно!",value='Пользователю было отправлено сообщение с приглашением на сервер!')
        await ctx.send(embed = emb)

    @__invite.error
    async def __invite_error(ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.invite``:",value="Такого пользоватея нет")
        await ctx.send(embed = emb)
        await ctx.message.delete()

#Команда_youtube
    @commands.command(aliases=['ютуб', 'ют', 'youtube', 'yt'])
    async def __youtube(self, ctx): 
        data = {
            "max_age": 86400,
            "max_uses": 0,
            "target_application_id": 755600276941176913,
            "target_type": 2,
            "temporary": False,
            "validate": None
        }
        headers = {
            "Authorization": f"Bot {settings['token']}",
            "Content-Type": "application/json"
        }
        if ctx.author.voice is not None:
            if ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel.id
            else:
                await ctx.send("Зайдите в канал")
        else:
            await ctx.send("Зайдите в канал")
        response = requests.post(f"https://discord.com/api/v8/channels/{channel}/invites", data=json.dumps(data), headers=headers)
        link = json.loads(response.content)
        await ctx.send(f"https://discord.com/invite/{link['code']}")

#Команда_chess
    @commands.command(aliases=['шахматы', 'chess'])
    async def __chess(self, ctx):
    
        data = {
            "max_age": 86400,
            "max_uses": 0,
            "target_application_id": 832012774040141894,
            "target_type": 2,
            "temporary": False,
            "validate": None
        }
        headers = {
            "Authorization": f"Bot {settings['token']}",
            "Content-Type": "application/json"
        }
    
        if ctx.author.voice is not None:
            if ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel.id
            else:
                await ctx.send("Зайдите в канал")
        else:
            await ctx.send("Зайдите в канал")
    
        response = requests.post(f"https://discord.com/api/v8/channels/{channel}/invites", data=json.dumps(data), headers=headers)
        link = json.loads(response.content)
    
        await ctx.send(f"https://discord.com/invite/{link['code']}")


def setup(bot):
    bot.add_cog(UserCommands(bot))

