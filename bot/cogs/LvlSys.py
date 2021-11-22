import asyncio
import discord
from discord import embeds
from discord import channel
from discord.ext import commands,tasks
from discord.ext.commands.core import command
import psycopg2
from datetime import datetime
import threading
import random
import json
import string

class StastUsers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    global connection
    global cursor
    connection = psycopg2.connect(
        dbname='d7npuuht675g6t',
        user='dfelpwutbrsdwj',
        password='84d0cfdcf95f22787066edbc6cac37e900a64943ad8629d9ad30e325c6e797cc',
        host='ec2-44-198-223-154.compute-1.amazonaws.com')
    cursor = connection.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            name TEXT,
            id BIGINT,
            cash BIGINT,
            server_id BIGINT
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS shop(
            role_id INT,
            id INT,
            cost BIGINT            
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS CashCasino(
            cash BIGINT,
            server_id BIGINT
        )""")
        
        for guild in self.bot.guilds:
            for member in guild.members:
                cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
                results = cursor.fetchone()
                if not member.bot:
                    if results is None:
                        cursor.execute(f"INSERT INTO users VALUES ('{member}','{member.id}',0,'{guild.id}')")
                    else:
                        pass
            cursor.execute(f"SELECT cash FROM CashCasino WHERE server_id = {guild.id}")
            serverCash = cursor.fetchone()
            if serverCash is None:
                cursor.execute(f"INSERT INTO CashCasino VALUES (0,'{guild.id}')")
            else:
                pass
        connection.commit()
        print("База данный загружена!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
        results = cursor.fetchone()
        if not member.bot:
            if results is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}','{member.id}',0,'{member.guild.id}')")
                connection.commit()
            else:
                pass

    @commands.Cog.listener()
    async def on_message(self,message):
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

        amount = len(message.content) // 10
        if message.content[0] != ".":
            if not message.author.bot:
                if amount >= 30:
                    cursor.execute(f"UPDATE users SET cash = cash + 30 WHERE id = {message.author.id}")
                else:
                    cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                connection.commit()

#Команда_balance
    @commands.command(aliases = ['balance','cash','баланс'])
    async def __balance(self,ctx,member:discord.Member = None):
        if member is None:
            cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
            results = cursor.fetchone()[0]
            await ctx.send(embed = discord.Embed(
                description = f"""Баланс пользователя **{ctx.author.mention}** составляет: **{results}** :leaves:"""
            ))
            await ctx.message.delete()
        else:
            cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id))
            results = cursor.fetchone()[0]
            await ctx.send(embed = discord.Embed(
                description = f"""Баланс пользователя **{member.mention}** составляет: **{results}** :leaves:"""
            ))
            await ctx.message.delete()

#Команда_give
    @commands.command(pass_context=True, aliases=['give', 'выдать'])
    @commands.has_permissions(administrator=True)
    async def __give(self, ctx, member: discord.Member=None, amount:int=None):
        if member is None:
            await ctx.send(f"{ctx.author.mention}, укажи пользователя, которому нужно зачислить :leaves:.")
            await ctx.message.delete()
        else:
            if amount is None:
                await ctx.send(f"{ctx.author.mention}, ты не указал, сколько :leaves: выдать.")
                await ctx.message.delete()
            elif amount < 0:
                await ctx.send(f"{ctx.author.mention}, укажи число больше 0.")
                await ctx.message.delete()
            else:
                cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {member.id}")
                connection.commit()
                await ctx.message.add_reaction('✅')
    @__give.error
    async def __give_error(self, ctx, error):
        emb = discord.Embed(color=0xa62019)
        emb.add_field(name='❌ Ошибка команды ``.give``!',value=f'У вас недостаточно прав!')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(10)
        await Mes.delete()  
    
#Команда_add-shop
    @commands.command(pass_context=True, aliases=['add-shop','добавить-роль'])
    @commands.has_permissions(administrator=True)
    async def __add_shop(self, ctx, role: discord.Role=None, cost: int = None):
        if role is None:
            await ctx.send(f"{ctx.authot.mention}, укажите роль, для добавления в магазин.")
            await ctx.message.delete()
        else:
            if cost is None:
                await ctx.send(f"{ctx.author.mention}, укажите стоимость роли.")
                await ctx.message.delete()
            elif cost < 0:
                await ctx.send(f"{ctx.author.mention}, вы задали отрицательное число стоимости. Давай по новой.")
                await ctx.message.delete()
            else:
                cursor.execute(f"INSERT INTO shop VALUES ({role.id},{ctx.guild.id},{cost})")
                connection.commit()
                await ctx.message.delete()
                await ctx.send(embed=discord.Embed(description = "Роль добавлена в магазин!"))
    @__add_shop.error
    async def __add_shop_error(self, ctx, error):
        emb = discord.Embed(color=0xa62019)
        emb.add_field(name='❌ Ошибка команды ``.add_shop``!',value=f'У вас недостаточно прав!')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(10)
        await Mes.delete()

#Команда_remove-shop
    @commands.command(pass_context=True, aliases=['remove-shop','удалить-роль'])
    @commands.has_permissions(administrator=True)
    async def __remove_shop(self, ctx, role: discord.Role=None):
        if role is None:
            await ctx.send(f"{ctx.authot.mention}, укажите роль, для удаления из магазина.")
            await ctx.message.delete()
        else:
            cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
            connection.commit()
            await ctx.message.delete()
            await ctx.send(embed=discord.Embed(description = "Роль удалена из магазина!"))
    @__remove_shop.error
    async def __remove_shop_error(self, ctx, error):
        emb = discord.Embed(color=0xa62019)
        emb.add_field(name='❌ Ошибка команды ``.remove_shop``!',value=f'У вас недостаточно прав!')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(10)
        await Mes.delete()

#Команда_shop
    @commands.command(pass_context=True, aliases=['shop','магазин'])
    async def __shop(self, ctx):
        embed = discord.Embed(title="Магазин ролей",color=0x00d166)
        cursor.execute("SELECT role_id, cost FROM shop WHERE id = %s", [ctx.guild.id])
        for row in cursor.fetchall():
            if ctx.guild.get_role(row[0]) != None:
                embed.add_field(
                    name = f"Роль  ``{ctx.guild.get_role(row[0])}``",
                    value = f"Стоимость роли: {row[1]} :leaves:",
                    inline = False
                )
        embed.set_footer(text="Для покупки роли необходимо вести команду .buy @role, где @role это название роли")
        await ctx.send(embed = embed)
        await ctx.message.delete()
    
#Команда_buy
    @commands.command(pass_context=True, aliases=['buy','купить'])
    async def __buy(self, ctx, role: discord.Role = None):
        # rolelist = [547109093907628046,547398893579665421,547399773322346508]
        if role is None:
            await ctx.send(f"{ctx.authot.mention}, укажите роль, для покупки.")
            await ctx.message.delete()
        else:
            cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id))
            resilts_one = cursor.fetchone()[0]
            cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
            resilts_two = cursor.fetchone()[0]
            if role in ctx.author.roles:
                await ctx.send(f"{ctx.author.mention}, у вас уже имеется данная роль")
            elif resilts_one > resilts_two:
                await ctx.send(f"{ctx.author.mention}, у тебя недостаточно средст для покупки данной роли")
                await ctx.message.delete()
            else:
                # if any(role.id in rolelist for role in ctx.message.author.roles):
             #     await ctx.author.remove_roles(rolelist)
                # await ctx.author.edit(roles = [])
                await ctx.author.add_roles(role)
                await ctx.message.delete()
                cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(resilts_one, ctx.author.id))
                await ctx.send(embed=discord.Embed(description = "✅ Покупка прошла успешно!", color = 0x00d166))

#Команда_leaderboard
    @commands.command(aliases = ['leaderboard', 'лидерборд'])
    async def __leaderboard(self,ctx):
        embed = discord.Embed(title = 'Топ 10 сервера', color = 0x00d166)
        counter = 0
        cursor.execute("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id))
        resilt = cursor.fetchall()
        for row in resilt:
            counter += 1
            embed.add_field(
                name = f'# {counter} | ``{row[0]}``',
                value = f'Баланс: {row[1]} :leaves:',
                inline = False
            )
    
        await ctx.send(embed = embed)

#Команда_convey
    @commands.command(aliases = ['convey','передать'])
    async def __convey(self, ctx, member: discord.Member=None, amount:int=None):
        if member is None:
            Mes = await ctx.send(f"{ctx.author.mention}, укажи пользователя, которому хотите передать :leaves:.")
            await ctx.message.delete()
            await asyncio.sleep(10)
            await Mes.delete()
        elif member is ctx.author:
            Mes = await ctx.send(embed=discord.Embed(description = "❌ Ты не можешь перевести деньги самому себе!", color = 0xa62019))
            await ctx.message.delete()
            await asyncio.sleep(10)
            await Mes.delete()
        else:
            cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
            resilts_one = cursor.fetchone()[0]
            if amount is None:
                Mes = await ctx.send(f"{ctx.author.mention}, ты не указал, сколько :leaves: передать.")
                await ctx.message.delete()
                await asyncio.sleep(10)
                await Mes.delete()
            elif amount <= 0:
                Mes = await ctx.send(f"{ctx.author.mention}, укажи число больше 0.")
                await ctx.message.delete()
                await asyncio.sleep(10)
                await Mes.delete()
            elif resilts_one >= amount:
                cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {member.id}")
                cursor.execute(f"UPDATE users SET cash = cash - {amount} WHERE id = {ctx.author.id}")
                connection.commit()
                await ctx.send(embed=discord.Embed(description = "✅ Перевод прошёл успешно!", color = 0x00d166))
                await ctx.message.delete()
            elif amount >= resilts_one:
                Mes = await ctx.send(embed=discord.Embed(description = "❌ У тебя недостаточно денег!", color = 0xa62019))
                await ctx.message.delete()
                await asyncio.sleep(10)
                await Mes.delete()
        

def checkTime():
    threading.Timer(1, checkTime).start()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    currentDay = datetime.now().day

    if(current_time == '04:00:00'):
        print('Баллы били отправлены')
        cursor.execute(f"UPDATE users SET cash = cash + 10")
    if currentDay == 1 and current_time == '04:00:00':
        print("Jeckpot был увеличен!")
        cursor.execute("UPDATE cashcasino SET cash = cash + cash")
    connection.commit()
        
checkTime()

def setup(bot):
    bot.add_cog(StastUsers(bot))