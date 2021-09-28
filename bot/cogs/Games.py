import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import command
import psycopg2
import random
from discord_components import DiscordComponents,Button,ButtonStyle, component

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
        if coins < 0:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка!',value=f'Ты ввел отрицательное число!')
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
                await Mes.edit(content=f"Ты выбрал Орёл!\nВыпала Орёл!\nТы выйграл {coins*2}",components=[])
                # await responce.respond(content=f"Ты выбрал Орёл!\nВыпала Орёл!\nТы выйграл {coins*2}")
                cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins,ctx.author.id))
            else:
                await Mes.edit(content=f"Ты выбрал Орёл!\nВыпала Решка!\nТы проиграл {coins}",components=[])
                cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(coins,ctx.author.id))
        elif responce.component.id == 'two':
            if side_coin == 1:
                await Mes.edit(content=f"Ты выбрал Решка!\nВыпала Решка!\nТы выйграл {coins*2}",components=[])
                cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins,ctx.author.id))
            else:
                await Mes.edit(content=f"Ты выбрал Решка!\nВыпала Орёл!\nТы проиграл {coins}",components=[])
                cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(coins,ctx.author.id))
        connection.commit()

#Казино
    @commands.command(aliases=['casino','рулетка','казино'])
    async def __casino(self,ctx,number:int=None):
        cursor.execute("SELECT cash FROM cashcasino WHERE server_id = {}".format(ctx.guild.id))
        jeckpot = cursor.fetchone()[0]
        cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
        balance = cursor.fetchone()[0]
        if number is None:
            emb = discord.Embed(
                title = "Мини-Игра: 🎰 Казино",
                description = f"Коротко о правилах:\n\
                    •Начиная игру вы делаете фиксированную ставку в 10:leaves:\n\
                    •Цель игрока отгадать число от 000 до 999, если игрок отдагал число, то он получает Jeckpot\n\
                    •Jeckpot составляет всю сумму которую проиграли предыдущие игроки\n\
                    Jeckpot на данный момент составляет: {jeckpot}:leaves:",
                color = 0x00d166
            )
            await ctx.send(embed = emb,
                components = [
                    Button(style=ButtonStyle.green,label='Начать игру!')
                ])
            
            responce = await self.bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
            if responce.component.label == 'Начать игру!':
                await ctx.send(embed = discord.Embed(description = "Для начала игры пропиши команду .casino и число от 0 до 999",color = 0x00d166))
        else:
            casinoResult = int(random.randint(0,999))
            cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
            resilts = cursor.fetchone()[0]
            if 10 > resilts:
                emb = discord.Embed(color=0xa62019)
                emb.add_field(name='❌ Ошибка!',value=f'Недостаточно денег для ставки!')
                Mes = await ctx.send(embed = emb)
                await ctx.message.delete()
                await asyncio.sleep(30)
                await Mes.delete()
            if number == casinoResult:
                cursor.execute(f"UPDATE users SET cash = cash + {jeckpot} WHERE id = {ctx.author.id}")
                cursor.execute("UPDATE cashcasino SET cash = cash - cahs WHERE server_id = {0}".format(ctx.guild.id))
                cursor.execute("SELECT cash FROM cashcasino WHERE server_id = {}".format(ctx.guild.id))
                jeckpot = cursor.fetchone()[0]
                cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
                balance = cursor.fetchone()[0]
                connection.commit()
                await ctx.send(
                    f"Играет {ctx.suthor.mention}\nТвоё число: {number}\nЧисло которое выпало: {casinoResult}\nПоздравляю, ты выйграл! Ты сорвал Jeckpot в размере: {jeckpot}:leaves:\nТвой баланс составляет: {balance}:leaves:"
                )
            else:
                cursor.execute(f"UPDATE users SET cash = cash - 10 WHERE id = {ctx.author.id}")
                cursor.execute("UPDATE CashCasino SET cash = cash + 10 WHERE server_id = {0}".format(ctx.guild.id))
                cursor.execute("SELECT cash FROM cashcasino WHERE server_id = {}".format(ctx.guild.id))
                jeckpot = cursor.fetchone()[0]
                cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
                balance = cursor.fetchone()[0]
                connection.commit()
                await ctx.send(
                    f"Играет {ctx.suthor.mention}\nТвоё число: {number}\nЧисло которое выпало: {casinoResult}\nСожалею, но ты проиграл!\nСумма Jeckpot'a теперь составляет: {jeckpot}:leaves:\nТвой баланс составляет: {balance}:leaves:"
                )


def setup(bot):
    bot.add_cog(GamesForProgit(bot))