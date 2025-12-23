import discord
import json
from bot.ai.gemini import generate
from bot.ai.prompts import PARTICIPANTS_PROMPT
from bot.permissions import has_permission

async def analyze_participants(bot, channel_id, guild_id):

    channel = bot.get_channel(channel_id)
    msgs = []
    async for m in channel.history(limit=200):
        if not m.author.bot:
            msgs.append(f"{m.author.name}: {m.content}")

    participants_text = generate(PARTICIPANTS_PROMPT + "\n".join(msgs), guild_id=guild_id)
    if not participants_text:
        return []
    
    try:
        return json.loads(participants_text)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON from Gemini: {participants_text}")
        return []

def register(bot):
    @bot.slash_command(description="Analyze who contributed what to the conversation")
    async def participants(ctx):
        if not has_permission(ctx, "participants"):
            return await ctx.respond("❌ No permission")
        await ctx.defer()
        
        data = await analyze_participants(bot, ctx.channel.id, guild_id=str(ctx.guild.id) if ctx.guild else None)
        if not data:
            return await ctx.respond("✅ No participants found")
        
        embed = discord.Embed(title="👥 Participant Analysis", color=discord.Color.purple())
        for participant in data:
            name = participant.get("name", "Unknown")
            count = participant.get("message_count", 0)
            contrib_type = participant.get("contribution_type", "N/A")
            contributions = ", ".join(participant.get("key_contributions", []))
            
            embed.add_field(
                name=f"{name}",
                value=f"📝 {count} messages | 🎯 {contrib_type}\n📌 {contributions}",
                inline=False
            )
        
        await ctx.respond(embed=embed)
