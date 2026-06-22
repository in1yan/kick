import random
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll, Center, Middle
from textual.widgets import Header, Input, Markdown, Static, LoadingIndicator
from agent import agent
import os
from functions.read import read
from functions.ls import ls
from functions.write import write
from functions.edit import edit
from functions.bash import bash


class Welcome(Static):
    pass


class Spinner(Markdown):
    FRAMES = ["{/////}", "{~////}", "{/~///}", "{//~//}", "{////~}"]
    MESSAGES = [
        "Thinking ...Building a ramp...",
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
        self.frame = 0
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


class Kick(App):
    BINDINGS = [
        ("escape", "cancel_stream", "stop agent"),
    ]
    CSS = """
    #welcome_container {
            width: 100%;
            align: center middle;
        }
    #welcome {
        text-align: center;
        width: 100%;
    }
    """

    def __init__(self):
        super().__init__()
        self.message_history = []
        self.current_stream = None
        self.current_spinner = None
        self.is_response_loading = False

    async def run_agent(self, prompt: str, message_widget: Spinner):
        response = ""
        first_chunk = True
        async with agent.run_stream(
            prompt,
            deps=os.getcwd(),
            message_history=self.message_history,
        ) as stream:
            self.current_stream = stream
            async for chunk in stream.stream_text(delta=True):
                if first_chunk:
                    message_widget.stop()
                    first_chunk = False
                response += chunk
                message_widget.update(f"### Kick\n\n{response}")
            self.message_history = stream.all_messages()

    async def on_input_submitted(self, event: Input.Submitted):
        prompt = event.value
        event.input.value = ""
        messages = self.query_one("#messages", VerticalScroll)
        user_message = Markdown(f"> ### {prompt}")
        assistant_message = Spinner()
        self.current_spinner = assistant_message
        welcome = self.query("#welcome")
        if welcome:
            await welcome.first().remove()
        await messages.mount(user_message)
        await messages.mount(assistant_message)
        self.run_worker(self.run_agent(prompt, assistant_message))

        messages.scroll_end(animate=True)
        if prompt.strip() == "/exit":
            self.exit()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Vertical():
            yield Header(icon="🦸")
            with VerticalScroll(id="messages"):
                with Middle():
                    with Center():
                        with Vertical(id="welcome_container"):
                            yield Welcome(
                                """
[yellow]Kick[/]

       ░[#FE0000]▒▒▒▒▒[/]       
     █[#FE0000]▒▒▒▒[/]█████░    
   ░█[#FE0000]▓▒▒▒[/]████████   
   ██[#FE0000]▒▒▒▒[/]█████████  
  ░██[#FE0000]▒▒▒▒[/]█████████  
           [#FE0000]░[/]█████▒  
            █████   
             ░░     

Autonomous Coding Agent

    • Analyze repositories
    • Edit files
    • Execute commands
    • Run tests

    [red] /exit [/] - [yellow] exit the agent [/]
    [red] esc [/] - [yellow] stop the agent execution [/]
    [red] ctrl + p [/]  - [yellow] open command pallete [/]

Type a prompt below to begin.
                            """,
                                id="welcome",
                            )
            yield Input(placeholder="Build anything cool ..", id="prompt")

    async def on_mount(self):
        self.theme = "rose-pine"
        ip = self.query_one("#prompt", Input)
        ip.focus()

    async def action_cancel_stream(self) -> None:
        if self.current_stream:
            await self.current_stream.cancel()
            messages = self.query_one("#messages")
            if self.current_spinner:
                self.current_spinner.stop()
            messages.mount(Markdown("> Agent Cancelled"))


if __name__ == "__main__":
    app = Kick()
    app.run()
