from __future__ import annotations

from typing import TYPE_CHECKING, Any

from textual.widgets import TextArea

from composeui.core.signal import Signal, SignalNoArgs

if TYPE_CHECKING:
    from textual import events


class ComposeTextArea(TextArea):
    """A `TextArea` that re-exposes its messages as plain composeui `Signal`s, as `ComposeInput`.

    `value_changed` also reports a text set by the app; `value_submitted` is emitted
    whenever the area loses the focus, since Enter starts a new line.
    """

    # four lines of text in a form, not all the height left; a form row's field while the
    # row is invalid (see `ROW_INVALID_CLASS`): as Input's own `-invalid`
    DEFAULT_CSS = """
    ComposeTextArea {
        height: 6;
    }
    ComposeTextArea.-row-invalid {
        border: tall $error 60%;
        &:focus {
            border: tall $error;
        }
    }
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.value_changed: Signal[str] = Signal()
        self.value_submitted: SignalNoArgs = SignalNoArgs()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        self.value_changed.emit(event.text_area.text)

    def on_blur(self, event: events.Blur) -> None:
        self.value_submitted.emit()
