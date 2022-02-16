"""Stores program context as side input to intent parsing and actions."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Context:
    """Store program context to aid intent parsers.

    Args:
        episode_history: List of episode ids
        active_window: Current in-focus window with GUI
    """
    MAX_EPISODES = 10

    episode_history: List[str] = field(default_factory=list)
    active_window: str = None
    running_applications: List[str] = field(default_factory=list)

    def add_episode(self, episode_id: str):
        self.episode_history.append(episode_id)
        self.episode_history = self.episode_history[-self.MAX_EPISODES:]
