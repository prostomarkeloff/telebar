import sys
import asyncio

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import setup_logger
from telegrinder.rules import Text

from telebar import progressify

setup_logger(console_sink=sys.stderr, level="INFO")
api = API(token=Token("your_token_here"))
bot = Telegrinder(api)


@bot.on.message(Text("/start"))
async def start(message: Message) -> None:
    ans = (await message.answer(f"Progress bar below:")).unwrap()
    async for _ in progressify(range(10), 10).at(ans):
        await asyncio.sleep(1)

bot.run_forever()
