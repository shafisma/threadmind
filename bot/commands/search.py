import discord
from storage.db import cur
from bot.permissions import has_permission

def register(bot):
    @bot.slash_command(description="Search summaries by keyword across the server")
    async def search(ctx, keyword: str):
        if not has_permission(ctx, "search"):
            return await ctx.respond("❌ No permission")
        
        cur.execute(
            "SELECT channel_id, content FROM summaries WHERE guild_id=? AND content LIKE ? LIMIT 10",
            (str(ctx.guild.id), f"%{keyword}%")
        )
        results = cur.fetchall()
        
        if not results:
            return await ctx.respond(f"❌ No summaries found matching '{keyword}'")
        
        embed = discord.Embed(
            title=f"🔍 Search Results for '{keyword}'",
            color=discord.Color.blue(),
            description=f"Found {len(results)} result(s)"
        )
        
        for channel_id, content in results:
            channel = bot.get_channel(int(channel_id))
            channel_name = channel.name if channel else f"Unknown (ID: {channel_id})"
            preview = content[:200] + "..." if len(content) > 200 else content
            
            embed.add_field(
                name=f"#{channel_name}",
                value=preview,
                inline=False
            )
        
        await ctx.respond(embed=embed)
