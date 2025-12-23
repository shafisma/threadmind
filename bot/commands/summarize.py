import discord
import json
from bot.ai.gemini import generate
from bot.ai.prompts import SUMMARY_PROMPT, DECISION_PROMPT
from storage.db import cur, conn
from bot.permissions import has_permission

async def summarize_channel(bot, channel_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        return
    msgs = []
    async for m in channel.history(limit=200):
        if not m.author.bot:
            msgs.append(f"{m.author.name}: {m.content}")

    cur.execute("SELECT tone FROM guild_settings WHERE guild_id=?",
                (str(channel.guild.id),))
    tone = cur.fetchone()
    tone = tone[0] if tone else "professional"

    summary = generate(
        SUMMARY_PROMPT.format(tone=tone) + "\n".join(msgs[::-1]),
        guild_id=str(channel.guild.id)
    )
    
    if not summary:
        print("❌ Gemini API failed to generate summary")
        return

    cur.execute(
        "INSERT INTO summaries (guild_id, channel_id, content) VALUES (?,?,?)",
        (str(channel.guild.id), str(channel.id), summary)
    )

    decisions_text = generate(DECISION_PROMPT + "\n".join(msgs), guild_id=str(channel.guild.id))
    if not decisions_text:
        print("⚠️ No decisions extracted")
        decisions = []
    else:
        try:
            decisions = json.loads(decisions_text)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON from Gemini: {decisions_text}")
            decisions = []
    
    for d in decisions:
        cur.execute(
            "INSERT INTO decisions VALUES (NULL,?,?,?)",
            (str(channel.id), d["decision"], d["confidence"])
        )

    conn.commit()

def register(bot):
    @bot.slash_command(description="Summarize and extract key decisions")
    async def summarize(ctx):
        if not has_permission(ctx, "summarize"):
            return await ctx.respond("❌ No permission")
        await ctx.defer() 
        await summarize_channel(bot, ctx.channel.id)
        await ctx.respond("✅ Summary saved. Use /recall to view it.")
