import sys
import asyncio

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import setup_logger
from telegrinder.rules import Text

from telebar import progressify
from telebar import MoonBar

setup_logger(console_sink=sys.stderr, level="INFO")
api = API(token=Token("your_token_here"))
bot = Telegrinder(api)


@bot.on.message(Text("/start"))
async def start(message: Message) -> None:
    iterator, length = range(10), 10
    ans = (await message.answer(f"Progress bar below:")).unwrap()
    async for item in progressify(iterator, length).at(ans).using(MoonBar(length, width=3)):
        await asyncio.sleep(item)

bot.run_forever()
