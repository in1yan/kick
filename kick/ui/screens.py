from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import ListItem, ListView, Label, Input


class ModelSelectionModal(ModalScreen[str]):
    def __init__(self, recent_models: list[str], current_model: str):
        super().__init__()
        self.current_model = current_model
        self.recent_models = recent_models
        if not self.recent_models:
            self.recent_models.append(self.current_model)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Select a Model:")
            yield Input(value=self.current_model, id="model_input")
            yield ListView(
                *[ListItem(Label(model)) for model in self.recent_models],
                id="recent_models",
            )

    def on_input_submitted(self, event: Input.Submitted):
        event.stop()
        self.dismiss(event.value)

    async def on_input_changed(self, event: Input.Changed):
        query = event.value.lower()
        list_view = self.query_one("#recent_models", ListView)
        filtered_models = [
            model for model in self.recent_models if query in model.lower()
        ]
        list_view.clear()

        for model in filtered_models:
            await list_view.append(ListItem(Label(model)))

    def on_list_view_selected(
        self,
        event: ListView.Selected,
    ):
        label = event.item.query_one(Label)

        self.dismiss(str(label.content))
