from rich.align import Align
from rich import box
from rich.console import RenderableType
from textual import events
from textual.app import ComposeResult
from textual.widget import Widget
from rich.text import Text
from rich.panel import Panel
from textual.widgets import Label

from ...utils.parser import MAIN_PARSER

parser = MAIN_PARSER


class NumberScroll(Widget):
    """
    A number scroll that acts as an option to set a particular value
    """

    def __init__(
        self,
        name: str,
        step: int = 1,
        min_value: int = 0,
        max_value: int = 500,
        section: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self.section = section
        self.name_ = name
        if section:
            self.value = int(parser.get(section, name))
        self.step = step
        self.max_value = max_value
        self.min_value = min_value
        self.selected = False

    def highlight(self) -> None:
        self.selected = True
        self.refresh()

    def lowlight(self) -> None:
        self.selected = False
        self.refresh()

    def update(self) -> None:
        if self.section:
            parser.set(self.section, self.name_, str(self.value))
        self.refresh()

    def select_next_option(self) -> None:
        self.value = min(self.step + self.value, self.max_value)
        self.update()

    def select_prev_option(self) -> None:
        self.value = max(self.value - self.step, self.min_value)
        self.update()

    def on_mouse_scroll_down(self, _: events.MouseScrollDown) -> None:
        self.select_next_option()

    def on_mouse_scroll_up(self, _: events.MouseScrollUp) -> None:
        self.select_prev_option()

    def compose(self) -> ComposeResult:
        yield Label(Text(str(self.value).center(5), style="reverse green"))
