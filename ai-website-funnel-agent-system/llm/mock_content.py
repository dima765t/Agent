"""
Deterministic Markdown renderers used by MockLLMClient.

Each function takes the project dict and returns Markdown for one funnel
stage. This is throwaway logic that exists only so the MVP produces
realistic, structured output without a real model. When you connect a
real LLM, this whole file becomes unused (the prompt + project data are
sent to the model instead).
"""

from __future__ import annotations

from typing import Any, Callable, Dict


def _header(project: Dict[str, Any], title: str) -> str:
    return (
        f"# {title}\n\n"
        f"**Client:** {project['client_name']}  \n"
        f"**Project:** {project['project_name']}  \n"
        f"**Industry:** {project['industry']}  \n"
        f"**Generated stage:** {title}\n\n"
        "---\n\n"
    )


def discovery(p: Dict[str, Any]) -> str:
    return _header(p, "Discovery Summary") + (
        "## Business Overview\n"
        f"{p['client_name']} operates in the **{p['industry']}** sector. "
        f"The objective of *{p['project_name']}* is: {p['goal']}.\n\n"
        "## Target Audience\n"
        f"- Primary audience: {p['target_audience']}\n"
        f"- Budget signal: {p['budget']}\n\n"
        "## Key Requirements\n"
        f"- {p['notes']}\n"
        "- Clear value proposition above the fold\n"
        "- Mobile-first, fast-loading pages\n\n"
        "## Open Questions\n"
        "1. Who owns content and copy?\n"
        "2. Are there existing brand assets (logo, palette, fonts)?\n"
        "3. What does success look like 90 days post-launch?\n"
    )


def proposal(p: Dict[str, Any]) -> str:
    return _header(p, "Proposal") + (
        "## Scope of Work\n"
        f"Design and build a website for **{p['client_name']}** to achieve: "
        f"{p['goal']}.\n\n"
        "## Deliverables\n"
        "- Responsive marketing website (up to 5 pages)\n"
        "- Contact / lead capture form\n"
        "- Basic on-page SEO setup\n"
        "- One round of revisions per stage\n\n"
        "## Timeline (indicative)\n"
        "| Phase | Duration |\n"
        "|---|---|\n"
        "| Planning | 1 week |\n"
        "| Design | 2 weeks |\n"
        "| Development | 2-3 weeks |\n"
        "| Launch | 3 days |\n\n"
        "## Investment\n"
        f"Aligned with the stated budget: **{p['budget']}**. "
        "Final quote confirmed after planning.\n\n"
        "## Next Step\n"
        "Approve this proposal to move into the Planning stage.\n"
    )


def planning(p: Dict[str, Any]) -> str:
    return _header(p, "Planning Checklist") + (
        "## Pre-Work\n"
        "- [ ] Kickoff call scheduled\n"
        "- [ ] Stakeholders and decision-maker confirmed\n"
        "- [ ] Brand assets collected\n\n"
        "## Information Architecture\n"
        "- [ ] Sitemap drafted and approved\n"
        "- [ ] Page-by-page content outline\n"
        "- [ ] Conversion goals defined\n\n"
        "## Logistics\n"
        "- [ ] Domain & hosting access\n"
        "- [ ] Tooling / CMS chosen\n"
        f"- [ ] Milestones mapped to budget ({p['budget']})\n\n"
        "## Sign-off\n"
        f"- [ ] {p['client_name']} approves the plan to proceed to Design\n"
    )


def design(p: Dict[str, Any]) -> str:
    return _header(p, "Design Brief") + (
        "## Design Goal\n"
        f"Visual direction that supports: {p['goal']}.\n\n"
        "## Audience Tone\n"
        f"Designed for **{p['target_audience']}** in the {p['industry']} space.\n\n"
        "## Direction\n"
        "- Clean, trustworthy, conversion-focused layout\n"
        "- Clear visual hierarchy and prominent CTAs\n"
        "- Accessible color contrast (WCAG AA)\n\n"
        "## Screens to Design\n"
        "- [ ] Homepage\n"
        "- [ ] About / Services\n"
        "- [ ] Contact\n"
        "- [ ] Mobile variants\n\n"
        "## Deliverable\n"
        "High-fidelity mockups for client review and one revision round.\n"
    )


def development(p: Dict[str, Any]) -> str:
    return _header(p, "Development Checklist") + (
        "## Setup\n"
        "- [ ] Repository and environment initialized\n"
        "- [ ] Base layout / component system\n\n"
        "## Build\n"
        "- [ ] Implement approved designs (responsive)\n"
        "- [ ] Contact / lead form wired up\n"
        "- [ ] Content populated\n"
        "- [ ] Analytics installed\n\n"
        "## Quality\n"
        "- [ ] Cross-browser & mobile testing\n"
        "- [ ] Performance pass (Lighthouse)\n"
        "- [ ] Accessibility pass\n"
        "- [ ] On-page SEO verified\n\n"
        "## Handoff\n"
        f"- [ ] Staging link sent to {p['client_name']} for UAT\n"
    )


def launch(p: Dict[str, Any]) -> str:
    return _header(p, "Launch Checklist") + (
        "## Pre-Launch\n"
        "- [ ] Final client approval received\n"
        "- [ ] Backups taken\n"
        "- [ ] DNS / domain ready\n"
        "- [ ] SSL configured\n\n"
        "## Go-Live\n"
        "- [ ] Deploy to production\n"
        "- [ ] Smoke test all pages and forms\n"
        "- [ ] Submit sitemap to search engines\n\n"
        "## Post-Launch (first 48h)\n"
        "- [ ] Monitor analytics & error logs\n"
        "- [ ] Verify lead notifications working\n"
        f"- [ ] Confirm {p['goal']} tracking is live\n"
    )


def maintenance(p: Dict[str, Any]) -> str:
    return _header(p, "Maintenance Plan") + (
        "## Cadence\n"
        "- Weekly: uptime & backup verification\n"
        "- Monthly: dependency / security updates\n"
        "- Quarterly: performance & SEO review\n\n"
        "## Support\n"
        f"- Point of contact for {p['client_name']}\n"
        "- Defined response times for critical issues\n"
        "- Content update requests handled within SLA\n\n"
        "## Growth\n"
        f"- Review progress toward: {p['goal']}\n"
        "- Recommend iterative improvements based on analytics\n"
    )


# Stage id  ->  renderer. Agents reference these ids via their `stage` attr.
RENDERERS: Dict[str, Callable[[Dict[str, Any]], str]] = {
    "discovery": discovery,
    "proposal": proposal,
    "planning": planning,
    "design": design,
    "development": development,
    "launch": launch,
    "maintenance": maintenance,
}
