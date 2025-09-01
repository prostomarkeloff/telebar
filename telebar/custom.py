import typing
from telegrinder import Message
from telebar.bar import ProgressBar


class MoonBar(ProgressBar):
    """
    Moon-phase progress bar.

    Renders a fixed-width bar using phases:
        empty → 🌑 , partial → 🌒/🌓/🌔 , full → 🌕

    Example output:
        Progress  🌕🌕🌔🌑🌑  7/12 (58.3%)

    length : int
        Total number of items to process.
    width : int, default 6
        How many emoji "cells" to draw.
    label : str | None, default "Progress"
        Optional text prefix.
    show_counts : bool, default True
        Show (current/length).
    show_percent : bool, default True
        Show percentage with one decimal digit.
    """

    # (empty, quarter, half, three-quarter, full)
    DEFAULT_PHASES: typing.ClassVar[tuple[str, str, str, str, str]] = ("🌑", "🌒", "🌓", "🌔", "🌕")

    def __init__(
        self,
        length: int,
        *,
        width: int = 6,
        label: str | None = "Progress",
        show_counts: bool = True,
        show_percent: bool = True
    ) -> None:
        if length <= 0:
            raise ValueError("length must be > 0")
        if width <= 0:
            raise ValueError("width must be > 0")

        self.length = length
        self.width = width
        self.label = label or ""
        self.show_counts = show_counts
        self.show_percent = show_percent

        self._current_index = 0

    @property
    def current(self) -> int:
        """Processed items count (clamped)."""
        return min(self._current_index, self.length)

    @property
    def percent(self) -> float:
        """Progress from 0.0 to 100.0 (clamped)."""
        if self.length == 0:
            return 0.0
        # clamp in case of extra increments
        p = (self.current / self.length) * 100.0
        return 0.0 if p < 0 else (100.0 if p > 100.0 else p)

    def inc_index(self) -> None:
        """Advance progress by 1 (safe to call past the end)."""
        if self._current_index < self.length:
            self._current_index += 1

    async def update(self, message: Message) -> None:
        """Append a pretty single-line bar to the message text."""
        line = self._compose_line()
        await message.edit(text=message.text.unwrap_or("") + "\n\n" + line)

    def _compose_line(self) -> str:
        parts: list[str] = []

        if self.label:
            parts.append(self.label)

        parts.append(self._render_bar())

        meta: list[str] = []
        if self.show_counts:
            meta.append(f"{self.current}/{self.length}")
        if self.show_percent:
            meta.append(f"{self.percent:.1f}%")
        if meta:
            parts.append("(" + " · ".join(meta) + ")")

        return "  ".join(parts)

    def _render_bar(self) -> str:
        # map total progress to N full cells + 0..1 partial + remaining empties
        exact_cells = (self.percent / 100.0) * self.width
        full_cells = int(exact_cells)
        frac = exact_cells - full_cells

        empty, quarter, half, threeq, full = self.DEFAULT_PHASES

        cells: list[str] = []
        # full
        if full_cells > 0:
            cells.append(full * min(full_cells, self.width))

        # partial (only if room left and a fractional remainder exists)
        if full_cells < self.width and frac > 0:
            # 0 < frac <= 1 → {quarter, half, three-quarter}
            # thresholds chosen to look balanced visually
            if frac < 1 / 3:
                cells.append(quarter)
            elif frac < 2 / 3:
                cells.append(half)
            else:
                cells.append(threeq)

        # empty
        remaining = self.width - sum(len(chunk) for chunk in cells)
        if remaining > 0:
            cells.append(empty * remaining)

        return "".join(cells)
