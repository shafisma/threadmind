import discord
import json
from bot.ai.gemini import generate
from bot.ai.prompts import COMPARISON_PROMPT
from storage.db import cur
from bot.permissions import has_permission

def register(bot):
    @bot.slash_command(description="Compare summaries from two channels")
    async def compare(
        ctx,
        channel1: discord.TextChannel,
        channel2: discord.TextChannel
    ):
        if not has_permission(ctx, "compare"):
            return await ctx.respond("❌ No permission")

        await ctx.defer()
        cur.execute(
            "SELECT content FROM summaries WHERE channel_id=? ORDER BY id DESC LIMIT 1",
            (str(channel1.id),)
        )
        s1 = cur.fetchone()

        cur.execute(
            "SELECT content FROM summaries WHERE channel_id=? ORDER BY id DESC LIMIT 1",
            (str(channel2.id),)
        )
        s2 = cur.fetchone()

        if not s1 or not s2:
            return await ctx.respond("❌ One or both channels have no summaries")

        comparison_text = generate(
            COMPARISON_PROMPT.format(
                summary1=s1[0],
                summary2=s2[0]
            ),
            guild_id=str(ctx.guild.id) if ctx.guild else None
        )

        if not comparison_text:
            return await ctx.respond("❌ Failed to compare summaries")

        try:
            result = json.loads(comparison_text)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON from Gemini: {comparison_text}")
            return await ctx.respond("❌ Failed to parse comparison")

        embed = discord.Embed(
            title=f"🔄 Comparison: #{channel1.name} vs #{channel2.name}",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="Similarities",
            value="\n".join(f"• {s}" for s in result.get("similarities", [])) or "None",
            inline=False
        )
        embed.add_field(
            name="Differences",
            value="\n".join(f"• {d}" for d in result.get("differences", [])) or "None",
            inline=False
        )
        embed.add_field(
            name="Evolution",
            value=result.get("evolution", "N/A"),
            inline=False
        )
        embed.add_field(
            name="New Decisions",
            value="\n".join(f"• {d}" for d in result.get("new_decisions", [])) or "None",
            inline=False
        )

        await ctx.respond(embed=embed)
