import discord
from discord.ext import commands
from discord import utils
import Bot
import settings
from settings import lastNumber

"""
Commands List:
Check-api: Not currently working

"""
"""
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
                await message.delete()"""


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def setnumber(self, ctx: discord.ext.commands.Context, number: int):
        for Role in ctx.message.author.roles:
            if Role.name == "________Administration________":
                print(settings.lastNumber)
                settings.updateScore(settings.lastUsers, number)
                print(settings.lastNumber)
                await ctx.send(f"Set lastNumber to {number}")
                break

    @commands.hybrid_command()
    async def pronouns(self, ctx: discord.ext.commands.Context):
        """Will show the pronouns of the bot"""
        await ctx.send("Bot\They")


async def setup(bot):
    await bot.add_cog(Commands(bot))
