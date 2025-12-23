import discord
import json
from bot.ai.gemini import generate
from bot.ai.prompts import TIMELINE_PROMPT
from bot.permissions import has_permission

async def create_timeline(bot, channel_id, guild_id):
    channel = bot.get_channel(channel_id)
    msgs = []
    async for m in channel.history(limit=200):
        if not m.author.bot:
            msgs.append(f"{m.author.name}: {m.content}")

    timeline_text = generate(TIMELINE_PROMPT + "\n".join(msgs), guild_id=guild_id)
    if not timeline_text:
        return []
    
    try:
        return json.loads(timeline_text)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON from OpenRouter: {timeline_text}")
        return []

def register(bot):
    @bot.slash_command(description="Create a chronological timeline of key events")
    async def timeline(ctx):
        if not has_permission(ctx, "timeline"):
            return await ctx.respond("❌ No permission")
        await ctx.defer()
        
        events = await create_timeline(bot, ctx.channel.id, str(ctx.guild.id))
        if not events:
            return await ctx.respond("✅ No timeline events found")
        
        embed = discord.Embed(title="⏳ Conversation Timeline", color=discord.Color.gold())
        for event in events:
            order = event.get("timestamp_order", 0)
            description = event.get("event", "N/A")
            event_type = event.get("type", "discussion")
            
            emoji = {
                "decision": "✅",
                "question": "❓",
                "announcement": "📢",
                "discussion": "💬"
            }.get(event_type, "•")
            
            embed.add_field(
                name=f"{emoji} Step {order}",
                value=description,
                inline=False
            )
        
        await ctx.respond(embed=embed)
