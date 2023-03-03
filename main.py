import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
from discord import Embed

# Load .env file with the bot token
load_dotenv()


# Retrieve the secure token from the .env file
TOKEN = os.getenv('TOKEN')


# Initialize the Discord API client for our bot
client = discord.Client(intents=discord.Intents.default())


# Read the show data file as a data frame
# Column names: title, dj_names, time, day, description, genre
# Note: Not every field in an example is defined
show_data = pd.read_csv('winter23_shows.csv', keep_default_na=False)


# Example of a show:
# title                                            1-800-HOT-READS
# dj_names                                     DJ Squid Giant Axon
# time                                                    11:00 AM
# day                                                       Friday
# description    1-800-HOT-READS will review and discuss books ...
# genres                                                     Other


# When the program starts this message will be printed to the console
@client.event
async def on_ready():
   print(f"{client.user} has logged in to Discord")
   # Start the send_message task so that a message
   # is sent every 30 seconds
   announce_show.start()


# Checks whether there's a show at the start of
# each hour and sends a message if there is one
# TODO: change seconds=30 to hours=1
@tasks.loop(minutes=1)
async def announce_show():
   now = datetime.now()
   current_time = now.strftime("%I:%M %p")  # Get the current time, e.g. 12:09 AM
   today_name = now.strftime("%A")  # Get the current day of the week, e.g. Thursday
   
   #embed = discord.Embed(title='show title')
   #embed.add_field(name='dj name', value = "show description")
   #channel = client.get_channel(1070113608358441030)
   #await channel.send(embed=embed)

   # message
   for _, row in show_data.iterrows():
      if row["day"] == today_name and row["time"] == current_time:
         # des = row['description']
         # if not row['description']:
         #    print("empty")
         if row['description']: #if row description is not empty
            #print(row['description'])
            print(f"{row['title']} hosted by {row['dj_names']} has just begun! {row['description']} Tune in now!")
            embed = discord.Embed(title=f"{row['title']}")
            embed.add_field(name=f"{row['dj_names']}", value = f"{row['description']} Tune in now!")
            channel = client.get_channel(1070113608358441030)
            await channel.send(embed=embed)
            #await channel.send(f"{row['title']} hosted by {row['dj_names']} has just begun! {row['description']} Tune in now!")
         else: #row description is empty
            print(f"{row['title']} hosted by {row['dj_names']} has just begun! Tune in now!")
            embed = discord.Embed(title=f"{row['title']}")
            embed.add_field(name=f"{row['dj_names']}", value = "Tune in now!")
            channel = client.get_channel(1070113608358441030)
            await channel.send(embed=embed)
   
      #elif row["day"] == today_name:
         #print("currday: " + today_name + " currtime: " + current_time + row["day"] + " " + row["time"])
                 #await channel.send("Current Time = " + current_time)
   # TODO: for each show in show_data that is on today_name, check if the hour roughly matches current_time
   # TODO: if it does, send a nicely formatted message that announces a show


   # Get the #shows channel (the argument is its ID)
   # channel = client.get_channel(1070113608358441030)
   # await channel.send("Day = " + str(today_name))
   # await channel.send("Current Time = " + current_time)

# Run the bot with its token
client.run(TOKEN)
