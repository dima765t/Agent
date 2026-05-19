"""
AI Website Funnel Agent System - CLI entry point.

Run:
    python main.py

Flow:
    1. Collect basic client/project info from the user.
    2. Persist it as JSON under data/projects/<project_id>.json.
    3. Run all 7 stage agents in order.
    4. Save each agent's Markdown output under outputs/<project_id>/.
"""

from __future__ import annotations

import datetime
import json
import os
import re

from agents.discovery_agent import DiscoveryAgent
from agents.proposal_agent import ProposalAgent
from agents.planning_agent import PlanningAgent
from agents.design_agent import DesignAgent
from agents.development_agent import DevelopmentAgent
from agents.launch_agent import LaunchAgent
from agents.maintenance_agent import MaintenanceAgent
from llm.client import get_llm_client

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "projects")
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")

# Funnel order. Adding/reordering a stage is a one-line change here.
AGENT_PIPELINE = [
    DiscoveryAgent,
    ProposalAgent,
    PlanningAgent,
    DesignAgent,
    DevelopmentAgent,
    LaunchAgent,
    MaintenanceAgent,
]


def _slugify(text: str) -> str:
    """Make a filesystem-safe id from a project name."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "project"


def _ask(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    answer = input(f"{label}{suffix}: ").strip()
    return answer or default


def collect_project() -> dict:
    """Interactively gather client/project info."""
    print("\n=== New Website Funnel Project ===\n")
    client_name = _ask("Client name", "Acme Co")
    project_name = _ask("Project name", "Acme Website")
    industry = _ask("Industry", "General")
    goal = _ask("Primary goal", "Generate more qualified leads")
    target_audience = _ask("Target audience", "Local small-business owners")
    budget = _ask("Budget", "TBD")
    notes = _ask("Notes / special requirements", "None")

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    project_id = f"{_slugify(project_name)}-{timestamp}"

    return {
        "project_id": project_id,
        "client_name": client_name,
        "project_name": project_name,
        "industry": industry,
        "goal": goal,
        "target_audience": target_audience,
        "budget": budget,
        "notes": notes,
        "created_at": timestamp,
    }


def save_project(project: dict) -> str:
    """Persist project data as JSON; returns the file path."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{project['project_id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(project, f, indent=2, ensure_ascii=False)
    return path


def run_pipeline(project: dict) -> None:
    """Run every stage agent in order, saving each Markdown output."""
    llm = get_llm_client()
    print(f"\nRunning {len(AGENT_PIPELINE)} agents for "
          f"'{project['project_name']}'...\n")

    for AgentClass in AGENT_PIPELINE:
        agent = AgentClass(llm)
        agent.run(project)
        print(f"  [done] {agent.display_name:<12} -> "
              f"outputs/{project['project_id']}/{agent.stage}.md")


def main() -> None:
    project = collect_project()
    json_path = save_project(project)
    print(f"\nSaved project data: {json_path}")

    run_pipeline(project)

    out_dir = os.path.join(OUTPUTS_DIR, project["project_id"])
    print(f"\nAll outputs written to: {out_dir}\n")


if __name__ == "__main__":
    main()
