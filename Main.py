import discord
from discord.ext import commands
import requests
import json
from discord import Embed

#Initialize the bot. Utilizing commands just imported and discord package. Give prefects that the bot will listen out for on the discord sever. The bot detects prefect (e.g. !) and then looks for the command after. If user typed !hello, a programmed bot might type hi. ! says call and hello is the fucntion being called

intents = discord.Intents.default()
intents.typing = False #You can set individual intents to True or False based on your reqs
intents.members = True

#Enable the message content intent 
intents.message_content = True

# initialized bot with prefect/ intents
client = commands.Bot(command_prefix = '!', intents=intents)

#Add on event
@client.event
async def on_ready():  #on ready function - when  bot is ready to start receiving commmands, will execute function.
    print("The bot is now ready for use.")   #want to know when bot is ready. User wont see
    print("-------------------------------") #useful for debugging 

@client.command()
async def hello(ctx): #name of function that user types in chat to run function. ctx says take input from discord
    await ctx.send("Hello, I am the youtube bot")

# #Now need to link this bot up to web app which created in discord developer. tell this code wht app to link to


@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye, hope you have a good rest of your day")


#Going to make it so that the bot detects when someone new enters and waves at them and tells a joke. detects when leave too
@client.event #Defining an event
async def on_member_join(member): #Calling an on member join event 
    jokeurl = "https://dad-jokes7.p.rapidapi.com/dad-jokes/joke-of-the-day"
    headers = {
        "X-RapidAPI-Key": "795b830386msh55c805d0d69f102p169894jsnebec8474ea46",
        "X-RapidAPI-Host": "dad-jokes7.p.rapidapi.com"
    }
    response = requests.get(jokeurl, headers=headers)
    channel = client.get_channel(1161381888078925926)
    joke_data = json.loads(response.text)
    joke = joke_data.get('joke', 'No joke available')
    source = "Source: " + joke_data.get('source', 'Unknown')
    await channel.send("Welcome to the server newcomer! Here is a dad joke: ")
    await channel.send(joke) #send the joke
    await channel.send(source) #send the source

@client.event
async def on_member_remove(member): #When user leaves, will run this function
    channel = client.get_channel(1161381888078925926)
    await channel.send("Goodbye! Sad to see you leaving!")

#Attempting embed anouncements. Set up so if user send a specfic message, the bot will detect the word dog and reply with an embed
@client.command()
async def embed(ctx):   #function named embed
    #make sure url has http or https at the beginning with ://. 
    embed = discord.Embed(title="Go Bucs!", url="https://www.etsu.edu/ehome/", description = "ETSU Homepage", color=0x0066cc) #Used W3Schools color picker. Need to add 0x before the hex
    #author = ctx.author
    embed.set_author(name=ctx.author.display_name, url="https://www.etsualumni.org/s/974/bp18/interior.aspx?sid=974&gid=1&pgid=1222", icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/0/0b/Appalachian_Mountains_wallpaper.jpg")
    #name is just for title name, title of a field. 
    embed.add_field(name="Fall 2023", value="Week 8", inline=TRUE)
    #tell bot to send embed to chat
    await ctx.send(embed=embed)
    

#Goes at the end
client.run("") #tells bot to run. Goes through script and then starts running it. Need token. Do NOT share TOKEN ever