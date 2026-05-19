"""
LLM client layer.

This module is the ONE place you need to change to go from the mocked MVP
to a real LLM-powered system. Every agent talks to an `LLMClient` through
the same `.generate(prompt, context)` method, so swapping the implementation
does not require touching any agent code.

Currently `MockLLMClient` is used. It returns deterministic, structured
Markdown so the whole funnel runs end-to-end without API keys or network.

To go live, implement `generate()` in `AnthropicLLMClient` (or build an
`OpenAILLMClient`) and return that instance from `get_llm_client()`.
"""

from __future__ import annotations

from typing import Any, Dict

from llm import mock_content


class LLMClient:
    """Interface every concrete client must implement."""

    def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        """
        Args:
            prompt:  The fully-rendered prompt text (template + project data).
            context: Extra structured data. Always contains:
                       - "stage":   the funnel stage id (e.g. "discovery")
                       - "project": the full project dict

        Returns:
            Markdown text produced by the model.
        """
        raise NotImplementedError


class MockLLMClient(LLMClient):
    """
    Deterministic stand-in for a real model.

    It ignores the prompt string and instead renders structured Markdown
    from the project data using `llm/mock_content.py`. This keeps the MVP
    fully runnable offline while preserving the exact call signature a real
    client will use.
    """

    def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        stage = context["stage"]
        project = context["project"]
        renderer = mock_content.RENDERERS.get(stage)
        if renderer is None:
            return f"# {stage.title()}\n\n_No mock renderer registered for this stage._\n"
        return renderer(project)


class AnthropicLLMClient(LLMClient):
    """
    Real client skeleton. Fill this in when you are ready to go live.

    Steps:
      1. pip install anthropic
      2. export ANTHROPIC_API_KEY=...
      3. Uncomment the implementation below and return this client
         from `get_llm_client()`.
    """

    def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        # ------------------------------------------------------------------
        # REAL LLM CALL GOES HERE.
        #
        # import os
        # from anthropic import Anthropic
        #
        # client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        # message = client.messages.create(
        #     model="claude-sonnet-4-20250514",
        #     max_tokens=2000,
        #     messages=[{"role": "user", "content": prompt}],
        # )
        # return message.content[0].text
        #
        # (For OpenAI, swap in the openai SDK here instead — same idea:
        #  send `prompt`, return the model's text response.)
        # ------------------------------------------------------------------
        raise NotImplementedError(
            "AnthropicLLMClient.generate() is not implemented yet. "
            "See the comment block in llm/client.py."
        )


def get_llm_client() -> LLMClient:
    """
    Single source of truth for which client the app uses.

    Swap the return value here to go live:
        return AnthropicLLMClient()
    """
    return MockLLMClient()
