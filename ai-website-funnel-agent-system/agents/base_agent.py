"""
BaseAgent: shared behaviour for every funnel-stage agent.

Each concrete agent only declares:
  - `stage`        : short id, also the prompt filename and mock key
  - `display_name` : human-readable label

Everything else (load prompt template, fill it with project data, call the
LLM, save Markdown) is handled here, so the system stays modular and DRY.
"""

from __future__ import annotations

import os
from typing import Any, Dict

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")


class BaseAgent:
    stage: str = ""          # overridden by subclasses, e.g. "discovery"
    display_name: str = ""   # overridden by subclasses, e.g. "Discovery"

    def __init__(self, llm_client):
        self.llm = llm_client

    # --- prompt handling --------------------------------------------------

    def _load_prompt_template(self) -> str:
        """Read this stage's prompt template from prompts/<stage>.md."""
        path = os.path.join(PROMPTS_DIR, f"{self.stage}.md")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def build_prompt(self, project: Dict[str, Any]) -> str:
        """
        Fill the template's {placeholders} with project values.

        Missing keys are tolerated so adding new project fields later
        does not break older templates.
        """
        template = self._load_prompt_template()
        try:
            return template.format(**project)
        except KeyError:
            # Fall back to safe substitution if a placeholder is unknown.
            class _Safe(dict):
                def __missing__(self, key):  # noqa: D401
                    return "{" + key + "}"

            return template.format_map(_Safe(project))

    # --- run --------------------------------------------------------------

    def run(self, project: Dict[str, Any]) -> str:
        """Build the prompt, call the LLM, persist the Markdown output."""
        prompt = self.build_prompt(project)

        # The LLM call. With the mock client this is deterministic; with a
        # real client this sends `prompt` to Claude/OpenAI. Same signature.
        markdown = self.llm.generate(
            prompt,
            context={"stage": self.stage, "project": project},
        )

        self._save_output(project, markdown)
        return markdown

    # --- output -----------------------------------------------------------

    def _save_output(self, project: Dict[str, Any], markdown: str) -> None:
        project_dir = os.path.join(OUTPUTS_DIR, project["project_id"])
        os.makedirs(project_dir, exist_ok=True)
        out_path = os.path.join(project_dir, f"{self.stage}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(markdown)
