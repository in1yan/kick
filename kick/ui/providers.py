from textual.command import Provider, Hit, Hits


class CommandProvider(Provider):
    async def search(self, query: str) -> Hits:

        matcher = self.matcher(query)

        app = self.app
        current_model = app.config.agent.model
        command = f"Model: {current_model}"
        score = matcher.match(command)
        if score > 0:
            yield Hit(
                score,
                matcher.highlight(command),
                app.show_model_selector,
                help="Change the current model",
            )
