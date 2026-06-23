from kick.config import write_config
from kick.agent import create_agent


def switch_model(app, model):
    if not model:
        return
    recents = app.config.agent.recent_models
    if model in recents:
        recents.remove(model)
    recents.insert(0, model)
    app.config.agent.model = model
    write_config(app.config)
    app.agent = create_agent(app.config)
    app.notify(f"Model changed to {app.config.agent.model}")
