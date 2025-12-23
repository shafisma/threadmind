import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from bot.commands import (
    summarize, recall, sentiment, action_items, participants, 
    timeline, search, settings, compare, statistics
)
from bot.scheduler import auto_summary

load_dotenv()

bot = commands.Bot(intents=discord.Intents.all())

summarize.register(bot)
recall.register(bot)
sentiment.register(bot)
action_items.register(bot)
participants.register(bot)
timeline.register(bot)
search.register(bot)
settings.register(bot)
compare.register(bot)
statistics.register(bot)

@bot.event
async def on_ready():
    await bot.sync_commands()
    auto_summary.start(bot)
    print("✅ ThreadMind running")

bot.run(os.getenv("DISCORD_TOKEN"))
