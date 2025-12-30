import os, sys
from pathlib import Path
from discord import Bot
from dotenv import load_dotenv

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.commands import (
    summarize, recall, sentiment, action_items, participants, 
    timeline, search, settings, compare, statistics
)
from bot.scheduler import auto_summary

load_dotenv()

# Use py-cord's Bot class which supports slash_command
bot = Bot()

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
