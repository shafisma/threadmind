import discord
import json
from bot.ai.gemini import generate
from bot.ai.prompts import ACTION_ITEMS_PROMPT
from storage.db import cur, conn
from bot.permissions import has_permission

async def extract_action_items(bot, channel_id, guild_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        return []
    msgs = []
    async for m in channel.history(limit=200):
        if not m.author.bot:
            msgs.append(f"{m.author.name}: {m.content}")

    items_text = generate(ACTION_ITEMS_PROMPT + "\n".join(msgs), guild_id=guild_id)
    if not items_text:
        return []
    
    try:
        return json.loads(items_text)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON from Gemini: {items_text}")
        return []

def register(bot):
    @bot.slash_command(description="Extract action items, TODOs, and tasks")
    async def action_items(ctx):
        if not has_permission(ctx, "action_items"):
            return await ctx.respond("❌ No permission")

        await ctx.defer()

        items = await extract_action_items(
            bot,
            ctx.channel.id,
            guild_id=str(ctx.guild.id) if ctx.guild else None
        )

        if not items:
            return await ctx.respond("✅ No action items found")

        embed = discord.Embed(
            title="✅ Action Items",
            color=discord.Color.green()
        )

        for idx, item in enumerate(items, 1):
            task = item.get("task", "N/A")
            assignee = item.get("assignee") or "Unassigned"
            priority = item.get("priority", "medium")
            deadline = item.get("deadline") or "No deadline"

            embed.add_field(
                name=f"{idx}. {task}",
                value=f"👤 {assignee} | 🎯 {priority} | ⏰ {deadline}",
                inline=False
            )

        await ctx.respond(embed=embed)

