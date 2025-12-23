import discord
import json
from bot.ai.gemini import generate
from bot.ai.prompts import STATISTICS_PROMPT
from storage.db import cur
from bot.permissions import has_permission

async def compute_stats(guild_id):
    cur.execute("SELECT COUNT(*) FROM summaries WHERE guild_id=?",
               (str(guild_id),))
    total_summaries = cur.fetchone()[0]
    
    cur.execute("""
        SELECT COUNT(*) FROM decisions 
        WHERE channel_id IN (SELECT channel_id FROM summaries WHERE guild_id=?)
    """, (str(guild_id),))
    total_decisions = cur.fetchone()[0]
    
    avg_decisions = total_decisions / total_summaries if total_summaries > 0 else 0
    
    return {
        "total_summaries": total_summaries,
        "total_decisions": total_decisions,
        "avg_decisions": avg_decisions
    }

def register(bot):
    @bot.slash_command(description="View activity, decisions, and trends")
    async def statistics(ctx):
        if not has_permission(ctx, "statistics"):
            return await ctx.respond("❌ No permission")
        
        await ctx.defer()
        stats = await compute_stats(ctx.guild.id)
        
        embed = discord.Embed(
            title="📈 Server Statistics",
            color=discord.Color.nitro_pink(),
            description="Activity and decision-making metrics"
        )
        
        embed.add_field(
            name="Summaries Created",
            value=f"**{stats['total_summaries']}**",
            inline=True
        )
        embed.add_field(
            name="Total Decisions",
            value=f"**{stats['total_decisions']}**",
            inline=True
        )
        embed.add_field(
            name="Avg Decisions/Summary",
            value=f"**{stats['avg_decisions']:.1f}**",
            inline=True
        )
        
        cur.execute("""
            SELECT channel_id, COUNT(*) as count FROM summaries 
            WHERE guild_id=? GROUP BY channel_id ORDER BY count DESC LIMIT 5
        """, (str(ctx.guild.id),))
        active_channels = cur.fetchall()
        
        if active_channels:
            embed.add_field(name="Most Active Channels", value="", inline=False)
            for channel_id, count in active_channels:
                channel = bot.get_channel(int(channel_id))
                channel_name = channel.name if channel else f"Unknown"
                embed.add_field(
                    name=f"#{channel_name}",
                    value=f"{count} summaries",
                    inline=True
                )
        
        await ctx.respond(embed=embed)
