import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import command
import psycopg2
import random
from discord_components import DiscordComponents,Button,ButtonStyle

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
        await ctx.send(
            f'Ты поставил {coins} :leaves:\nВыбери сторону монетки.',
            components = [
                Button(style=ButtonStyle.green,label='Орёл',id='one'),
                Button(style=ButtonStyle.green,label='Решка',id='two')
            ])
        side_coin = random.randint(1,2)
        responce = await self.bot.wait_for('button_click')
        if responce.channel == ctx.channel:
            if responce.component.id == 'one':
                if side_coin == 1:
                    await responce.respond(content=f"Ты выбрал Орёл!\nВыпала Орёл!\nТы выйграл {coins*2}")
                    cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins,ctx.author.id))
                else:
                    await responce.respond(content=f"Ты выбрал Орёл!\nВыпала Решка!\nТы проиграл {coins}")
                    cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(coins,ctx.author.id))
            elif responce.component.id == 'two':
                if side_coin == 1:
                    await responce.respond(content=f"Ты выбрал Решка!\nВыпала Решка!\nТы выйграл {coins*2}")
                    cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins,ctx.author.id))
                else:
                    await responce.respond(content=f"Ты выбрал Решка!\nВыпала Орёл!\nТы проиграл {coins}")
                    cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(coins,ctx.author.id))
        connection.commit()

    # @commands.command(aliases=['удача','luck'])
    # async def __coin(self,ctx,side:int=None,coins:int=None):
    #     coin_side = random.randint(1,2)
    #     if side is None:
    #         emb = discord.Embed(color=0xa62019)
    #         emb.add_field(name='❌ Ошибка!',value=f'Ты не указал число от 1 до 2!')
    #         Mes = await ctx.send(embed = emb)
    #         await ctx.message.delete()
    #         await asyncio.sleep(30)
    #         await Mes.delete()
    #         return
    #     if coins is None:
    #         emb = discord.Embed(color=0xa62019)
    #         emb.add_field(name='❌ Ошибка!',value=f'Ты не поставил ставку!')
    #         Mes = await ctx.send(embed = emb)
    #         await ctx.message.delete()
    #         await asyncio.sleep(30)
    #         await Mes.delete()
    #         return
    #     cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(coins,ctx.author.id))
    #     connection.commit()
    #     mes = await ctx.send(f"Ты выбрал:{side}\nЯ бросаю монетку.")
    #     await asyncio.sleep(0.8)
    #     await mes.edit(content=f"Ты выбрал:{side}\nЯ бросаю монетку..")
    #     await asyncio.sleep(0.8)
    #     await mes.edit(content=f"Ты выбрал:{side}\nЯ бросаю монетку...")
    #     await asyncio.sleep(0.8)
    #     if 1 == side:
    #         if coin_side == 1:
    #             await mes.edit(content=f"Ты выбрал:{side}\nВыпало: {coin_side}.\nТы выйграл{coins*2}")
    #             cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins*2,ctx.author.id))
    #             connection.commit()
    #         else:
    #             await mes.edit(content=f"Ты выбрал:{side}\nВыпало: {coin_side}.\nТы проиграл{coins}")
    #     if 2 == side:
    #         if coin_side == 2:
    #             await mes.edit(content=f"Ты выбрал:{side}\nВыпало: {coin_side}.\nТы выйграл{coins*2}")
    #             cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins*2,ctx.author.id))
    #             connection.commit()
    #         else:
    #             await mes.edit(content=f"Ты выбрал:{side}\nВыпало: {coin_side}.\nТы проиграл{coins}")

        # coin_side = random.randint(1,2)
        # side = side.lower()
        # if side is None:
        #     emb = discord.Embed(color=0xa62019)
        #     emb.add_field(name='❌ Ошибка!',value=f'Ты не указал сторону монетки, на которую ставишь!')
        #     Mes = await ctx.send(embed = emb)
        #     await ctx.message.delete()
        #     await asyncio.sleep(30)
        #     await Mes.delete()
        #     return
        # if coins is None:
        #     emb = discord.Embed(color=0xa62019)
        #     emb.add_field(name='❌ Ошибка!',value=f'Ты не поставил ставку!')
        #     Mes = await ctx.send(embed = emb)
        #     await ctx.message.delete()
        #     await asyncio.sleep(30)
        #     await Mes.delete()
        #     return
        # # cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(coins,ctx.author.id))
        # mes = await ctx.send(f"Ты выбрал:{side}\nЯ бросаю монетку.")
        # await asyncio.sleep(0.8)
        # await mes.edit(content=f"Ты выбрал:{side}\nЯ бросаю монетку..")
        # await asyncio.sleep(0.8)
        # await mes.edit(content=f"Ты выбрал:{side}\nЯ бросаю монетку...")
        # await asyncio.sleep(0.8)
        # if side
        # if side == coin_side: 
        #     await mes.edit(content=f"Ты выбрал:{side}\nВыпало: {coin_side}.\nТы выйграл{coins*2}")
        #     cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(coins*2,ctx.author.id))
        # else: 
        #     await mes.edit(content=f"Ты выбрал:{side}\nВыпало: {coin_side}.\nТы проиграл{coins}")


        
def setup(bot):
    bot.add_cog(GamesForProgit(bot))