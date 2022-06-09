import asyncio
import discord
import math
from discord import embeds
from discord import channel
from discord.ext import commands,tasks
from discord.ext.commands.core import command
from discord.message import Message
import psycopg2
from datetime import datetime
import threading
import random
import json
import string
from discord.utils import get
from dislash import *
from config import settings

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
            premium BOOLEAN,
            cash BIGINT,
            spent BIGINT,
            server_id BIGINT,
            warns BIGINT,
            bad_omen BIGINT
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS shop(
            role_id BIGINT,
            id BIGINT,
            cost BIGINT,
            item_type TEXT           
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
                        cursor.execute(f"INSERT INTO users VALUES ('{member}','{member.id}',false,0,0,'{guild.id}',0,0)")
                    else: pass
            cursor.execute(f"SELECT cash FROM CashCasino WHERE server_id = {guild.id}")
            serverCash = cursor.fetchone()
            if serverCash is None:
                cursor.execute(f"INSERT INTO CashCasino VALUES (0,'{guild.id}')")
            else:pass
        connection.commit()
        print("База данный загружена!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
        results = cursor.fetchone()
        if not member.bot:
            if results is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}','{member.id}',0,'{member.guild.id},0,0')")
                connection.commit()
            else:pass

    @commands.Cog.listener()
    async def on_message(self,message):
        OffMat = ["Или мне кажется, или ты матюкнулся {}?\nНадеюсь показалось, а то забаню!","Я конечно не профессионалка, но мне показалось что ты материшься {}","Не используй таких слов, хорошо {}?"]

        # if 'габе жив' in message.content.lower():
        #     await message.channel.send("Габе Рип!!!")
        #     await asyncio.sleep(60)

        # if 'мику рип' in message.content.lower():
        #     await message.channel.send("Сам Рип, так же как и Габе!!!")
        #     await asyncio.sleep(60)

        if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.content.split(' ')}.intersection(set(json.load(open('bot/textFile/cenz.json')))) != set():
            role = message.author.guild.get_role(874610184692072478)

            cursor.execute(f"UPDATE users SET warns = warns + 1 WHERE id = {message.author.id}")
            
            Mes = await message.channel.send(random.choice(OffMat).format(message.author.mention))

            cursor.execute(f"SELECT warns FROM users WHERE id = {message.author.id}")
            Warns = cursor.fetchone()[0]
            cursor.execute(f"SELECT bad_omen FROM users WHERE id = {message.author.id}")
            Bad_Omen = cursor.fetchone()[0]

            if Warns >= 5 and Bad_Omen == 0:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")
                
                emb=discord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 5 минут", value="Причина: Мат", inline=False)
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 5 минут."
                channel = self.bot.get_channel(settings['logChannel'])
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(5 * 60)
                await message.author.remove_roles(role)  
            elif Warns >= 5 and Bad_Omen == 1:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")
                
                emb=discord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 15 минут", value="Причина: Мат", inline=False)
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 15 минут."
                channel = self.bot.get_channel(settings['logChannel'])
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(15 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 5 and Bad_Omen == 2:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")
                
                emb=discord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 30 минут", value="Причина: Мат", inline=False)
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 30 минут."
                channel = self.bot.get_channel(settings['logChannel'])
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(30 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 5 and Bad_Omen == 3:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")
                
                emb=discord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 1 час", value="Причина: Мат", inline=False)
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 1 час."
                channel = self.bot.get_channel(settings['logChannel'])
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(60 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 5 and Bad_Omen == 4:
                cursor.execute(f"UPDATE users SET bad_omen = bad_omen + 1 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")
                
                emb=discord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан мут на 1 сутки", value="Причина: Мат", inline=False)
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                await message.author.send(embed=emb)

                msg = f"Мику заткнула {message.author.mention} на 1 сутки."
                channel = self.bot.get_channel(settings['logChannel'])
                await channel.send(msg)

                await message.author.add_roles(role)
                await message.author.move_to(None)
                await asyncio.sleep(24 * 60 * 60)
                await message.author.remove_roles(role)
            elif Warns >= 10 and Bad_Omen == 5:
                cursor.execute(f"UPDATE users SET bad_omen = 0 WHERE id = {message.author.id}")
                cursor.execute(f"UPDATE users SET warns = 0 WHERE id = {message.author.id}")
                
                emb=discord.Embed(title="Оповещение от Мику!", description="Мут", color=0xff0000)
                emb.add_field(name="Вам был выдан бан", value="Причина: Мат", inline=False)
                emb.set_image(url= "https://thumbs.gfycat.com/AcceptableAgitatedBarbet-size_restricted.gif")
                emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
                await message.author.send(embed=emb)

                await message.author.ban(reason="Мат")

                msg = f"Мику выдала бан {message.author.mention}, по причине \"Мат\"."
                channel = self.bot.get_channel(settings['logChannel'])
                await channel.send(msg)

                emb = discord.Embed(title= "",color = 0x00ff00)
                emb.add_field(name="Вам бан!",value="{} был успешно забанен Мику".format(message.author.name))
                emb.set_image(url= "https://thumbs.gfycat.com/AcceptableAgitatedBarbet-size_restricted.gif")
                await message.channel.send(embed = emb)
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

        try:
            amount = len(message.content) // 10
            if message.content[0] != settings['prefix']:
                if not message.author.bot:
                    godRole = message.guild.get_role(547399773322346508)
                    gamerRole = message.guild.get_role(888113637561090080)
                    ourRole = message.guild.get_role(547398893579665421)
                    if amount >=30:
                        cursor.execute(f"UPDATE users SET cash = cash + 30 WHERE id = {message.author.id}")
                    elif godRole in message.author.roles: #Для богов
                        amount = round(amount*1.5)
                        cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                    elif gamerRole in message.author.roles: #Для геймеров
                        amount = round(amount*1.3)
                        cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                    elif ourRole in message.author.roles: #Для наших людей
                        amount = round(amount*1.2)
                        cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                    else:
                        cursor.execute(f"UPDATE users SET cash = cash + {amount} WHERE id = {message.author.id}")
                    connection.commit() 
        except:pass

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
    # @commands.command(pass_context=True, aliases=['add-shop','добавить-роль'])
    # @commands.has_permissions(administrator=True)
    # async def __add_shop(self, ctx, role: discord.Role=None, cost: int = None):
    #     if role is None:
    #         await ctx.send(f"{ctx.authot.mention}, укажите роль, для добавления в магазин.")
    #         await ctx.message.delete()
    #     else:
    #         if cost is None:
    #             await ctx.send(f"{ctx.author.mention}, укажите стоимость роли.")
    #             await ctx.message.delete()
    #         elif cost < 0:
    #             await ctx.send(f"{ctx.author.mention}, вы задали отрицательное число стоимости. Давай по новой.")
    #             await ctx.message.delete()
    #         else:
    #             cursor.execute(f"INSERT INTO shop VALUES ({role.id},{ctx.guild.id},{cost})")
    #             connection.commit()
    #             await ctx.message.delete()
    #             await ctx.send(embed=discord.Embed(description = "Роль добавлена в магазин!"))
    # @__add_shop.error
    # async def __add_shop_error(self, ctx, error):
    #     emb = discord.Embed(color=0xa62019)
    #     emb.add_field(name='❌ Ошибка команды ``.add_shop``!',value=f'У вас недостаточно прав!')
    #     Mes = await ctx.send(embed = emb)
    #     await ctx.message.delete()
    #     await asyncio.sleep(10)
    #     await Mes.delete()

#Команда_remove-shop
    # @commands.command(pass_context=True, aliases=['remove-shop','удалить-роль'])
    # @commands.has_permissions(administrator=True)
    # async def __remove_shop(self, ctx, role: discord.Role=None):
    #     if role is None:
    #         await ctx.send(f"{ctx.authot.mention}, укажите роль, для удаления из магазина.")
    #         await ctx.message.delete()
    #     else:
    #         cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
    #         connection.commit()
    #         await ctx.message.delete()
    #         await ctx.send(embed=discord.Embed(description = "Роль удалена из магазина!"))
    # @__remove_shop.error
    # async def __remove_shop_error(self, ctx, error):
    #     emb = discord.Embed(color=0xa62019)
    #     emb.add_field(name='❌ Ошибка команды ``.remove_shop``!',value=f'У вас недостаточно прав!')
    #     Mes = await ctx.send(embed = emb)
    #     await ctx.message.delete()
    #     await asyncio.sleep(10)
    #     await Mes.delete()

#Команда_shop
    @commands.command(pass_context=True, aliases=['shop','магазин'])
    async def __shop(self, ctx):
        embed = discord.Embed(title="Магазин",color=0x00d166)
        cursor.execute("SELECT item_num, role_id, cost, item_type, description FROM shop WHERE server_id = {0}".format(ctx.guild.id))
        buttons = []
        for row in cursor.fetchall():
            if row[3] == "role":
                embed.add_field(
                    name = f"Товар: ``{ctx.guild.get_role(row[1])}``",
                    value = f"Стоимость: {row[2]} :leaves:"
                )
                buttons.append(Button(style=ButtonStyle.green,custom_id = f"{row[0]}",label=f'{ctx.guild.get_role(row[1])}')),
            else:
                embed.add_field(
                    name = f"Товар: ``{row[4]}``",
                    value = f"Стоимость: {row[2]} :leaves:"
                )
                buttons.append(Button(style=ButtonStyle.green,custom_id = f"{row[0]}",label=f'{row[4]}'))
        mes = await ctx.send(embed = embed,components=buttons)
        await ctx.message.delete()

        while True:
            responce = await self.bot.wait_for('button_click')
            responce = await ctx.wait_for_button_click(check=check)
            num = responce.component.custom_id
            cursor.execute("SELECT item_type FROM shop WHERE item_num = {0}".format(num))
            itemType = cursor.fetchone()[0]
            cursor.execute("SELECT cost FROM shop WHERE item_num = {0}".format(num))
            cost = cursor.fetchone()[0]
            cursor.execute("SELECT role_id FROM shop WHERE item_num = {0}".format(num))
            role = ctx.guild.get_role(cursor.fetchone()[0])
            author = responce.author
            cursor.execute(f"SELECT premium FROM users WHERE id = {author.id}")
            isPremium = cursor.fetchone()[0]
            cursor.execute(f"SELECT cash FROM users WHERE id = {author.id}")
            cash = cursor.fetchone()[0]
            cursor.execute(f"SELECT bad_omen FROM users WHERE id = {author.id}")
            Bad_Omen = cursor.fetchone()[0]

            if cost <= cash:
                if itemType == "sub":
                    if isPremium == True:
                        await responce.reply(f"{author.mention}, у вас уже имеется премиум подписка.")
                    if isPremium == False:
                        cursor.execute(f"UPDATE users SET premium = true WHERE id = {author.id}")
                        cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cost, author.id))
                        await responce.reply(embed=discord.Embed(description = "✅ Покупка прошла успешно!", color = 0x00d166))
                        msg = f"{author.mention} преобрёл \"Премиум подписку\"."
                        channel = self.bot.get_channel(settings['logChannel'])
                        await channel.send(msg)
                elif itemType == "role":
                    if role in author.roles:
                        await responce.reply(f"{author.mention}, у вас уже имеется данная роль.")
                    else:
                        await author.add_roles(role)
                        cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cost, author.id))
                        if isPremium == True:
                            cursor.execute("UPDATE users SET spent = spent + {0} WHERE id = {1}".format(cost, author.id))
                        await responce.reply(embed=discord.Embed(description = "✅ Покупка прошла успешно!", color = 0x00d166))
                        msg = f"{author.mention} преобрёл роль: \"{role}\"."
                        channel = self.bot.get_channel(settings['logChannel'])
                        await channel.send(msg)
                elif itemType == "bad_omen":
                    if Bad_Omen == 0:
                        await responce.reply(f"{author.mention}, у вас 0 уровень предупреждений.")
                    if Bad_Omen >= 1:
                        if isPremium == True:
                            cursor.execute("UPDATE users SET spent = spent + {0} WHERE id = {1}".format(cost, author.id))
                        cursor.execute(f"UPDATE users SET bad_omen = bad_omen - 1 WHERE id = {author.id}")
                        cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cost, author.id))
                        await responce.reply(embed=discord.Embed(description = "✅ Покупка прошла успешно!", color = 0x00d166))
                        msg = f"{author.mention} преобрёл \"Понижение уровня предупреждения\"."
                        channel = self.bot.get_channel(settings['logChannel'])
                        await channel.send(msg)
                await mes.delete()
            else:
                await responce.reply(f"{author.mention}, у тебя недостаточно средст для покупки данного товара")
                await mes.delete()
                
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
        await ctx.message.delete()
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
                msg = f"{ctx.author.mention} перевёл {member.mention} {amount} :leaves:."
                channel = self.bot.get_channel(settings['logChannel'])
                await channel.send(msg)
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

    if(current_time == '00:00:00'):
        print('Баллы били отправлены')
        cursor.execute(f"UPDATE users SET cash = cash + 10")
    if currentDay == 1 and current_time == '00:00:00':
        print("Jackpot был увеличен!")
        cursor.execute("UPDATE cashcasino SET cash = cash + cash")
        print("Кешбек был возвращен")
        cursor.execute(f'UPDATE users SET cash = cash + spent * 0.04')
        cursor.execute(f'UPDATE users SET spent = 0')
    connection.commit()
        
checkTime()

def setup(bot):
    bot.add_cog(StastUsers(bot))