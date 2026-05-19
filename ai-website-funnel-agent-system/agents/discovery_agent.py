"""Stage 1 - Discovery: clarify business goals, audience and requirements.

Unlike the other stage agents (which still use the deterministic MockLLMClient),
the Discovery agent calls Anthropic's Claude API directly to produce a real
Discovery Summary. If the API key is missing or the call fails, it falls back
to the mock output so the funnel still runs end-to-end offline.
"""
from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent

# Load variables from a local .env file once, at import time.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed yet; rely on real environment variables.
    pass


CLAUDE_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2000


class DiscoveryAgent(BaseAgent):
    stage = "discovery"
    display_name = "Discovery"

    def run(self, project: Dict[str, Any]) -> str:
        prompt = self.build_prompt(project)

        markdown = self._generate_with_claude(prompt)
        if markdown is None:
            markdown = self._fallback(prompt, project)

        self._save_output(project, markdown)
        return markdown

    # --- real LLM call ----------------------------------------------------

    def _generate_with_claude(self, prompt: str) -> Optional[str]:
        """Return Claude's Markdown, or None to signal "use the fallback"."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print(
                "  [discovery] ANTHROPIC_API_KEY not set - using mock fallback.",
                file=sys.stderr,
            )
            return None

        try:
            from anthropic import Anthropic
        except ImportError:
            print(
                "  [discovery] anthropic package not installed "
                "(pip install -r requirements.txt) - using mock fallback.",
                file=sys.stderr,
            )
            return None

        try:
            client = Anthropic(api_key=api_key)
            message = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as exc:
            print(
                f"  [discovery] Claude API call failed "
                f"({exc.__class__.__name__}: {exc}) - using mock fallback.",
                file=sys.stderr,
            )
            return None

    # --- fallback ---------------------------------------------------------

    def _fallback(self, prompt: str, project: Dict[str, Any]) -> str:
        """Delegate to whatever client was injected (MockLLMClient in the MVP)."""
        return self.llm.generate(
            prompt,
            context={"stage": self.stage, "project": project},
        )
