from storage.db import cur

def register(bot):
    @bot.slash_command(description="Get the latest channel summary")
    async def recall(ctx):
        cur.execute(
            "SELECT content FROM summaries WHERE channel_id=? ORDER BY id DESC LIMIT 1",
            (str(ctx.channel.id),)
        )
        row = cur.fetchone()
        if not row:
            return await ctx.respond("No summary.")
        await ctx.respond(row[0][:2000])
