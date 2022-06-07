import asyncio
from itertools import cycle
from operator import setitem
import discord
from discord.embeds import Embed
from discord.ext import commands
import random
from discord.ext.commands.core import has_permissions
import psycopg2
from config import settings
import json
import requests
from PIL import Image, ImageFont, ImageDraw, ImageChops
import io
from discord_components import DiscordComponents,Button,ButtonStyle
# from googletrans import Translator

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
        # self.translator = Translator()
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
                emb.add_field(name='❌ Ошибка команды ``.clear``!',value=f'Ты превысил лимит количества удаляемых сообщений.')
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
    @commands.command(pass_context=True, aliases=['ранд', 'rand'])
    async def __rand(self, ctx, one, two):
        try:
            one= int(one)
            two= int(two)
            arg = random.randint(one,two)
        except ValueError:
            emb = discord.Embed(title= "",color = 0xff0000)
            emb.add_field(name="Ошибка команды ``.rand``:",value="Введены неправильные значения, повтори попытку.")
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
        name,nick,id,status = str(member),member.display_name,str(member.id),str(member.status)
        created_at = member.created_at.strftime("%d.%m.%Y")
        joined_at = member.joined_at.strftime("%d.%m.%Y")
        cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id))
        money = str(cursor.fetchone()[0])
        cursor.execute("SELECT premium FROM users WHERE id = {}".format(member.id))
        prem = cursor.fetchone()[0]
        roles = str(len(member.roles)-1)
        base = Image.open('img/base.png').convert('RGBA')
        background = Image.open('img/bg.png').convert('RGBA')
        pfp = member.avatar_url_as(size = 256)
        data = io.BytesIO(await pfp.read())
        pfp = Image.open(data).convert('RGBA')
        name = f"{name[:13]}..." if len(name)>16 else name
        nick = f"AKA:{nick[:17]}..." if len(nick)>17 else f"AKA:{nick}"
        draw = ImageDraw.Draw(base)
        pfp = circle(pfp,size=(215,215))
        online = Image.open('img/online.png').convert('RGBA')
        offline = Image.open('img/offline.png').convert('RGBA')
        idle = Image.open('img/idle.png').convert('RGBA')
        dnd = Image.open('img/dnd.png').convert('RGBA')
        premImg = Image.open('img/prem.png').convert('RGBA')
        bad_omen = Image.open('img/bad_omen.png').convert('RGBA')

        font = ImageFont.truetype('img/arial.ttf', size=38)
        AKAfont = ImageFont.truetype('img/arial.ttf', size=30)
        subfont = ImageFont.truetype('img/arial.ttf', size=25)
        bad_omen_font = ImageFont.truetype('img/minecraft.ttf', size=46)

        if status == 'online':
            pfp.paste(online,(140,140),online)
        elif status == 'dnd':
            pfp.paste(dnd,(140,140),dnd)
        elif status == 'offline':
            pfp.paste(offline,(140,140),offline)
        elif status == 'idle':
            pfp.paste(idle,(140,140),idle)

        if prem == True:
            background.paste(premImg,(270,175),premImg)

        cursor.execute(f"SELECT bad_omen FROM users WHERE id = {member.id}")
        Bad_Omen = cursor.fetchone()[0]
        offset = 3
        shadowColor = 'black'
        x = 100
        y = 94
        if Bad_Omen == 1:
            bad_omen_lvl="I"
            for off in range(offset):
                draw.text((x-off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
            draw.text((x,y),bad_omen_lvl,font=bad_omen_font)
            background.paste(bad_omen,(0,0),bad_omen)
        elif Bad_Omen == 2:
            bad_omen_lvl="II"
            for off in range(offset):
                draw.text((x-off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
            draw.text((x,y),bad_omen_lvl,font=bad_omen_font)
            background.paste(bad_omen,(0,0),bad_omen)
        elif Bad_Omen == 3:
            bad_omen_lvl="III"
            for off in range(offset):
                draw.text((x-off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
            draw.text((x,y),bad_omen_lvl,font=bad_omen_font)
            background.paste(bad_omen,(0,0),bad_omen)
        elif Bad_Omen == 4:
            bad_omen_lvl="IV"
            for off in range(offset):
                draw.text((x-off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
            draw.text((x,y),bad_omen_lvl,font=bad_omen_font)
            background.paste(bad_omen,(0,0),bad_omen)
        elif Bad_Omen == 5:
            bad_omen_lvl="V"
            for off in range(offset):
                draw.text((x-off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y+off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x-off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
                draw.text((x+off, y-off), bad_omen_lvl, font=bad_omen_font, fill=shadowColor)
            draw.text((x,y),bad_omen_lvl,font=bad_omen_font)
            background.paste(bad_omen,(0,0),bad_omen)

        draw.text((280,240),name,font=font)
        draw.text((275,320),nick,font=AKAfont)

        draw.text((65,490),money,font=subfont)
        draw.text((395,490),roles,font=subfont)

        draw.text((65,618),created_at,font=subfont)
        draw.text((395,618),joined_at,font=subfont)

        draw.text((65,728),id,font=subfont)

        base.paste(pfp,(56,158),pfp)

        background.paste(base,(0,0),base)

        with io.BytesIO() as a:
            background.save(a,"png")
            a.seek(0)
            await ctx.message.delete()
            await ctx.send(file = discord.File(a, "profile.png"))

#Команда_rules
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
        emb.set_author(name="Привет я Мику! Я управляющая этим сервером.\nНе считая skr1pmen и его команды Админов конечно.")
        emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
        await ctx.send('{}, я выслала правила тебе в личку'.format(ctx.author.mention))
        await ctx.author.send(embed = emb)
        await ctx.message.delete()

#Команда_help
    @commands.command(pass_context=True, aliases = ['хелп','help','как'])
    async def __help(self,ctx):
        buttons = [
            [
                Button(style=ButtonStyle.green,label='rules'),
                Button(style=ButtonStyle.green,label='info'),
                Button(style=ButtonStyle.green,label='clear'),
                Button(style=ButtonStyle.green,label='about'),
                Button(style=ButtonStyle.green,label='rand')
            ],
            [
                Button(style=ButtonStyle.green,label='status'),
                Button(style=ButtonStyle.green,label='invite'),
                Button(style=ButtonStyle.green,label='balance'),
                Button(style=ButtonStyle.green,label='shop'),
                Button(style=ButtonStyle.green,label='leaderboard'),
            ],
            [
                Button(style=ButtonStyle.green,label='coin'),
                Button(style=ButtonStyle.green,label='casino'),
                Button(style=ButtonStyle.green,label='convey'),
            ]
        ]
        buttons_adm = [
            [
                Button(style=ButtonStyle.green,label='rules'),
                Button(style=ButtonStyle.green,label='info'),
                Button(style=ButtonStyle.green,label='clear'),
                Button(style=ButtonStyle.green,label='about'),
                Button(style=ButtonStyle.green,label='rand')
            ],
            [
                Button(style=ButtonStyle.green,label='status'),
                Button(style=ButtonStyle.green,label='invite'),
                Button(style=ButtonStyle.green,label='balance'),
                Button(style=ButtonStyle.green,label='shop'),
                Button(style=ButtonStyle.green,label='leaderboard'),
            ],
            [
                Button(style=ButtonStyle.green,label='coin'),
                Button(style=ButtonStyle.green,label='casino'),
                Button(style=ButtonStyle.green,label='convey'),
                Button(style=ButtonStyle.green,label='ban'),
                Button(style=ButtonStyle.green,label='banlist'),
            ],
            [
                Button(style=ButtonStyle.green,label='unban'),
                Button(style=ButtonStyle.green,label='kick'),
                Button(style=ButtonStyle.green,label='mute')
            ]
        ]
        emb = discord.Embed(
            title = 'Список команд',
            description = "Ниже представлены кнопки со всеми командами на сервере. Нажав на кнопку, вы сможете увидеть подробности про команду.",
            color = 0xffff00
        )
        if ctx.message.author.guild_permissions.administrator:
            Mes = await ctx.send(embed = emb,components=buttons_adm)
            await ctx.message.delete()
            await asyncio.sleep(60)
            await Mes.delete()
        else:
            Mes = await ctx.send(embed = emb,components=buttons)
            await ctx.message.delete()
            await asyncio.sleep(60)
            await Mes.delete()

        while True:
            responce = await self.bot.wait_for('button_click')
            if responce.component.label == 'rules':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="rules/правила",value="Мику отправит список всех правил в личку")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'info':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="info/инфо",value="Муки выведет карточку с информацией о любом пользователе")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'clear':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="clear/чист",value="Команда для удаления лишних сообщений (доступна частникам с ролью 🔰 Бог и выше)")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'about':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="about/ктоты",value="Мику расскажет немного о себе в лс")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'rand':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="rand/ранд",value="Выдача рандомного числа в заданных пользователем рамках")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'status':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="status/статус",value="Присвоение Мику кастомного статуса")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'invite':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="invite/инвайт",value="Приглашения участников на сервер по его ID")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'balance':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="balance/баланс",value="Команда выведет баланс любого пользователя на сервере")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'shop':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="shop/магазин",value="Вывод магазина ролей доступных для покупки")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'leaderboard':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="leaderboard/лидерборд",value="Вывод топ 10 самых богатых участников сервера")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'coin':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="coin/монетка",value="Мини-Игра \"Монетка\" для заработка баланса")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'casino':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="casino/рулетка/казино",value="Мини-Игра \"🎰 Казино\" для заработка баланса")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'convey':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="convey/передать",value="Команда для перевода денег между пользователями")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'ban':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="ban/бан",value="Бан пользователя ``.ban @user``")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'banlist':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="banlist/банлист",value="Выдаст список забаненных людей в лс")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'unban':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="unban/разбан",value="Разбан участника ``.unban {@user}``")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'kick':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="kick/кик",value="Удаление участника сервера с возможностью вернуться вновь ``.kick {@user}``")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()
            elif responce.component.label == 'mute':
                emb = discord.Embed(title= "",color = 0xffff00)
                emb.add_field(name="mute/мут",value="Выдача мута пользователю на определённое время (в минутах) ``.kick {@user} {time}``")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                Mes = await ctx.send(embed = emb)
                await asyncio.sleep(60)
                await Mes.delete()

