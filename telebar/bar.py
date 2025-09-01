import typing
from telegrinder import Message

class ProgressBar(typing.Protocol):
    def inc_index(self):
        ...

    async def update(self, message: Message):
        ...

class DefaultProgressBar(ProgressBar):
    MAX_PERCENT = 100

    def __init__(self, length: int):
        self.length = length
        self._current_index = 0

    @property
    def current_percent(self):
        return self._current_index / self.length * self.MAX_PERCENT

    def inc_index(self):
        if self._current_index < self.length:
            self._current_index += 1

    def compose_line(self):
        filled = int(self.length * self.current_percent / self.MAX_PERCENT)
        text = f"[{'█' * filled}{' ' * (self.length - filled)}] {self.current_percent:.2f}%"
        return text

    async def update(self, message: Message):
        line = self.compose_line()
        await message.edit(text=message.text.unwrap_or(str())+ f"\n\n{line}")
