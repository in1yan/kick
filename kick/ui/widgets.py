from textual.widgets import Static, Markdown, TextArea
from textual.message import Message
import random


class Welcome(Static):
    pass


class Spinner(Markdown):
    FRAMES = ["{/////}", "{~////}", "{/~///}", "{//~//}", "{////~}"]
    MESSAGES = [
        "Thinking ...",
        "Building a ramp...",
        "Launching stunt...",
        "Defying physics...",
        "Revving engines...",
        "Helmet on...",
        "Daredevil mode...",
        "Aiming for awesome...",
        "Full send...",
        "What could possibly go wrong?",
    ]
    FRAME_INTERVAL = 0.2
    MESSAGE_TICK_RATE = 50

    def on_mount(self):
        self.frame = -1
        self.tick = 0
        self.current_message = random.choice(self.MESSAGES)
        self.update(f"{self.FRAMES[self.frame]} {self.current_message}")
        self.timer = self.set_interval(self.FRAME_INTERVAL, self.animate)

    def animate(self):
        self.frame = (self.frame + 1) % len(self.FRAMES)
        if self.tick % self.MESSAGE_TICK_RATE == 0:
            self.current_message = random.choice(self.MESSAGES)
        self.update(f"{self.FRAMES[self.frame]} {self.current_message}")
        self.tick += 1

    def stop(self):
        self.timer.stop()


class Prompt(TextArea):
    class Submitted(Message):
        def __init__(self, value: str):
            self.value = value
            super().__init__()

    async def on_mount(self):
        self.styles.height = 3

    async def on_key(self, event):
        if event.key == "enter":
            event.prevent_default()
            event.stop()
            self.post_message(self.Submitted(self.text))
            return
        if event.key == "shift+enter":
            self.insert("\n")
            event.prevent_default()
            event.stop()
            return
        await super()._on_key(event)

    async def on_text_area_changed(self, event):

        self.styles.height = max(
            3,
            min(self.document.line_count, 8),
        )

        self.refresh(layout=True)