#Команда_about
    @commands.command(pass_context=True, aliases=['ктоты', 'about'])
    async def __about(self, ctx):
        emb= discord.Embed(title="",color = 0x00bfff)
        emb.set_author(name= "Мику Хацунэ\nHatsune Miku", url="https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BA%D1%83_%D0%A5%D0%B0%D1%86%D1%83%D0%BD%D1%8D")
        emb.add_field(name="1.Кто ты ?",value="Я японская виртуальная певица, созданная компанией Crypton Future Media 31 августа 2007 года.\nШутка, на самом деле я Бот созданный для управления сервером SSquad")
        emb.add_field(name="2.Зачем ты нужна ?",value="Как я уже сказала, я нужна для помощи в управлении сервером skr1pmen")
        emb.add_field(name="3.Когда создана ?",value="Моей официальной датой создания является 8 марта 2019\n(вот я вас мужиков трести в 2 раза больше буду в марте)...Хехе...мда неловко получилось")
        emb.add_field(name="4.Кто тебя написал и на каком языке ?",value="Я была написана skr1pmen'ом, на языке Python")
        emb.add_field(name="__Версия бота:__",value=f"{settings['version']}")
        emb.add_field(name="__Помощь в создании:__",value="alex_jonas,Southpaw,STRAYKERRR")

        emb.set_thumbnail(url= "https://raw.githubusercontent.com/SkripMen/mikubotskripmen/master/%D0%90%D0%92%D0%90%D0%A2%D0%90%D0%A0%D0%9C%D0%98%D0%9A%D0%A3.png")
        emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
        await ctx.author.send(embed = emb)
        await ctx.message.delete()

