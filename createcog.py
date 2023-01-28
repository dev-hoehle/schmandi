import argparse
import os


def createCog(name:str, cmdName:str, cmdDesc:str) -> str:
    exampleCog = f"""from discord import app_commands
from discord.ext import commands
class {name}(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="{cmdName}", description={cmdDesc}))
    async def {cmdName}(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello there!")
    
async def setup(bot):
    await bot.add_cog({name})"""
    return exampleCog

def main() -> None:
    parser = argparse.ArgumentParser(description="Discord.py 2.0+ cog generator")
    parser.add_argument("--cogName", type=str, default="Test", required=False, help="Name of the new cog")
    parser.add_argument("--cmdName", type=str, default="test", required=False, help="Name of the example command")
    parser.add_argument("--cmdDesc", type=str, default="Example cmd", required=False, help="Description of the example command")
    args = parser.parse_args()
    try:
        with open(os.path.join(os.getcwd(), f"{args.cogName}.py"), "x+", encoding="UTF-8") as f:
            f.write(createCog(args.cogName, args.cmdName, args.cmdDesc))
    except FileExistsError:
        print("File already there!")
    else:
        print("Finished!")
        
main()
