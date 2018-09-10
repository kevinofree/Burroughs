# Work with Python 3.6
import discord
from discord.ext import commands
import youtube_dl
import json

#load configuration from json file
with open('config.json') as f:
    config = json.load(f)

#connect to discord
client = discord.Client()
#remove default help command
client = commands.Bot(command_prefix = '!')
client.remove_command('help')
songQueue = []

#Events
#====================================================================================================
@client.event
async def on_ready():
    print('Logged in as username: {} and id: {}'.format(client.user.name, client.user.id))

@client.event
async def on_message(message):
    if message.author != client.user:
        await client.process_commands(message)

#Commands
#====================================================================================================
@client.command(pass_context=True)
async def help(ctx):
    #Print out all the basic commands for the bot
    msg = str("```\nUtilities:\n"
                    +"!help                         prints out all the commands the bot can do.\n"
                    +"!hello                        Say hello to bot.\n"
                    +"!echo [message]               Bot repeats everything after command.\n"
                    +"!ping                         Bot responds back to ping.\n"
                    +"Music:\n"
                    +"!join                         Summons bot into voice channel.\n"
                    +"!leave                        Makes bot leave voice channel.\n"
                    +"!songrequest [url]            Add a youtube link to the songQueue.\n"
                    +"!play/!pause/!resume          Change state of song  .\n"
                    +"!skip                         skip current song  .\n"
                    +"!queue                        Prints # remaining songs in queue  .\n"
                    +"!songname                     Prints current song.\n"
                    +"```")
    await client.send_message(ctx.message.channel, msg)

@client.command(pass_context=True)
async def echo(ctx, *args):
    #Echo a message from user
    if args[0] == "-s":
        await client.send_message(discord.Object(id='426898544754950149'), " ".join(args[1::]))
    else:
        await client.say(" ".join(args))

@client.command(pass_context=True)
async def hello(ctx):
    #Greets user when hello command is used
    msg = 'Hello, {0}. Im Burroughs, a navigational AI.'.format(ctx.message.author.mention)
    await client.send_message(ctx.message.channel, msg)

@client.command(pass_context=True)
async def ping(ctx):
    #Responds to ping command
    await client.say("Pong!")

#Voice chat controls
#====================================================================================================
@client.command(pass_context=True)
async def join(ctx):
    #joins voice channel
    await client.say("Voice chat joined")
    channel = ctx.message.author.voice.voice_channel
    try:
        await client.join_voice_channel(channel)
    except Exception as e:
        pass

@client.command(pass_context=True)
async def leave(ctx):
    #leaves voice channel
    await client.say("Left the voice channel")
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


#Music playback functions
#====================================================================================================
@client.command()
async def play():
    songQueue[0][0].start()

@client.command()
async def pause():
    songQueue[0][0].pause()

@client.command()
async def skip():
    songQueue[0][0].stop()

@client.command()
async def resume():
    songQueue[0][0].resume()

@client.command()
async def queue():
    if len(songQueue) == 0:
        await client.say("Song queue is empty")
    else:
        await client.say("Songs remaining in queue: {}".format(len(songQueue)))

def next():
    old = songQueue.pop(0)
    if songQueue != []:
        songQueue[0][0].start()
    else:
        print("Ran out of songs")

@client.command(aliases=['sn'])
async def songname():
    if songQueue != []:
        await client.say(songQueue[0][1])
    else:
        client.say("Queue empty.")

@client.command(pass_context=True, aliases=['sr'])
async def songrequest(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: next())
    if len(songQueue) == 0:
        songQueue.append(tuple([player,url]))
        await client.say("Song added to queue in position 1")
        songQueue[0][0].start()
    elif len(songQueue) == 5:
        await client.say("Queue is full. Song could not be added")
    else:
        songQueue.append(tuple([player,url]))
        await client.say("Song added to queue in  position {}.".format(len(songQueue)))

client.run(config["token"])
