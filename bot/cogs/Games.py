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

    @commands.command(aliases = ['coin','монетка'])
    async def __coin(self,ctx,coins:int=None):
        if coins is None:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка!',value=f'Ты не поставил ставку!')
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(30)
            await Mes.delete()
            return
        cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id))
        resilts = cursor.fetchone()[0]
        if coins > resilts:
            emb = discord.Embed(color=0xa62019)
            emb.add_field(name='❌ Ошибка!',value=f'Недостаточно денег для ставки!')
            Mes = await ctx.send(embed = emb)
            await ctx.message.delete()
            await asyncio.sleep(30)
            await Mes.delete()
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

        
def setup(bot):
    bot.add_cog(GamesForProgit(bot))