#Команда_status
    @commands.command(pass_content=True, aliases=['статус', 'status'])
    async def __status(self, ctx, act = None, name = None, url = None):
        if act == None and name == None and url == None:
            if settings['debug'] == True:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=settings['versionDebug']))
                emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
                emb.add_field(name='Подробности:',value='Статус боты был изменён на дефолтный!')
                mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(15)
                await mes.delete()
            else:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Версию {}".format(settings['version'])))
                emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
                emb.add_field(name='Подробности:',value='Статус боты был изменён на дефолтный!')
                mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(15)
                await mes.delete()
        elif act == "game" or act == "игра":
            if name != None:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="{}".format(name)))
                emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
                emb.add_field(name='Подробности:',value='Статус боты был изменён на \"Играет в {}\"'.format(name))
                mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(15)
                await mes.delete()
            else:
                emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
                emb.add_field(name='Ошибка:',value='Вы не указала название игры!')
                mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(15)
                await mes.delete()
                return
        elif act == "stream" or act == "стрим":
            if name != None:
                if url != None:
                    await self.bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Streaming(name=name, url=url))
                    emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
                    emb.add_field(name='Подробности:',value='Статус боты был изменён на \"Смотрит {}\"'.format(name))
                    mes = await ctx.send(embed = emb)
                    await ctx.message.delete()
                    await asyncio.sleep(15)
                    await mes.delete()
                else:
                    emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
                    emb.add_field(name='Ошибка:',value='Вы не указали ссылку на стрим!')
                    mes = await ctx.send(embed = emb)
                    await ctx.message.delete()
                    await asyncio.sleep(15)
                    await mes.delete()
                    return
            else:
                emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
                emb.add_field(name='Ошибка:',value='Вы не указали кого мы будем смотреть!')
                mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(15)
                await mes.delete()
                return
        elif act == "skr1pmen":
            await self.bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Streaming(name="Skr1pMen", url="https://www.twitch.tv/skr1pmen"))
            emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
            emb.add_field(name='Подробности:',value='Статус боты был изменён на \"Смотрит skr1pmen\"')
            mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(15)
            await mes.delete()
        elif act == "southpaw" or act == "Southpaw":
            await self.bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Streaming(name="Skr1pMen", url="https://www.twitch.tv/southpaworlefty"))
            emb = discord.Embed(title = 'Статус Мику', color = 0x00ff00)
            emb.add_field(name='Подробности:',value='Статус боты был изменён на \"Смотрит Southpaw\"')
            mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(15)
            await mes.delete()

