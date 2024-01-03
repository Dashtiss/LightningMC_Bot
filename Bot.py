import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import difflib
from discord.ui import Button, View

# ---------|||||||Variables||||||-----------------
CommitNumber = "1"
Testing = True
# Sets up all the variables
lastNumber = 0
HighestNumber = 0
HasHitHighest = False
lastUsers = ""
UsersButtonPushed = {}

# Sets if these systems will  be online
CountingSystem = False
ClickingSystem = False

# will set the reason why it is disabled
DisabledReason = "Bot is Undergoing major updates and the system your trying to use is down for maintenance"

# Load or create UsersButtonPushed dictionary from a JSON file
if os.path.exists("saves.json"):
    with open("saves.json", "r") as file:
        saves = json.load(file)
        lastNumber = saves["LastNumber"]
        HighestNumber = saves["HighestNumber"]
        lastUsers = saves["LastUser"]
        UsersButtonPushed = saves["UsersButtonPushed"]
# Set up Discord intents for specific events
intents = discord.Intents.all()
LightningMC = None
# Load environment variables from .env file
load_dotenv()

# Enumerate channel types
Types = discord.ChannelType

# List to store words
words = []

# Dictionary to store Discord text channels by name
# Change this to your Discord channel ids
DiscordTextChannels = {
    'staff-chat': 1010722709354844230,
    'admin-stuff': 1138990105386819724,
    'bots': 1011794713361260544,
    "clickertest": 1190345552978776094,
    "count": 1190410937233047662
    # Add more channels as needed
}

# Sets up the bot with Discord.ext.commands.Bot
bot = commands.Bot(intents=intents, command_prefix="$")


# ---------|||||||Extra Functions||||||-----------------
def GetText() -> str:
    """
    Generate a string with user button press information.

    Returns:
    - str: User button press information.
    """
    text = ""
    for key, value in UsersButtonPushed.items():
        text += f"{key} has pressed the button {value} {'times' if value > 1 else 'time'}\n"
    return text


class CounterButton(Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.success, label='Click me!')
        self.count = 0

    async def callback(self, interaction: discord.Interaction):
        global UsersButtonPushed
        user_who_pressed = interaction.user
        try:
            UsersButtonPushed[str(user_who_pressed.name)] += 1
        except KeyError:
            UsersButtonPushed[str(user_who_pressed.name)] = 1
        text = GetText()
        text += f"{user_who_pressed.mention} pressed the button last"
        await interaction.response.edit_message(
            content=text,
            view=self.view)


class CounterView(View):
    def __init__(self):
        super().__init__()
        self.add_item(CounterButton())


def CheckName(message: str):
    """
    Check if the message starts with specific prefixes indicating different roles.

    Args:
    - message (str): The message content.

    Returns:
    - bool: True if the message starts with specific prefixes, False otherwise.
    """
    prefixes = ["[Member]", "[Admin]", "[VIP]", "[MVP]", "[Owner]"]
    return any(message.startswith(prefix) for prefix in prefixes)


def is_similar_to_word(word, word_list, threshold=0.8):
    """
    Check if a word is similar to any word in a list using Ratcliff/Obershelp similarity.

    Parameters:
        word (str): The word to check for similarity.
        word_list (list): The list of words to compare against.
        threshold (float): The similarity threshold. Defaults to 0.8.

    Returns:
        bool: True if a similar word is found, False otherwise.
    """
    for existing_word in word_list:
        similarity = difflib.SequenceMatcher(None, word, existing_word).ratio()
        if similarity >= threshold:
            return True

    return False


# ---------||||||Discord Bot Functions||||||-----------------
@bot.event
async def on_ready():
    global LightningMC
    """
    Event handler when the bot is ready.

    Prints information about connected servers and channels.
    """
    print(f'{bot.user} has connected to Discord!     {bot.status}')
    if Testing:
        await bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Game("Getting new features added to me")
        )
    else:
        game = discord.Game("on Lightning-MC.net")
        await bot.change_presence(status=discord.Status.online, activity=game)
    LightningMC = bot.get_guild(1010718669577408533)
    BotDiscordChannel = bot.get_channel(DiscordTextChannels["bots"])
    embed = discord.Embed(
        title="Status",
        description=f"Checks\nIs Testing: ✅\n"
                    f"Systems online:"
                    f"Counting: {CountingSystem}"
                    f"Clicking: {ClickingSystem}",
        color=0x58fe75  # You can customize the color using hexadecimal
    )
    await BotDiscordChannel.send(content=f"{bot.user.name} is online")
    await BotDiscordChannel.send(embed=embed)

    guild = bot.get_guild(1010718669577408533)
    channel = guild.get_channel(DiscordTextChannels["clickertest"])
    async for message in channel.history(limit=100):
        await message.delete()
    if ClickingSystem:
        counter_view = CounterView()
        message = await channel.send(GetText(), view=counter_view)
        counter_view.message = message
    else:
        embed = discord.Embed(
            title="Clicking System is disabled",
            description=f"Clicking system is offline \nReason: {DisabledReason}",
            color=0xff0000  # You can customize the color using hexadecimal
        )
        await channel.send(embed=embed)


