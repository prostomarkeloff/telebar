import typing
from telegrinder import Message
from telebar.bar import DefaultProgressBar, ProgressBar


type Iterable[T] = typing.Iterable[T] | typing.AsyncIterable[T]

async def _async_iter[T](orig_iter: typing.Iterator[T]) -> typing.AsyncIterator[T]:
    for item in orig_iter:
        yield item

def any_iter_to_async_iter[T](iterable: Iterable[T]) -> typing.AsyncIterator[T]:
    if hasattr(iterable, "__aiter__"):
        iterable = typing.cast(typing.AsyncIterable[T], iterable)
        return iterable.__aiter__()
    else:
        iterable = typing.cast(typing.Iterable[T], iterable)
        return _async_iter(iterable.__iter__())


class progressify[T]:
    def __init__(self, items: Iterable[T], length: int):
        self._items = items
        self.length = length
        self._iterator: typing.AsyncIterator[T] | None = None
        self._message: Message | None = None
        self._bar = DefaultProgressBar(length)

    def for_(self, message: Message) -> typing.Self:
        self._message = message
        return self

    def in_(self, message: Message) -> typing.Self:
        return self.for_(message)

    def at(self, message: Message):
        return self.for_(message)

    def using(self, bar: ProgressBar):
        self._bar = bar
        return self

    @property
    def iterator(self) -> typing.AsyncIterator[T]:
        if self._iterator is None:
            self._iterator = any_iter_to_async_iter(self._items)
        return self._iterator

    def __aiter__(self) -> typing.Self:
        return self

    async def __anext__(self) -> T:
        if not self._message or not self._bar:
            raise ValueError("Message or bar are missingß")

        async for item in self.iterator:
            self._bar.inc_index()
            await self._bar.update(self._message)
            return item
        raise StopAsyncIteration
