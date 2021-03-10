import os
import logging

from discord.ext.commands import Bot as BaseBot, errors


log = logging.getLogger(__name__)


class Bot(BaseBot):
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
