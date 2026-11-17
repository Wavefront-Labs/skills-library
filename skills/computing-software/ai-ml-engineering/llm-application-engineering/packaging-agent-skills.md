---
id: computing-software.ai-ml-engineering.llm-application-engineering.packaging-agent-skills
name: packaging-agent-skills
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, agent-skills, skill-md, claude-code, progressive-disclosure, code-execution]
level: practitioner
status: docs-checked
description: "Package reusable agent expertise as Agent Skills: SKILL.md frontmatter and body, progressive disclosure with bundled files and scripts, use in Claude Code, the API and apps."
sources:
  - https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
  - https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
  - https://docs.claude.com/en/api/skills-guide
  - https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Agent Skills packaging

**Goal:** domain procedures (how to build our reports, how to triage our incidents) are packaged once and loaded by agents only when relevant, without bloating every prompt.

## Structure
```
quarterly-report/
  SKILL.md            # required
  reference/style.md  # loaded only if needed
  templates/report.xlsx
  scripts/build_charts.py
```
`SKILL.md`:
```markdown
---
name: quarterly-report
description: Builds Acme quarterly finance reports from the ledger export. Use when asked for a quarterly report, QBR numbers or finance summary decks.
---
# Quarterly report
1. Validate the export with `python scripts/validate.py <file>`; stop and report errors.
2. ...
For chart styling see reference/style.md.
```

## Progressive disclosure
1. Only `name` + `description` of every installed skill sit in context (cheap) - so the description must say what it does and when to use it.
2. When relevant, the agent reads the `SKILL.md` body.
3. Referenced files and scripts are read or executed only as needed; scripts run without their source entering context.
Keep the `SKILL.md` body under 500 lines; move detail into reference files one level deep.

## Where skills run
- **Claude Code:** personal skills in `~/.claude/skills/<name>/`, project skills in `.claude/skills/<name>/` (checked into the repo), or via plugins.
- **Claude API:** skills run in the code execution container. Pass `container={"skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}, {"type": "custom", "skill_id": "<id>", "version": "latest"}]}` with the code execution tool; upload custom skills through the Skills API (`/v1/skills` endpoints). Anthropic provides pre-built skills (pptx, xlsx, docx, pdf).
- **Claude apps:** upload a zipped skill in settings.

## Writing good skills
- Write for a capable reader: concrete steps, commands, gotchas; skip general knowledge.
- Prefer scripts for deterministic, fragile operations; instructions for judgment.
- Test with real tasks: does the agent pick the skill up from the description alone? Does it follow steps?
- Version skills; review changes like code.

## Security
Skills can contain instructions and executable code. Install only from trusted sources, review scripts, and watch for skills that fetch remote content or exfiltrate data.

## Checked
2026-11-01. Confirmed against the Agent Skills overview and best-practices pages and the Skills API guide: progressive disclosure levels, scripts run without their code entering context, `~/.claude/skills/` and `.claude/skills/`, container skills list shape (`type`, `skill_id`, `version`), `/v1/skills`, pre-built skill ids, zip upload in Settings, the 500-line guidance, one-level-deep references, trusted-source warning. Removed: the Agent SDK line and the `client.skills.*` method name.
Method: documentation only; no commands were run.

## Verify
- [ ] The skill triggers on representative requests and not on unrelated ones.
- [ ] Scripts run in the target environment (dependencies available, no network assumptions).
