from textual.widgets import Static, Markdown
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
