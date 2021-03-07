import os
import logging

import asyncio
from discord import Intents, AllowedMentions
from dotenv import load_dotenv

from bot import Bot


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(
    command_prefix=os.getenv("BOT_PREFIX"),
    allowed_mentions=AllowedMentions.none(),
    case_insensitive=True,
    intents=Intents(messages=True, guilds=True),
)


if __name__ == "__main__":
    # Basic event loop, logs the bot out when control-c is pressed
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start(os.getenv("BOT_TOKEN")))
    except KeyboardInterrupt:
        loop.run_until_complete(bot.logout())
    finally:
        loop.run_until_complete(loop.close())
