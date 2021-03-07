from discord.ext.commands import Bot, Cog, Context, command, is_owner


class Management(Cog):
    """Managing the bot"""

    @command(aliases=["r"], hidden=True)
    @is_owner()
    async def reload(self, ctx: Context):
        """Reload all cogs and commands"""

        ctx.bot.reload_cogs()
        await ctx.send(
            f"Reloaded **{len(ctx.bot.commands)} commands** "
            f"from **{len(ctx.bot.cogs)} cogs**."
        )


def setup(bot: Bot):
    bot.add_cog(Management())
