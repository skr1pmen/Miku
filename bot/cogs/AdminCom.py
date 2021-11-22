import asyncio
import discord
from discord.ext import commands

class AdministrationCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

#Команда_ban
    @commands.command(pass_context=True, aliases=['бан', 'ban'])
    @commands.has_permissions(administrator=True)
    async def __ban(ctx, user: discord.Member):
        await user.ban()
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Вам бан!",value="{} был успешно забанен".format(user.name))
        emb.set_thumbnail(url= "https://i.gifer.com/fzm0.gif")
        await ctx.send(embed = emb)
        await ctx.message.delete()

    @__ban.error
    async def __ban_error(ctx, error):
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

    @__unban.error
    async def __unban_error(ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.unban``:",value="У вас недостаточно прав или такого пользователя нет")
        await ctx.send(embed = emb)
        await ctx.message.delete()

#Команда_banlist
    @commands.command(aliases=['банлист', 'banlist'])
    @commands.has_permissions(administrator=True)
    async def __banlist(self, ctx):
        guild = ctx.guild
        bans = await guild.bans()
        emb = discord.Embed(title= "Список забаненых участников сервера:",color = 0x00ff00)
        for ban in bans:
            emb.add_field(name="◙",value=ban[1:])
        await ctx.author.send(embed = emb)
        await ctx.message.delete()

    @__banlist.error
    async def __banlist_error(ctx, error):
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

    @__kick.error
    async def __kick_error(ctx, error):
        emb = discord.Embed(title= "",color = 0xff0000)
        emb.add_field(name="Ошибка команды ``.kick``:",value="У вас недостаточно прав или такого пользователя нет")
        await ctx.send(embed = emb)
        await ctx.message.delete()

#Команда_mute
    @commands.command(aliases=['мут', 'mute'])
    @commands.has_permissions(administrator=True)
    async def __mute(self, ctx, user: discord.Member, time: int):
        role = user.guild.get_role(874610184692072478)
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Помолчи ка:",value=f'{user} получил мут на {time} минут')
        await ctx.send(embed = emb)
        await user.add_roles(role)
        await user.move_to(None)
        await asyncio.sleep(time * 60)
        await user.remove_roles(role)
        emb = discord.Embed(title= "",color = 0x00ff00)
        emb.add_field(name="Научился говорить:",value=f'{user} наконец-то нашёл кнопку включения микрофона')
        await ctx.send(embed = emb)

    @__mute.error
    async def __mute_error(ctx, error):
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