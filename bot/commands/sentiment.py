import discord
import json
from bot.ai.gemini import generate
from bot.ai.prompts import SENTIMENT_PROMPT
from storage.db import cur, conn
from bot.permissions import has_permission

async def analyze_sentiment(bot, channel_id, guild_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        return None
    msgs = []
    async for m in channel.history(limit=200):
        if not m.author.bot:
            msgs.append(f"{m.author.name}: {m.content}")

    sentiment_text = generate(SENTIMENT_PROMPT + "\n".join(msgs), guild_id=guild_id)
    if not sentiment_text:
        return None
    
    try:
        return json.loads(sentiment_text)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON from Gemini: {sentiment_text}")
        return None

def register(bot):
    @bot.slash_command(description="Analyze sentiment, tone, and emotional themes")
    async def sentiment(ctx):
        if not has_permission(ctx, "sentiment"):
            return await ctx.respond("❌ No permission")
        await ctx.defer()
        result = await analyze_sentiment(bot, ctx.channel.id, str(ctx.guild.id))
        if not result:
            return await ctx.respond("❌ Failed to analyze sentiment")
        
        embed = discord.Embed(title="📊 Sentiment Analysis", color=discord.Color.blue())
        embed.add_field(name="Overall Sentiment", value=result.get("overall_sentiment", "N/A"), inline=False)
        embed.add_field(name="Sentiment Score", value=f"{result.get('sentiment_score', 0):.2f}", inline=True)
        embed.add_field(name="Tone", value=result.get("tone", "N/A"), inline=True)
        embed.add_field(name="Themes", value=", ".join(result.get("themes", [])), inline=False)
        embed.add_field(name="Summary", value=result.get("emotional_summary", "N/A"), inline=False)
        
        await ctx.respond(embed=embed)
