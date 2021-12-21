import asyncio
import discord
from discord import message
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import command
from discord_components.dpy_overrides import send
import psycopg2
import random
from discord_components import DiscordComponents,Button,ButtonStyle, component
import json

#Для_Городов
# def parse_city_json(json_file='bot/textFile/russia.json'):
def parse_city_json(json_file='bot/textFile/cities.json'):
    p_obj = None
    try:
        js_obj = open(json_file, "r", encoding="utf-8")
        p_obj = json.load(js_obj)
    except Exception as err:
        print(err)
        return None
    finally:
        js_obj.close()   
    return [city['city'].lower() for city in p_obj]
def get_city(city):
    normilize_city = city.strip().lower()
    # if is_correct_city_name(normilize_city):
    if get_city.previous_city != "" and normilize_city[0] != get_city.previous_city[-1]:
        return 'Город должен начинаться на "{0}"!'.format(get_city.previous_city[-1])

    if normilize_city not in cities_already_named:
        cities_already_named.add(normilize_city)
        last_latter_city = normilize_city[-1]
        proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
        if proposed_names:
            for city in proposed_names:
                if city not in cities_already_named:
                    cities_already_named.add(city)
                    get_city.previous_city = city
                    return city.capitalize()
        return 'rip'
    else:
        return 'repeat'
    # else:
    #     return 'incorrect'
get_city.previous_city = "" 
# def is_correct_city_name(city):
#     return city[-1].isalpha() and city[-1] not in ('ь', 'ъ')
def refresh():
    cities = parse_city_json()[:1000]
    cities_already_named = set()
cities = parse_city_json()[:1000]  # города которые знает бот
cities_already_named = set()  # города, которые уже называли

class GamesForProgit(commands.Cog):

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

#Монетка
    @commands.command(aliases = ['coin','монетка'])
    async def __coin(self,ctx,coins:int=None):
        if coins <= 0:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка!',value=f'Ты ввел 0 или отрицательное число листочков!')
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(30)
            await Mes.delete()
            return False
        if coins is None:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка!',value=f'Ты не поставил ставку!')
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(30)
            await Mes.delete()
            return False
        cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
        resilts = cursor.fetchone()[0]
        if coins > resilts:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка!',value=f'Недостаточно денег для ставки!')
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(30)
            await Mes.delete()
            return False
        cursor.execute(f"SELECT premium FROM users WHERE id = {ctx.author.id}")
        isPremium = cursor.fetchone()[0]
        Mes = await ctx.send(
            f'Ты поставил {coins} :leaves:\nВыбери сторону монетки.',
            components = [
                Button(style=ButtonStyle.green,label='Орёл',id='one'),
                Button(style=ButtonStyle.green,label='Решка',id='two')
            ])
        side_coin = random.randint(1,2)
        responce = await self.bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
        if responce.component.id == 'one':
            if side_coin == 1:
                await Mes.edit(content=f"Ты выбрал Орёл!\nВыпала Орёл!\nТы выиграл {coins*2}",components=[])
                cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins,ctx.author.id))
                if isPremium == True:
                    cursor.execute("UPDATE users SET spent = spent + {0} WHERE id = {1}".format(coins, ctx.author.id))
            else:
                await Mes.edit(content=f"Ты выбрал Орёл!\nВыпала Решка!\nТы проиграл {coins}",components=[])
                cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(coins,ctx.author.id))
                if isPremium == True:
                    cursor.execute("UPDATE users SET spent = spent + {0} WHERE id = {1}".format(coins, ctx.author.id))
        elif responce.component.id == 'two':
            if side_coin == 1:
                await Mes.edit(content=f"Ты выбрал Решка!\nВыпала Решка!\nТы выиграл {coins*2}",components=[])
                cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins,ctx.author.id))
                if isPremium == True:
                    cursor.execute("UPDATE users SET spent = spent + {0} WHERE id = {1}".format(coins, ctx.author.id))
            else:
                await Mes.edit(content=f"Ты выбрал Решка!\nВыпала Орёл!\nТы проиграл {coins}",components=[])
                cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(coins,ctx.author.id))
                if isPremium == True:
                    cursor.execute("UPDATE users SET spent = spent + {0} WHERE id = {1}".format(coins, ctx.author.id))
        connection.commit()

