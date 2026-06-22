import tomllib
import tomli_w
from pathlib import Path
from dataclasses import dataclass, asdict, field

CONFIG_PATH = Path.home() / ".kick" / "config.toml"


@dataclass
class UIConfig:
    theme: str = "rose-pine"


@dataclass
class AgentConfig:
    model: str = "groq:openai/gpt-oss-120b"
    max_steps: int = 20
    recent_models: list[str] = field(default_factory=list)


@dataclass
class Config:
    ui: UIConfig = field(default_factory=UIConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)


def load_config():
    if not CONFIG_PATH.exists():
        write_config(Config())
    with open(CONFIG_PATH, "rb") as file:
        data = tomllib.load(file)
        return Config(
            ui=UIConfig(**data.get("ui", {})),
            agent=AgentConfig(**data.get("agent", {})),
        )


def write_config(config: Config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, mode="wb") as file:
        tomli_w.dump(asdict(config), file)
    return config


config = load_config()