#Команда_invite
    @commands.command(pass_context=True, aliases=['инвайт', 'invite'])
    async def __invite(self, ctx, member:discord.Member ):
        invitelink = await ctx.channel.create_invite(max_uses=1,unique=True)
        await member.send("Вы были приглашены на сервер! Вот ссылочка на него: {}".format(invitelink))
        await ctx.message.delete()
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Успешно!",value='Пользователю было отправлено сообщение с приглашением на сервер!')
        await ctx.send(embed = emb)

    @__invite.error
    async def __invite_error(self, ctx, error):
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

#Команда_translate
    # @commands.command(aliases=['tr','перевод','translate'])
    # async def trans (self, ctx, lang,*, args):
    #     try:
    #         translator = Translator()
    #         o = translator.translate(f'{args}', dest = f'{lang}')
    #     except Exception as e:
    #         # обработка исключения
    #         em = discord.Embed(title = 'Ошибка при переводе.')
    #         em.add_field(name = 'Текст ошибки', value = str(e), inline = False)
    #     else:
    #         em = discord.Embed(title = 'Переводчик.')
    #         em.add_field(name = 'Оригинал текста:', value = f'{args}', inline = False)
    #         em.add_field(name = f'Перевод ({lang}):', value = f'{o.text}', inline = False)
    #     await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(UserCommands(bot))