#Казино
    @commands.command(aliases=['casino','рулетка','казино'])
    async def __casino(self,ctx,number:int=None):
        cursor.execute("SELECT cash FROM cashcasino WHERE server_id = {}".format(ctx.guild.id))
        Jackpot = cursor.fetchone()[0]
        cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
        balance = cursor.fetchone()[0]
        if number is None:
            emb = discord.Embed(
                title = "Мини-Игра: 🎰 Казино",
                description = f"Коротко о правилах:\n\
                    •Начиная игру вы делаете фиксированную ставку в 10:leaves:\n\
                    •Цель игрока отгадать число от 000 до 999, если игрок отдагал число, то он получает Jackpot\n\
                    •Jackpot составляет всю сумму которую проиграли предыдущие игроки\n\
                    Jackpot на данный момент составляет: {Jackpot}:leaves:",
                color = 0x00d166
            )
            await ctx.send(embed = emb,
                components = [
                    Button(style=ButtonStyle.green,label='Начать игру!')
                ])
            await ctx.message.delete()
            
            responce = await self.bot.wait_for('button_click')
            if responce.component.label == 'Начать игру!':
                await ctx.send(embed = discord.Embed(description = "Для начала игры пропиши команду .casino и число от 0 до 999",color = 0x00d166))
        elif number < 0:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка!',value=f'Необходимо число от 0 до 999!')
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(30)
            await Mes.delete()
            return False
        elif number > 999:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка!',value=f'Необходимо число от 0 до 999!')
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(30)
            await Mes.delete()
            return False
        else:
            casinoResult = int(random.randint(0,999))
            cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
            resilts = cursor.fetchone()[0]
            cursor.execute(f"SELECT premium FROM users WHERE id = {ctx.author.id}")
            isPremium = cursor.fetchone()[0]
            if 10 > resilts:
                emb = discord.Embed(color=0xa62019)
                emb.add_field(name='❌ Ошибка!',value=f'Недостаточно денег для ставки!')
                Mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(30)
                await Mes.delete()
                return False
            if number == casinoResult:
                cursor.execute(f"UPDATE users SET cash = cash + {Jackpot} WHERE id = {ctx.author.id}")
                cursor.execute("UPDATE cashcasino SET cash = cash - cahs WHERE server_id = {0}".format(ctx.guild.id))
                cursor.execute("SELECT cash FROM cashcasino WHERE server_id = {}".format(ctx.guild.id))
                Jackpot = cursor.fetchone()[0]
                cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
                balance = cursor.fetchone()[0]
                if isPremium == True:
                    cursor.execute("UPDATE users SET spent = spent + 10 WHERE id = {0}".format(ctx.author.id))
                connection.commit()
                await ctx.send(
                    f"Играет {ctx.author.mention}\nТвоё число: {number}\nЧисло которое выпало: {casinoResult}\nПоздравляю, ты выйграл! Ты сорвал Jackpot в размере: {Jackpot}:leaves:\nТвой баланс составляет: {balance}:leaves:"
                )
                await ctx.message.delete()
            else:
                cursor.execute(f"UPDATE users SET cash = cash - 10 WHERE id = {ctx.author.id}")
                cursor.execute("UPDATE CashCasino SET cash = cash + 10 WHERE server_id = {0}".format(ctx.guild.id))
                cursor.execute("SELECT cash FROM cashcasino WHERE server_id = {}".format(ctx.guild.id))
                Jackpot = cursor.fetchone()[0]
                cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
                balance = cursor.fetchone()[0]
                if isPremium == True:
                    cursor.execute("UPDATE users SET spent = spent + 10 WHERE id = {0}".format(ctx.author.id))
                connection.commit()
                await ctx.send(
                    f"Играет {ctx.author.mention}\nТвоё число: {number}\nЧисло которое выпало: {casinoResult}\nСожалею, но ты проиграл!\nСумма Jackpot'a теперь составляет: {Jackpot}:leaves:\nТвой баланс составляет: {balance}:leaves:"
                )
                await ctx.message.delete()

#Города
    @commands.command(aliases=['города','city'])
    async def __city(self,ctx):
        coins = 0
        await ctx.channel.purge(limit=1)
        await ctx.send("Введи название города для начала игры. Если уже наигрался напиши ``.стоп``")
        while True:
            message_respose = await self.bot.wait_for('message', check=lambda m: m.author== ctx.author)
            message = str(message_respose.content)
            if ctx.author == self.bot.user:
                return
            if message_respose.content.lower() == "стоп":
                await ctx.channel.purge(limit=coins*2+2)
                await ctx.send(f"Игра закончена. Ты получил {coins*5} :leaves:")
                cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins*5,ctx.author.id))
                refresh()
                return False
            else:
                response = get_city(message)
                if response == "rip":
                    await ctx.channel.purge(limit=coins*2+2)
                    await ctx.send(f"Ты победил {ctx.author.mention}. Я не знаю города да данную букву. Ты выйграл {coins*5} :leaves:")
                    cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins*5,ctx.author.id))
                    refresh()
                    return False
                elif response == "repeat":
                    await ctx.send("Город уже был. Повторите попытку.")
                elif response == "incorrect":
                    await ctx.send("Некорректное название города. Повторите попытку.")
                else:
                    await ctx.send(f"{response}")
                    coins+=1
            connection.commit()

def setup(bot):
    bot.add_cog(GamesForProgit(bot))