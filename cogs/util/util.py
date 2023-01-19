import base64
from datetime import datetime
import requests
import discord
import pip._vendor.requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands
import requests
import json
from typing import Literal
import platform
import sys
import psutil
import cpuinfo


with open("config.json", "r", encoding="UTF-8") as configfile:
    config = json.load(configfile)
    apikey = config["apikey"]
configfile.close()


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Shows the avatar of a user")
    @app_commands.describe(member="Who you want to see the avatar of?")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        embed = discord.Embed(title="Download Avatar",
                              url=member.avatar, color=0x00EFDB,)
        embed.set_author(name=member.name + "`s avatar",
                         url="https://discord.com/users/" + str(member.id), icon_url=member.avatar,)
        embed.set_image(url=member.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="base64decode", description="Decodes a Base64 string")
    @app_commands.describe(text="What is your encoded text?")
    async def base64decode(self, interaction: discord.Interaction, text: str):
        decoded = base64.b64decode(text).decode("utf-8", "ignore")
        embed = discord.Embed(
            title="Your decoded text:\n ||" + str(decoded) + "||", color=0x00D9FF)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="base64_encode", description="Base64 encodes a string")
    @app_commands.describe(text="What is the text you want to encode?")
    async def base64_encode(self, interaction: discord.Interaction, *, text: str):
        string_bytes = text.encode("ascii")

        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")

        embed = discord.Embed(
            title="Your encoded text:\n ||" + str(base64_string) + "||", color=0x00D9FF)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ip", description="Shows information about a IP address")
    @app_commands.describe(ip="Which IP would you like to receive information about?")
    async def ip(self, interaction: discord.Interaction, ip: str):
        params = {"api_key": f"{apikey}", "ip": ip}
        getinformation = requests.get(
            url="https://api.ghostboy.dev/ip", params=params)
        if getinformation.status_code != 200:
            errorres = (
                discord.Embed(title="IP-Checker", color=discord.Color.blue())
                .clear_fields()
                .add_field(name="Something wrent wrong", value="Connection to api failed")
                .set_footer(text=interaction.user.name, icon_url=interaction.user.display_icon.url,)
            )
            return await interaction.response.send_message(embed=errorres, ephemeral=True)

        ipinfor = getinformation.json()
        continent = ipinfor["Continent"]
        city = ipinfor["City"]
        isp = ipinfor["ISP"]
        latitude = ipinfor["Latitude"]
        longitude = ipinfor["Longitude"]
        organization = ipinfor["Organization"]
        zipcode = ipinfor["Zipcode"]

        embed = discord.Embed(
            title="IP-Checker", description="Checked IP: " + ip, color=discord.Color.blue(),)
        embed.set_author(name=interaction.user, url="https://discord.com/users/" +
                         str(interaction.user.id), icon_url=interaction.user.avatar,)
        embed.add_field(name="Location-Info: ",
                        value=f"Continent: {continent}\nCity: {city}\nZip Code: {zipcode}\nLatitude: {latitude}\nLongitude: {longitude}\nOrganization: {organization}", inline=False,)
        embed.add_field(name="ISP:", value=isp, inline=False)

        gettorcheck = requests.get(
            url="https://check.torproject.org/torbulkexitlist")

        if ip in str(gettorcheck.content):
            embed.add_field(name="Tor:", value="True", inline=False)
        else:
            embed.add_field(name="Tor:", value="False", inline=False)
        embed.set_footer(text="IP Check")
        embed.timestamp = datetime.datetime.utcnow()

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="weather", description="Show information about the weather"
    )
    @app_commands.describe(location="About which location?")
    async def weather(self, interaction: discord.Interaction, location: str):
        try:
            params = {"api_key": apikey, "location": location}
            getapi = requests.get(
                url=f"https://api.ghostboy.dev/weather/{location}", params=params)

            if getapi.status_code != 200:
                weatherembed = (discord.Embed(title="Something wrent wrong", timestamp=datetime.now(), color=discord.Color.dark_red(),)
                                .add_field(name="Error", value="There was nothing found for your query!")
                                .set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
                                )
                await interaction.response.send_message(embed=weatherembed, ephemeral=True)
                weatherembed.clear_fields()
                return

            weather = getapi.json()
            weatherdsc = weather["Weather"]
            cloud = weather["Cloud"]
            fah = str(weather["Temperature"]).replace("°f", "F°")
            wspeed = weather["Wind"]
            cels = float(str(fah).replace("F°", "")) - 32 * 5 / 9
            cels = round(cels, 2)
            wspeedkmh = float(str(wspeed).replace("mph", "")) * 1.61
            wspeedkmh = round(wspeedkmh, 2)
            humidity = weather["Humidity"]
            weathericon = weather["Icon"]

            weatherembed = (
                discord.Embed(title="Weather", timestamp=datetime.datetime.now(
                ), color=0x00D9FF, description=weatherdsc,)
                .add_field(name="Cloud", value=cloud)
                .add_field(name="Temperature", value=f"{round(cels, 2)} C°   {fah}")
                .add_field(name="Wind Speed", value=f"{wspeedkmh} km/h {wspeed}")
                .add_field(name="Humidity", value=humidity)
            )
            weatherembed.set_thumbnail(url=weathericon)
            weatherembed.set_footer(
                text=interaction.guild.name, icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=weatherembed, ephemeral=True)
            weatherembed.clear_fields()
        except Exception as e:
            print(e)

    # I was bored...
    @app_commands.command(name="yt", description="Direct-Download for your YT video")
    @app_commands.describe(url="Which YT video do you want to download?")
    async def yt(self, interaction: discord.Interaction, url: str):
        if "https://youtu.be/" in url:
            url.replace("https://youtu.be/",
                        "https://www.youtube.com/watch?v=")

        vgm_url = "https://8downloader.com/download?v=" + url
        html_text = pip._vendor.requests.get(vgm_url).text
        soup = BeautifulSoup(html_text, "html.parser")
        download = soup.find("a", href=True, text="Download")["href"]

        link = "http://tinyurl.com/api-create.php?url=" + str(download)
        from urllib.request import urlopen

        with urlopen(link) as webpage:
            f = webpage.read().decode()

        embed = discord.Embed(
            title="Click here to download your Video", url=f, color=0xFF0000
        )
        embed.set_author(name="Your download link is ready")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="userinfo", description="Shows information about a user")
    @app_commands.describe(member="About which member do you want to get infos?")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(title=f"{member.name}'s Info", color=0x00CCFF)
        embed.set_author(name=str(member), icon_url=member.avatar)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime(
            date_format), inline=True)
        members = sorted(interaction.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position",
                        value=str(members.index(member) + 1))
        embed.add_field(name="Account created", value=member.created_at.strftime(
            date_format), inline=True,)
        embed.add_field(name="🤖 Bot", value=member.bot, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
        # embed.add_field(name='Status', value=member.raw_status, inline=True)

        embed.add_field(name="Highest role",
                        value=member.top_role.mention, inline=True)
        rolelist = [r.mention for r in member.roles]
        roles = ", ".join(rolelist)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ping", description="Pong")
    async def ping(self, interaction: discord.Interaction):
        # Calculate the ping in milliseconds
        ping_ms = round(self.bot.latency * 1000)

        # Choose the appropriate color for the embed based on the ping
        if ping_ms <= 50:
            color = 0x44FF44
        elif ping_ms <= 100:
            color = 0xFFD000
        elif ping_ms <= 200:
            color = 0xFF6600
        else:
            color = 0x990000

        # Create the Discord embed
        embed = discord.Embed(
            title="PING", description=f"Pong! The ping is **{ping_ms}** milliseconds!", color=color,)

        # Send the embed to Discord
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fact", description="Shows you a useless fact")
    @app_commands.describe(language="In which language should your useless fact be shown?")
    async def fact(self, interaction: discord.Interaction, language: Literal["English", "German"] = "English",):
        try:
            language_codes = {"English": "en", "German": "de"}
            code = language_codes.get(language)
            if not code:
                await interaction.response.send_message("Sorry, that language is not supported.", ephemeral=True)
                return

            url = f"https://uselessfacts.jsph.pl/random.json?language={code}"
            factembed = discord.Embed(timestamp=datetime.now(), color=discord.Color.dark_red(
            )).set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)

            try:
                response = requests.get(url)
                if response.status_code != 200:
                    factembed.add_field(name="Error Code:",
                                        value=response.status_code)
                    await interaction.response.send_message(embed=factembed, ephemeral=True)
                    return

                data = response.json()
                fact = data["text"]
                await interaction.response.send_message(fact, ephemeral=True)
            except requests.exceptions.RequestException as e:
                factembed.add_field(name="Error:", value=str(e))
                await interaction.response.send_message(embed=factembed, ephemeral=True)
            except ValueError:
                factembed.add_field(
                    name="Error:", value="Failed to parse response as JSON.")
                await interaction.response.send_message(embed=factembed, ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="short", description="Short a url")
    @app_commands.describe(shortner="Which shortner service do you want to use?")
    async def short(self, interaction: discord.Interaction, url: str, shortner: Literal["anditv.it", "tinyurl", "is.gd", "urlz (only ascii)"] = "tinyurl",):
        shortener_urls = {
            "anditv.it": "https://anditv.it/short/api/",
            "tinyurl": "http://tinyurl.com/api-create.php",
            "is.gd": "http://is.gd/api.php",
            "urlz": "https://urlz.fr/api_new.php",
        }
        try:
            shortener_url = shortener_urls[shortner]
            payload = {"url": url}
            response = requests.post(shortener_url, data=payload)

            if response.status_code == 400:
                raise ValueError("Invalid URL")
            elif response.status_code == 401:
                raise ValueError("Unauthorized")
            elif response.status_code != 200:
                raise ValueError(
                    f"Unexpected HTTP status code: {response.status_code}")
        except ValueError as e:
            embed = discord.Embed(
                title="Error while shortening URL",
                description=str(e),
                timestamp=datetime.now(),
                color=discord.Color.dark_red(),
            )
            embed.set_footer(text=interaction.guild.name,
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        except Exception as e:
            print("Error while shortening URL: %s", e)
            embed = discord.Embed(
                title="An unexpected error occurred",
                timestamp=datetime.now(),
                color=discord.Color.dark_red(),
            )
            embed.set_footer(text=interaction.guild.name,
                             icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        short_url = str(response.content, "utf-8")
        embed = discord.Embed(
            title="✅ Successfully shorted your URL", color=0xFFFFFF
        ).add_field(name="Short-Service:", value=shortner.capitalize(), inline=False)
        embed.add_field(name="Short URL:", value=short_url, inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='epic', description='Get free epicgames games')
    async def epic(self, interaction: discord.Interaction):
        try:
            params = {
                "api_key": apikey
            }

            getinformation = requests.get(
                url="https://api.ghostboy.dev/epic", params=params)
            if getinformation.status_code != 200:
                errorres = discord.Embed(
                    title='Free Epic Games',
                    color=discord.Color.dark_red()
                ).clear_fields(
                ).add_field(
                    name='Something wrent wrong',
                    value='Connection to api failed'
                ).set_footer(
                    text=interaction.user.name,
                    icon_url=interaction.user.avatar,
                )
                return await interaction.response.send_message(embed=errorres, ephemeral=True)

            offer_one = getinformation.json()['Offer one']
            offer_one_text = f'''**• Title**\n➥ {offer_one['Title']}\n**• Description**\n➥ {offer_one['Description']}\n**• Status**\n➥ {offer_one['Status']}\n**• Start**\n➥ {offer_one['Start']}\n**• End**\n➥ {offer_one['End']}\n'''

            offer_two = getinformation.json()['Offer two']
            offer_two_text = f'''\n\n**• Title\n➥ {offer_two['Title']}\n**• Description\n➥ {offer_two['Description']}\n**• Status\n➥ {offer_two['Status']}\n**• Start\n➥ {offer_two['Start']}\n**• End**\n➥ {offer_two['End']}\n'''

            epic_embed = discord.Embed(
                title='Epic games free game',
                color=0xFFD000,
                timestamp=datetime.datetime.now()
            )

            try:
                offer_three = getinformation.json()['Offer three']
                offer_three_text = f'''\n\nGame 3\n**Title**\n➥ {offer_three['Title']}\n**Description**\n➥ {offer_three['Description']}\n**Status**\n➥ {offer_three['Status']}\n**Start**\n➥ {offer_three['Start']}\n**End**\n➥ {offer_three['End']}\n'''

                offer_four = getinformation.json()['Offer four']
                offer_four_text = f'''\n\nGame 4\n**Title**\n➥ {offer_four['Title']}\n**Description**\n➥ {offer_four['Description']}\n**Status**\n➥ {offer_four['Status']}\n**Start**\n➥ {offer_four['Start']}\n**End**\n➥ {offer_four['End']}\n'''
                offer_img = getinformation.json()['Offer three']['Image']
                offers_text_part_one = offer_one_text + offer_two_text
                offers_text_part_two = offer_three_text + offer_four_text

                epic_embed.add_field(
                    name='Game part one',
                    value=offers_text_part_one
                ).add_field(
                    name='Game part two',
                    value=offers_text_part_two
                )
            except:
                offer_img = getinformation.json()['Offer one']['Image']
                offers_text = offer_one_text + offer_two_text

                epic_embed.add_field(
                    name='Game',
                    value=offers_text
                )

            epic_embed.set_image(
                url=offer_img
            ).set_footer(
                text=interaction.user.name,
                icon_url=interaction.user.avatar.url
            ).set_thumbnail(
                url='https://cdn2.unrealengine.com/Unreal+Engine%2Feg-logo-filled-1255x1272-0eb9d144a0f981d1cbaaa1eb957de7a3207b31bb.png'
            )

            await interaction.response.send_message(embed=epic_embed)
            epic_embed.clear_fields()
        except Exception as e:
            print(e)

    @app_commands.command(name='mock', description='lEtS YoU CrEaTe tExT LiKe tHiS')
    @app_commands.describe(text="wHiCh tExT Do yOu wAnT To mOcK?")
    async def mock(self, interaction: discord.Interaction, *, text: str):
        try:

            getinformation = requests.get(
                url=f"https://api.anditv.it/?api_key={apikey}&function=mock&text={text}")
            if getinformation.status_code != 200:
                errorres = discord.Embed(
                    title='API Error',
                    color=discord.Color.dark_red()
                ).clear_fields(
                ).add_field(
                    name='Something wrent wrong',
                    value='Connection to api failed'
                ).set_footer(
                    text=interaction.user.name,
                    icon_url=interaction.user.avatar,
                )
                return await interaction.response.send_message(embed=errorres, ephemeral=True)

            result = getinformation.json()['text']
            await interaction.response.send_message(result, ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="botinfo", description="Shows information about the bot.")
    async def botinfo(self, interaction: discord.Interaction):
        name = self.bot.user
        id = self.bot.user.id
        python_version = platform.python_version()
        os_version = platform.system()
        cpu_name = cpuinfo.get_cpu_info()['brand_raw']
        ram_usage = psutil.virtual_memory().percent

        info = f"Bot-Name: {name} ({id}) \nPython: {python_version}\nOS: {os_version}\nCPU: {cpu_name}\nRAM: {ram_usage} %"

        embed = discord.Embed(color=0x00D9FF)
        embed.add_field(name="Bot Info", value=f"```{info}```", inline=False)
        embed.set_footer(text=interaction.user.name,
                         icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='discordstatus', description="Shows you the discord server status")
    async def discordstatus(self, interaction: discord.Interaction):
        try:
            response = requests.get(
                "https://discordstatus.com/api/v2/summary.json")
            data = json.loads(response.text)
            if response.status_code != 200:
                raise ValueError(
                    f"Unexpected HTTP status code: {response.status_code}")
            components = [{'name': component["name"], 'value': component["status"].capitalize(
            ), 'inline': True} for component in data["components"]]

            embed = discord.Embed(title=data["status"]["description"],
                                  description=f"[Discord Status](https://discordstatus.com/)\n **Current Incident:**\n {data['status']['indicator']}",
                                  color=0x00D9FF,
                                  timestamp=datetime.now())
            embed.set_thumbnail(
                url="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png")
            for component in components:
                embed.add_field(
                    name=component["name"], value=component["value"], inline=component["inline"])
            await interaction.response.send_message(embed=embed)
        except ValueError as e:
            embed = discord.Embed(
                title="Error while retrieving discord status",
                description=str(e),
                color=discord.Color.dark_red(),
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("Error: " + str(e))


async def setup(bot):
    await bot.add_cog(Util(bot))
