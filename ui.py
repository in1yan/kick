from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll, Center, Middle
from textual.widgets import Footer, Header, Input, Markdown, Static, Label
from agent import agent
import os
from functions.read import read
from functions.ls import ls
from functions.write import write
from functions.edit import edit
from functions.bash import bash


class Welcome(Static):
    pass


class Kick(App):
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
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

    async def run_agent(
        self,
        prompt: str,
        message_widget: Markdown,
    ):
        response = ""

        async with agent.run_stream(
            prompt,
            deps=os.getcwd(),
            message_history=self.message_history,
        ) as stream:
            self.current_stream = stream
            async for chunk in stream.stream_text(delta=True):
                response += chunk
                message_widget.update(f"### Kick\n\n{response}")
            self.message_history = stream.all_messages()

    async def on_input_submitted(self, event: Input.Submitted):
        prompt = event.value
        event.input.value = ""
        messages = self.query_one("#messages", VerticalScroll)
        user_message = Markdown(f"### You\n\n{prompt}")
        assistant_message = Markdown("### Kick\n\nThinking...")
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
        yield Header()
        with Vertical():
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
        yield Footer()

    async def on_mount(self):
        ip = self.query_one("#prompt", Input)
        ip.focus()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    async def action_cancel_stream(self) -> None:
        if self.current_stream:
            await self.current_stream.cancel()
            messages = self.query_one("#messages")
            messages.mount(Markdown("> Agent Cancelled"))


if __name__ == "__main__":
    app = Kick()
    app.run()
