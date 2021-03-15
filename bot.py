import os
import logging

from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import errors


log = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_cogs()

    def load_cogs(self):
        """Load all cogs from the 'cogs' directory"""

        path = "cogs/"  # Should always have a trailing slash
        import_path = path.replace("/", ".")
        extensions: list[str] = [
            import_path + file.replace(".py", "")
            for file in os.listdir(path)
            if os.path.isfile(f"{path}{file}")
        ]

        for extension in extensions:
            try:
                self.load_extension(extension)
            except errors.ExtensionAlreadyLoaded:
                pass

        log.info(f"Loaded {len(self.commands)} commands from {len(self.cogs)} cogs")

    def reload_cogs(self):
        """Reload all loaded cogs"""

        for extension in list(self.extensions):
            try:
                self.reload_extension(extension)
            except errors.NoEntryPointError:
                log.info("The extension {extension} has no setup function")
                pass
            except errors.ExtensionAlreadyLoaded:
                pass

        log.info(f"Reloaded {len(self.extensions)} cogs")

    async def on_ready(self):
        log.info(f"Bot ready as {self.user}")

    async def on_command_error(self, ctx: commands.Context, exception: Exception):
        # Base error message title
        title = "Error"

        try:
            # Raising here for the sake of code readibility.
            # These checks can be easily accomplished with if/elif statements.
            # TODO: For Python 3.10: use pattern matching.
            raise exception
        except errors.CommandNotFound:
            # Ignore CommandNotFound, because it doesn't mean much for us.
            return
        except (errors.MissingRequiredArgument, errors.TooManyArguments):
            # Send command help if the user types too many or not enough arguments.
            # This approach is much cleaner than throwing a
            # 'too many arguments' error at them.
            return await ctx.send_help(ctx.command)
        except (errors.NotOwner, errors.MissingPermissions):
            title = "Insufficient permissions"
        except errors.BotMissingPermissions:
            title = "Missing bot permissions"
        except errors.NSFWChannelRequired:
            title = "This channel is not NSFW"
        except errors.CommandOnCooldown:
            title = "Cooldown"
        except (
            commands.RoleNotFound,
            commands.ChannelNotFound,
            commands.UserNotFound,
            commands.MemberNotFound,
            commands.MessageNotFound,
        ):
            title = "Not found"
        except Exception:
            # Anything not matched above we just log as an error.
            log.exception(exception)
            # pass

        embed = Embed(title=title, description=str(exception), color=Color.red())
        await ctx.send(embed=embed)
