import discord
from exporter import markdown, pdf
from storage.db import cur

def register(bot):
    @bot.slash_command()
    async def export(ctx, format: str):
        cur.execute(
            "SELECT content FROM summaries WHERE channel_id=? ORDER BY id DESC LIMIT 1",
            (str(ctx.channel.id),)
        )
        summary = cur.fetchone()[0]

        if format == "md":
            content = markdown.export(summary)
            file = discord.File(fp=content.encode(), filename="summary.md")
        else:
            path = "summary.pdf"
            pdf.export(summary, path)
            file = discord.File(path)

        await ctx.respond(file=file)
