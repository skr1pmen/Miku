import asyncio
import discord
from discord.ext import commands
from config import settings

class AdministrationCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

#Команда_ban
    @commands.command(pass_context=True, aliases=['бан', 'ban'])
    @commands.has_permissions(ban_members=True)
    async def __ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Вам бан!",value="{} был успешно забанен".format(user.name))
        emb.set_thumbnail(url= "https://i.gifer.com/fzm0.gif")
        await ctx.send(embed = emb)
        await ctx.message.delete()
        if reason == None:
            msg = f"{ctx.author.mention} выдал бан {user.mention}, по причине \"Не указано\"."
        else:
            msg = f"{ctx.author.mention} выдал бан {user.mention}, по причине \"{reason}\"."
        channel = self.bot.get_channel(settings['logChannel'])
        await channel.send(msg)

    @__ban.error
    async def __ban_error(self, ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.ban``:",value="У вас недостаточно прав или такого пользователя нет")
        await ctx.send(embed = emb)
        await ctx.message.delete()

#Команда_unban
    @commands.command(pass_context=True, aliases=['разбан', 'unban'])
    @commands.has_permissions(administrator=True)
    async def __unban(self, ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Великая пощада!",value="{} был успешно разбанен".format(user.name))
        await ctx.send(embed = emb)
        await ctx.message.delete()
        msg = f"{ctx.author.mention} разбанил {user.mention}."
        channel = self.bot.get_channel(settings['logChannel'])
        await channel.send(msg)

    @__unban.error
    async def __unban_error(self, ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.unban``:",value="У вас недостаточно прав или такого пользователя нет")
        await ctx.send(embed = emb)
        await ctx.message.delete()

#Команда_banlist
    @commands.command(aliases=['банлист', 'banlist'])
    # @commands.has_permissions(administrator=True)
    async def __banlist(self, ctx):
        guild = ctx.guild
        bans = await guild.bans()
        emb = discord.Embed(title= "Список забаненых участников сервера:",color = 0x00ff00)
        for ban in bans:
            user = ban.user
            reason = ban.reason
            if reason == None:
                emb.add_field(name=f"{user}",value=f"**Причина бана:** Нет данных!\n**ID:** {user.id}",inline = False)
            else:
                emb.add_field(name=f"{user}",value=f"**Причина бана:** {reason}!\n**ID:** {user.id}",inline = False)
        emb.set_footer(text="Все права защищены Miku©", icon_url= self.bot.user.avatar_url )
        await ctx.author.send(embed = emb)
        await ctx.message.delete()

    @__banlist.error
    async def __banlist_error(self, ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.banlist``:",value="У вас недостаточно прав")
        await ctx.send(embed = emb)
        await ctx.message.delete()

#Команда_kick
    @commands.command(pass_context=True, aliases=['кик', 'kick'])
    @commands.has_permissions(administrator=True)
    async def __kick(self, ctx, member:discord.Member):
        invitelink = await ctx.channel.create_invite(max_uses=1,unique=True)
        await member.send(invitelink)
        await ctx.guild.kick(member)
        await ctx.message.delete()
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Пошёл отдохнуть:",value="{} был кикнут с сервера, и ему выслано приглашение на сервер".format(member))
        await ctx.send(embed = emb)
        msg = f"{ctx.author.mention} кикнул {member.mention}."
        channel = self.bot.get_channel(settings['logChannel'])
        await channel.send(msg)

    @__kick.error
    async def __kick_error(self, ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.kick``:",value="У вас недостаточно прав или такого пользователя нет")
        await ctx.send(embed = emb)
        await ctx.message.delete()

#Команда_mute
    @commands.command(aliases=['мут', 'mute'])
    @commands.has_permissions(administrator=True)
    async def __mute(self, ctx, user: discord.Member, time: int):
        role = user.guild.get_role(874610184692072478)
        await ctx.message.delete()
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Помолчи ка:",value=f'{user} получил мут на {time} минут')
        await ctx.send(embed = emb)
        msg = f"{ctx.author.mention} заткнул {user.mention} на {time} минут."
        channel = self.bot.get_channel(settings['logChannel'])
        await channel.send(msg)
        await user.add_roles(role)
        await user.move_to(None)
        await asyncio.sleep(time * 60)
        await user.remove_roles(role)
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Научился говорить:",value=f'{user} наконец-то нашёл кнопку включения микрофона')
        await ctx.send(embed = emb)
        msg = f"{user.mention} научился говорить после того как {ctx.author.mention} заткнул его."
        channel = self.bot.get_channel(settings['logChannel'])
        await channel.send(msg)
        

    @__mute.error
    async def __mute_error(self, ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.mute``:",value="У вас недостаточно прав или такого пользователя нет")
        await ctx.send(embed = emb)
        await ctx.message.delete()

# #Команда_mes
#     @commands.command(aliases=['mes', 'сообщение','message'])
#     @commands.has_permissions(administrator=True)
#     async def __mess(self, ctx, role: discord.Role, *, message):
#         for member in ctx.message.guild.members:
#             if role in member.roles:
#                 await self.bot.send(member, message)


def setup(bot):
    bot.add_cog(AdministrationCommands(bot))