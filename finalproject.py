import discord
from discord import guild
from discord import embeds
from discord import message
from discord.ext import commands
import random
from typing import ValuesView
import os
import requests
import json
from datetime import datetime

#python3 -m pip install -U discord.py

from discord.ext.commands.core import has_guild_permissions

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = '$',intents=intents)

#bot login commandline notification
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#lockdown command
@client.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
    await ctx.send( ctx.channel.mention + " is now in lockdown.")

#unlock command
@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
    await ctx.send( ctx.channel.mention + " has been unlocked.")

#poll command
@client.command()
async def poll(ctx,*,message):
    emb = discord.Embed(title= " POLL ", description=f"{message}")
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction("👍🏾")
    await msg.add_reaction("👎🏾")

#name change command
@client.command()
async def changename(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

#slowmode command
@client.command()
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode delay has been set to {seconds} seconds.")

#Main Command Hub
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #time command
    datetime_object = datetime.now()
    if message.content.startswith('$time'):
        await message.channel.send(datetime_object)

    #hello command
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    #weather command
    if message.content.startswith('$weather'):
        api_key = "61ec60c7a5179f8a63fccbba684014cf" #my key
        url = "http://api.openweathermap.org/data/2.5/weather?units=imperial"

        #checks if proper formatting was used in command
        try:
            index = message.content.index(" ")
            city_name = message.content[index + 1:]
            complete_url = url + "&appid=" + api_key + "&q=" + city_name

            response = requests.get(complete_url)
            x = response.json()

            #checks if location exists
            if x["cod"] != "404":

                y = x["main"]
                current_temperature = y["temp"]

                current_feelslike = y["feels_like"]

                current_humidity = y["humidity"]

                z = x["weather"]

                weather_description = z[0]["description"]

                await message.channel.send("Temperature (in Fahrenheit): " +
                                str(current_temperature) +
                    "\nFeels Like = " +
                                str(current_feelslike) +
                    "\nHumidity (in percentage): " +
                                str(current_humidity) +
                    "\nDescription: " +
                                str(weather_description))
            else:
                await message.channel.send("City Not Found")
        except BaseException as err:
            await message.channel.send("Proper format: '$weather (city name)' ")
    await client.process_commands(message)


client.run("MTAxMzU4MzIwMjIwOTc2MzQ2MA.GQVIdJ.KAkYC7HFg6NJsla4wN-GkwvLKJZ1ZtOYdSlg1E")