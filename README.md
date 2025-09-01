# < telebar

**Fancy progress bars for your Telegram bots!**

Transform boring progress tracking into visually stunning animated bars that your users will love. From classic progress bars to mesmerizing moon phases, telebar makes waiting fun! ✨

*Part of the [awesome-telegrinder](https://github.com/prostomarkeloff/awesome-telegrinder) family* 🚀

## =� Installation

### From GitHub

```bash
pip install git+https://github.com/prostomarkeloff/telebar.git
```

### Using uv (recommended)

```bash
uv add git+https://github.com/prostomarkeloff/telebar.git
```

## =� Requirements

- Python 3.13+
- [telegrinder](https://github.com/timoniq/telegrinder)

## � Quick Start

```python
import asyncio
from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import Text
from telebar import progressify

api = API(token=Token("your_token_here"))
bot = Telegrinder(api)

@bot.on.message(Text("/start"))
async def start(message: Message) -> None:
    ans = (await message.answer("Processing your request...")).unwrap()
    
    # Magic happens here! (
    async for _ in progressify(range(10), 10).at(ans):
        await asyncio.sleep(1)

bot.run_forever()
```

## <� Available Progress Bars

### < MoonBar - Lunar Progress Magic
Experience the phases of the moon as your progress unfolds:

```python
from telebar import MoonBar

# Moon phase progress: < < < < <
async for item in progressify(range(12), 12).at(message).using(
    MoonBar(12, width=5, label="Lunar Progress")
):
    # Your processing magic here
    await process_item(item)
```

**Output:**
```
Lunar Progress  <<<<<  7/12 (58.3%)
```

### =� DefaultProgressBar - Classic Beauty
Clean, professional progress tracking:

```python
# Uses DefaultProgressBar automatically
async for item in progressify(your_data, total_count).at(message):
    await process_item(item)
```

**Output:**
```
[������������������] 40.00%
```

## =' Advanced Usage

### Flexible Message Targeting
Multiple ways to specify where your progress appears:

```python
# All equivalent - choose your style!
progressify(data, count).at(message)
progressify(data, count).for_(message)  
progressify(data, count).in_(message)
```

### Custom Progress Bars
Create your own progress bar by implementing the `ProgressBar` protocol:

```python
from telegrinder import Message

class FireBar:
    def __init__(self, length: int):
        self.length = length
        self._current_index = 0
    
    def inc_index(self):
        if self._current_index < self.length:
            self._current_index += 1
    
    async def update(self, message: Message):
        filled = self._current_index
        empty = self.length - filled
        bar = "=%" * filled + "�" * empty
        percent = (self._current_index / self.length) * 100
        line = f"{bar} {percent:.1f}%"
        await message.edit(text=message.text.unwrap_or("") + f"\n\n{line}")

# Use your custom bar
async for item in progressify(data, total).at(message).using(FireBar(total)):
    await process_item(item)
```

### Configuration Options
Fine-tune your progress bars:

```python
moon_bar = MoonBar(
    length=20,
    width=8,           # Number of emoji cells
    label="Processing", # Custom label
    show_counts=True,   # Show "7/20"
    show_percent=True   # Show "35.0%"
)
```

## <� Use Cases

- **File Processing**: Show upload/download progress
- **Data Analysis**: Track computation steps  
- **Batch Operations**: Visualize bulk actions
- **API Calls**: Monitor request processing
- **Content Generation**: Track creation progress

## < Why telebar?

- **<� Beautiful**: Eye-catching progress bars that users love
- **� Fast**: Lightweight and efficient
- **=' Flexible**: Easy to customize and extend
- **< Unique**: Distinctive moon phase animations
- **=� Telegram Native**: Built specifically for Telegram bots

## =� License

MIT License - Build amazing things! =