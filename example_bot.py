import os, re, discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
serverID = 1 #Changes for each server

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


async def dm_about_roles(member):
    print(f"Dming {member.name}...")

    await member.send(
        f"""Hi {member.name}, welcome to {member.guild.name}!

        Tell us, what year are you?

        **Freshman** :new_moon: 
        **Sophomore** :waning_crescent_moon: 
        **Junior** :last_quarter_moon: 
        **Senior** :full_moon: 

        Reply with the name of the year you are or the emoji associated with it so I can give you the right role, then you can join the party!

        If for whatever reason you want to remove a role from yourself, then reply with a role you currently have so I can remove it for you.
        """
    )

@bot.event
async def on_member_join(member):
    await dm_about_roles(member)

async def assign_roles(message):
    print("Assigning roles...")

    languages = set(re.findall("Freshman|Sophomore|Junior|Senior", message.content, re.IGNORECASE))

    language_emojis = set(re.findall("\U0001F311|\U0001F318|\U0001F317|\U0001F315", message.content))
    # https://unicode.org/emoji/charts/full-emoji-list.html

    # Convert emojis to names
    for emoji in language_emojis:
        {
            "\U0001F311": lambda: languages.add("Freshman"),
            "\U0001F318": lambda: languages.add("Sophomore"),
            "\U0001F317": lambda: languages.add("Junior"),
            "\U0001F315": lambda: languages.add("Senior")
        }[emoji]()

    if languages:
        server = bot.get_guild(serverID)

        # <-- RENAMED VARIABLE + LIST CHANGED TO SET
        new_roles = set([discord.utils.get(server.roles, name=language.lower()) for language in languages])

        member = await server.fetch_member(message.author.id)

        # NEW CODE BELOW
        current_roles = set(member.roles)

        roles_to_add = new_roles.difference(current_roles)
        roles_to_remove = new_roles.intersection(current_roles)

        try:
            await member.add_roles(*roles_to_add, reason="Roles assigned by WelcomeBot.")
            await member.remove_roles(*roles_to_remove, reason="Roles revoked by WelcomeBot.")
        except Exception as e:
            print(e)
            await message.channel.send("Error assigning roles.")
        else:
            if roles_to_add:
                    await message.channel.send(f"You've been assigned the following role{'s' if len(roles_to_add) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_add]) }")

            if roles_to_remove:
                await message.channel.send(f"You've lost the following role{'s' if len(roles_to_remove) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_remove]) }")

    else:
        await message.channel.send("No appropriate year was found in your message.")

@bot.event
async def on_message(message):
    print("Bot sees message...")

    if message.author == bot.user:
        return
    
    
    if isinstance(message.channel, discord.channel.DMChannel):
        await assign_roles(message)
        return


    # manual commands
    if message.content.startswith("!roles"):
        await dm_about_roles(message.author)

    elif message.content.startswith("!serverid"):
        await message.channel.send(message.channel.guild.id)

bot.run('TOKEN HERE')