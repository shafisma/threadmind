from discord.ext import tasks
import time
from storage.db import cur, conn
from bot.commands.summarize import summarize_channel

@tasks.loop(minutes=1)
async def auto_summary(bot):
    cur.execute("SELECT channel_id, interval, last_run FROM auto_config")
    for ch, interval, last in cur.fetchall():
        if time.time() - last >= interval * 60:
            await summarize_channel(bot, int(ch))
            cur.execute(
                "UPDATE auto_config SET last_run=? WHERE channel_id=?",
                (time.time(), ch)
            )
            conn.commit()

