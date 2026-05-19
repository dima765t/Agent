"""Stage 6 - Launch: pre-launch, go-live and post-launch monitoring."""
from agents.base_agent import BaseAgent


class LaunchAgent(BaseAgent):
    stage = "launch"
    display_name = "Launch"
