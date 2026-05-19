# AI Website Funnel Agent System

A lightweight, modular multi-agent system that manages a website-building
funnel for small-business clients — from first contact to long-term
maintenance.

The MVP runs entirely offline with a **mocked LLM** so you can see the full
pipeline work end-to-end. The code is structured so a real model
(Claude or OpenAI) can be plugged in by changing **one file**.

---

## Project Goal

Small web agencies and freelancers repeat the same seven-stage process for
every client. This system turns that process into a sequence of focused
**agents**, each responsible for one stage and each producing a clean,
structured Markdown deliverable from shared project data.

The result: consistent, fast, repeatable project artifacts with a single
source of truth.

---

## Workflow

The funnel runs these seven stages in order:

| # | Stage        | Deliverable             |
|---|--------------|-------------------------|
| 1 | Discovery    | Discovery Summary       |
| 2 | Proposal     | Proposal                |
| 3 | Planning     | Planning Checklist      |
| 4 | Design       | Design Brief            |
| 5 | Development  | Development Checklist   |
| 6 | Launch       | Launch Checklist        |
| 7 | Maintenance  | Maintenance Plan        |

Each stage receives the **same project data** and the **previous outputs on
disk**, then writes its own Markdown file.

---

## Agents

Every stage is a separate module under `agents/`, all extending
`BaseAgent`, which handles the shared work (load prompt template → fill
with project data → call the LLM → save Markdown).

```
agents/
  base_agent.py          # shared logic: prompt -> LLM -> save
  discovery_agent.py     # Stage 1
  proposal_agent.py      # Stage 2
  planning_agent.py      # Stage 3
  design_agent.py        # Stage 4
  development_agent.py    # Stage 5
  launch_agent.py        # Stage 6
  maintenance_agent.py    # Stage 7
```

A concrete agent is intentionally tiny — it only declares its `stage` id
and `display_name`. All behaviour lives in `BaseAgent`.

### Project structure

```
ai-website-funnel-agent-system/
├── main.py                 # CLI entry point (run this)
├── requirements.txt        # stdlib only for the MVP
├── README.md
├── agents/                 # one module per funnel stage
├── prompts/                # one Markdown prompt template per stage
├── llm/
│   ├── client.py           # <-- swap mock for real model HERE
│   └── mock_content.py     # deterministic offline output
├── data/projects/          # saved project JSON (one file per project)
└── outputs/                # generated Markdown (one folder per project)
```

---

## How to Run Locally

Requires **Python 3.8+**. No third-party packages needed for the MVP.

```bash
# 1. (optional) create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. install requirements (no-op for the MVP, kept for the real-LLM step)
pip install -r requirements.txt

# 3. run the CLI
python main.py
```

You'll be prompted for basic client/project info (press Enter to accept
defaults). The app then:

1. Saves project data to `data/projects/<project_id>.json`
2. Runs all 7 agents in order
3. Writes deliverables to `outputs/<project_id>/`

```
outputs/<project_id>/
  discovery.md
  proposal.md
  planning.md
  design.md
  development.md
  launch.md
  maintenance.md
```

---

## Connecting a Real LLM

The mock is isolated behind a single interface. To go live:

1. Open `llm/client.py`.
2. Implement `AnthropicLLMClient.generate()` (a ready-to-fill comment
   block with example code is already there). The same pattern works for
   OpenAI.
3. Change `get_llm_client()` to return your real client.
4. `pip install anthropic` (or `openai`) and set your API key.

No agent code changes. Prompt templates in `prompts/` are already written
to be sent straight to a real model.

---

## Future Improvements

- **Stage gating / approvals** — pause for human sign-off between stages.
- **Inter-agent context** — feed previous stage outputs into later prompts.
- **Resume / re-run** — re-run a single stage without restarting the funnel.
- **Persistence** — move from JSON files to SQLite for multi-project search.
- **Web UI** — replace the CLI with a small dashboard.
- **Config-driven pipeline** — define stages/order in a YAML file.
- **Output formats** — export to PDF or DOCX in addition to Markdown.
- **Tests** — unit tests for prompt rendering and the agent pipeline.

---

## Design Notes

- **Modular:** one file per agent, one prompt template per stage.
- **Swappable LLM:** every agent calls the same `generate(prompt, context)`.
- **Deterministic MVP:** runs offline, same input → same output.
- **Not over-engineered:** standard library only, no framework, no DI.