@bot.event
async def on_message(message: discord.Message):
    global lastNumber, lastUsers, HasHitHighest, HighestNumber
    if str(message.content).startswith("!"):
        msg = str(message.content)
        if msg.startswith("!help"):
            pass
        elif msg.startswith("!check-api"):
            await message.reply(content="API is not available right now")
        elif msg.startswith("!clear-button"):
            global UsersButtonPushed
            await message.channel.send("Clearing Button")
            UsersButtonPushed = {}
            print("clearing button")
        elif msg.startswith("!SetNumber"):
            content = msg.split(" ")
            try:
                SetNumber = int(content[1])
            except ValueError:
                await message.reply("Error, Could not turn that into a int")
            lastNumber = SetNumber
            await message.delete()
        elif msg.startswith("!ResetNumber"):
            lastNumber = 0
            Embed = discord.Embed(
                title="Reset",
                description="A Admin has reset the number back to 1",
                color=0xff0000
            )
            bots = bot.get_channel(DiscordTextChannels['count'])
            await bots.send(embed=Embed)
            await message.delete()
    if CountingSystem:
        if message.channel.name == "count":
            try:
                number = int(str(message.content))
            except ValueError:
                return
            if number - 1 == lastNumber and str(message.author.name) != lastUsers:
                await message.add_reaction('✅')

                lastNumber = number
                if lastNumber > HighestNumber:
                    if not HasHitHighest:
                        embed = discord.Embed(
                            title="Hit the Highest",
                            description=f"Yall have hit the highest number on this server",
                            color=0x58fe75  # You can customize the color using hexadecimal
                        )
                        await message.channel.send(embed=embed)
                        HasHitHighest = True
                    HighestNumber = number

                lastUsers = str(message.author.name)
            elif str(message.author.name) == lastUsers:

                await message.add_reaction('❌')
                embed = discord.Embed(
                    title="Only one at a time.",
                    description=f"Players can only go one time and have to wait for another person to go\nUser {message.author.mention} messed up,restarting \nLast Number was {lastNumber + 1}",
                    color=0xff0000  # You can customize the color using hexadecimal
                )
                await message.channel.send(embed=embed)
                lastNumber = 0
                lastUsers = ""
                HasHitHighest = False
            elif number - 1 > lastNumber or number - 1 < lastNumber:

                await message.add_reaction('❌')
                embed = discord.Embed(
                    title="Number wasn't synchronized",
                    description=f"The numbers didn't add up\nUser {message.author.mention} messed up, restarting \nLast "
                                f"Number was {lastNumber + 1}",
                    color=0xff0000  # You can customize the color using hexadecimal
                )
                await message.channel.send(embed=embed)
                lastNumber = 0
                lastUsers = ""
                HasHitHighest = False
    else:
        if message.author.id != 1189631393819537518:
            embed = discord.Embed(
                title="Counting System is disabled",
                description=f"Counting system is offline \nReason: {DisabledReason}",
                color=0xff0000  # You can customize the color using hexadecimal
            )
            await message.reply(embed=embed)
    try:
        if str(message.author) == "LightningMC-Survival#5428":
            if CheckName(str(message.content)):
                Player = message.content.split(":")[0].split(" ")[1]
                Player.replace("\\", "")
                for word in message.content.split():
                    if is_similar_to_word(word.lower(), words, threshold=0.92):
                        staff_chat_channel = message.guild.get_channel(
                            DiscordTextChannels.get("bots"))
                        if staff_chat_channel:
                            embed = discord.Embed(
                                title="Chat Message Warn",
                                description=f"Chat Message Warn:\nPlayer: {Player}\nMessage Content: {str(message.content).split(': ')[1]}",
                                color=0x78bef9  # You can customize the color using hexadecimal
                            )
                            await staff_chat_channel.send(
                                embed=embed)
                            print(
                                f"Chat Message Warn:\nPlayer: {Player}\nMessage Content: {message.content}")
                            await message.delete()
                            break
                        else:
                            print("Error: 'staff-chat' channel not found.")
    except Exception as E:
        staff_chat_channel = message.guild.get_channel(
            DiscordTextChannels.get("bots"))
        if staff_chat_channel:
            embed = discord.Embed(
                title="Error Has happened",
                description=f"Error: {E}\n\nArgs: {E.args}",
                color=0xff0000  # You can customize the color using hexadecimal
            )
            await staff_chat_channel.send(
                embed=embed)
            print(
                f"Error: {E}\n\nArgs: {E.args}")
    await bot.process_commands(message)


"""-------------------|||||||||||Commands||||||||----------------------------"""


@bot.command()
async def foo(ctx, arg):
    print("Foo happened")
    await ctx.send(arg)


# ---------|||||||Running the bot||||||-----------------
def Run():
    global words
    try:
        # Get the bot token from the environment variables
        bot_token = os.getenv('TOKEN')

        if not bot_token:
            print("Bot token not found. Please make sure to set it as an environment variable.")
        else:
            print('Loading Words')
            # Load words from a JSON file
            with open("words.json", "r") as WordsFile:
                words = json.load(WordsFile)
            print(f'Finished loading all {len(words)} words')
            # Run the bot with the token
            bot.run(bot_token)
            with open("saves.json", "w") as SaveFile:
                code = {"LastNumber": lastNumber, "LastUser": lastUsers, "HighestNumber": HighestNumber,
                        "UsersButtonPushed": UsersButtonPushed}
                json.dump(code, SaveFile)
    except KeyboardInterrupt:
        with open("saves.json", "w") as SaveFile:
            code = {"LastNumber": lastNumber, "LastUser": lastUsers, "HighestNumber": HighestNumber,
                    "UsersButtonPushed": UsersButtonPushed}
            json.dump(code, SaveFile)


if __name__ == "__main__":
    Run()
