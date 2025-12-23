import discord
from storage.db import cur, conn
from bot.permissions import has_permission

def register(bot):
    @bot.slash_command(description="Configure AI tone and server preferences")
    async def settings(ctx, tone: str = None):
        if not has_permission(ctx, "settings"):
            return await ctx.respond("❌ No permission")
        
        if tone is None:
            cur.execute("SELECT tone FROM guild_settings WHERE guild_id=?",
                       (str(ctx.guild.id),))
            result = cur.fetchone()
            current_tone = result[0] if result else "professional"
            
            embed = discord.Embed(
                title="⚙️ Server Settings",
                color=discord.Color.greyple(),
                description=f"Current AI Tone: **{current_tone}**\n\nUse `/settings <tone>` to change"
            )
            embed.add_field(
                name="Available Tones",
                value="• professional\n• casual\n• friendly\n• technical\n• executive",
                inline=False
            )
            return await ctx.respond(embed=embed)
        
        valid_tones = ["professional", "casual", "friendly", "technical", "executive"]
        if tone not in valid_tones:
            return await ctx.respond(f"❌ Invalid tone. Choose from: {', '.join(valid_tones)}")
        
        cur.execute("DELETE FROM guild_settings WHERE guild_id=?",
                   (str(ctx.guild.id),))
        cur.execute("INSERT INTO guild_settings (guild_id, tone) VALUES (?,?)",
                   (str(ctx.guild.id), tone))
        conn.commit()
        
        await ctx.respond(f"✅ AI tone updated to **{tone}**")
