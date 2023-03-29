import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from discord.utils import get

import discord
import requests
import re

from discord.ext import commands
from selenium.webdriver.common.by import By

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

recent = ''

def get_screenshot(url):
    chrome_options = Options()
    chrome_options.add_argument("window-size=1280,800")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    chrome_executable = Service(executable_path='chromedriver.exe', log_path='NUL')

    driver = webdriver.Chrome(service=chrome_executable, options=chrome_options)
    driver.get(url)

    element = driver.find_element(By.XPATH, "/html/body/div[2]/div[5]/div[2]/div[1]/div[2]/div[2]")
    element.screenshot("match.png")

    driver.quit()


@bot.event
async def on_ready():
    print("Ready")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game('holt dich hops'))



@bot.command()
async def ready(ctx):
    global recent
    while True:
        await asyncio.sleep(3600)
        print("test")
        response = requests.get("https://www.hltv.org/team/7532/big#tab-matchesBox")
        newest = re.findall('matches/(.*?)"', response.text, re.S)

        if newest[0] != recent:
            get_screenshot(f"https://www.hltv.org/matches/{newest[0]}")
            roles = get(ctx.guild.roles, name='csgo ankündigung')
            await ctx.send(f"||{roles.mention}||", file=discord.File('match.png'))
            recent = newest[0]



bot.run("MTA4OTc1NzA4MDEyNDE0OTg3Mw.GvnjJz.1HKbPlJFHKlpQudxqVnwBW9L0rrjDluH1BN1zY")

