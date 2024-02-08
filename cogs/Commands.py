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
    async def setcounting(self, ctx: discord.ext.commands.Context, number: int):
        """Will set the number of the counting,  YOU MUST BE A ADMIN FOR THIS"""
        if ctx.author.id in [810708562094719027]:
            settings.updateScore(settings.lastUsers, number)
            await ctx.send(f"Set lastNumber to {number}", ephemeral=True)
            return
        for Role in ctx.author.roles:
            if Role.name == "________Administration________":
                settings.updateScore(settings.lastUsers, number)
                await ctx.send(f"Set lastNumber to {number}", ephemeral=True)
                return
        await ctx.send("You do not have permission", ephemeral=True)
        DM = await ctx.author.create_dm()
        await DM.send("You do not have permission to use that command")

    @commands.hybrid_command()
    async def resetcounting(self, ctx: commands.Context):
        for Role in ctx.author.roles:
            if Role.name == "________Administration________":
                settings.updateScore('', 0)
                await ctx.send(f"Reset counting")
                Embed = discord.Embed(
                    title="Reset",
                    description="A Admin has reset the number back to 1",
                    color=0xff0000
                )

                bots = ctx.guild.get_channel(Bot.DiscordTextChannels['count'])
                await bots.send(embed=Embed)
                return
        await ctx.send("You do not have permission", ephemeral=True)
        DM = await ctx.author.create_dm()
        await DM.send("You do not have permission to use that command")


async def setup(bot):
    await bot.add_cog(Commands(bot))
