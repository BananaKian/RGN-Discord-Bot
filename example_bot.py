import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('Hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('Hey'):
        await message.channel.send('Hello!')

    if message.content.startswith('hey'):
        await message.channel.send('Hello!')

client.run('MTE2MjEwNjE1NTc5NjAyMTQ3OQ.GdCZnI.VSuSdPY1mh09NYH8dIMEMnWcCyslEh6XO768Jo')