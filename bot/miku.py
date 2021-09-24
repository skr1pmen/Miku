import asyncio
from logging import exception
import discord
from discord.ext import commands
import os
from config import settings
from discord.utils import get


bot = commands.Bot(command_prefix=settings['prefix'], intents = discord.Intents.all())
bot.remove_command('help')

@bot.command(pass_context=True)
async def load(ctx, extension):
    if ctx.author.id == 361154033362403338:
        bot.load_extension(f"cogs.{extension}")
        emb = discord.Embed(title='',color=0x00d166)
        emb.add_field(name='✅ Успешно!',value='Ког загружен.')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(30)
        await Mes.delete()
    else:
        emb = discord.Embed(title='',color=0xa62019)
        emb.add_field(name='❌ Ошибка!',value='Этой командой может пользоваться только разработчик.')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(30)
        await Mes.delete()

@bot.command(pass_context=True)
async def unload(ctx, extension):
    if ctx.author.id == 361154033362403338:
        bot.unload_extension(f"cogs.{extension}")
        emb = discord.Embed(title='',color=0x00d166)
        emb.add_field(name='✅ Успешно!',value='Ког отгружен.')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(30)
        await Mes.delete()
    else:
        emb = discord.Embed(title='',color=0xa62019)
        emb.add_field(name='❌ Ошибка!',value='Этой командой может пользоваться только разработчик.')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(30)
        await Mes.delete()

@bot.command(pass_context=True)
async def reload(ctx, extension):
    if ctx.author.id == 361154033362403338:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        emb = discord.Embed(title='',color=0x00d166)
        emb.add_field(name='✅ Успешно!',value='Ког перезагружен.')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(30)
        await Mes.delete()
    else:
        emb = discord.Embed(title='',color=0xa62019)
        emb.add_field(name='❌ Ошибка!',value='Этой командой может пользоваться только разработчик.')
        Mes = await ctx.send(embed = emb)
        await ctx.message.delete()
        await asyncio.sleep(30)
        await Mes.delete()

for filename in os.listdir('bot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


default_rooms_initted = False
default_room_category_id = 888417923151044608
default_room_creator_id = 888418406469079050

room_category = None
room_creator = None

async def delete_channel(guild, channel_id):
        channel = guild.get_channel(channel_id)
        await channel.delete()

async def create_voice_channel(guild, channel_name):
        channel = await guild.create_voice_channel(channel_name, category=room_category)
        return channel

def init_rooms():
    if default_room_category_id != -1:
        category_channel = bot.get_channel(default_room_category_id)
        if category_channel:
            global room_category
            room_category = category_channel

    if default_room_creator_id != -1:
        create_channel = bot.get_channel(default_room_creator_id)
        if create_channel:
            global room_creator
            room_creator = create_channel
  
    global default_rooms_initted
    default_rooms_initted = True

@bot.command(aliases = ['temp_category_set'])
async def __temp_category_set (ctx, id):
    category_channel = bot.get_channel(int(id))
    if category_channel:
        global room_category
        room_category = category_channel

@bot.command(aliases = ['temp_rooms_set'])
async def __temp_rooms_set (ctx, id):
    create_channel = bot.get_channel(int(id))
    if create_channel:
        global room_creator
        room_creator = create_channel

@bot.event
async def on_voice_state_update(member, before, after):
    if not default_rooms_initted:
        init_rooms()

    if not room_category:
        print("Set 'Temp rooms category' id first (temp_category_set)")
        return False

    if not room_creator:
        print("Set 'Temp rooms creator' id first (temp_rooms_set)")
        return False

    if member.bot:
        return False

    if after.channel == room_creator:
        channel = await create_voice_channel(after.channel.guild, f'Комната {member.name}')
        if channel is not None:
            await member.move_to(channel)
            await channel.set_permissions(member, manage_channels=True)

    if before.channel is not None:
        if before.channel != room_creator and before.channel.category == room_category:
            if len(before.channel.members) == 0:
                await delete_channel(before.channel.guild, before.channel.id)



bot.run(settings['token'])