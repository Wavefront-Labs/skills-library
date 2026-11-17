---
id: computing-software.ai-ml-engineering.llm-application-engineering.agent-workflow-patterns-orchestrator-evaluator
name: agent-workflow-patterns-orchestrator-evaluator
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, agents, agentic-workflows, orchestrator-workers, evaluator-optimizer, routing, parallelization]
level: practitioner
status: docs-checked
description: "Choose and implement agentic workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers and evaluator-optimizer, and when an autonomous agent is warranted."
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://www.anthropic.com/engineering/multi-agent-research-system
  - https://platform.openai.com/docs/guides/agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent workflow patterns

Start with the simplest thing that works: a single call with retrieval and good examples. Add structure only when evals show it helps. **Workflows** run LLMs through code-defined paths; **agents** let the model direct its own tool use in a loop.

## Patterns
**Prompt chaining** - fixed sequence with gates (outline -> check -> write). Use when the task splits cleanly into steps.

**Routing** - classify the input, send to a specialised prompt/model (refund vs technical vs sales; easy -> small model, hard -> large).

**Parallelization** - *sectioning* (independent subtasks concurrently, e.g., guardrail check alongside answer) or *voting* (same task several times, aggregate; e.g., multiple reviewers for vulnerability detection).

**Orchestrator-workers** - a lead model decomposes a task whose subtasks are not known in advance, dispatches workers, synthesises results:
```python
plan = call(LEAD, f"Break this research question into 3-6 independent sub-questions as JSON: {q}", schema=Plan)
findings = await asyncio.gather(*(worker(sub, model=WORKER) for sub in plan.subquestions))
answer = call(LEAD, render("synthesize.txt", question=q, findings=findings))
```
Give workers complete, self-contained instructions (objective, output format, tools, boundaries); vague delegation causes duplicated or missed work. Anthropic's research system reported that multi-agent systems use about 15x more tokens than chat interactions - worth it only for high-value, parallelisable tasks.

**Evaluator-optimizer** - one call generates, another critiques against explicit criteria, loop until pass or N rounds:
```python
draft = generate(task)
for _ in range(3):
    review = call(EVAL, f"<criteria>{criteria}</criteria><draft>{draft}</draft>", schema=Review)
    if review.passes:
        break
    draft = generate(task, feedback=review.issues)
```
Works when criteria are clear and feedback measurably improves output (translation nuance, code that must pass tests). Prefer objective checks (tests, validators) over LLM judgement where possible.

**Autonomous agent** - model plans and uses tools in a loop until done. Use for open-ended tasks with an unpredictable number of steps, in environments with feedback (tests, tool results) and recoverable errors. Add stop conditions (max turns, budget), checkpoints for human review, and sandboxed tools.

## Choosing
| Signal | Pattern |
|---|---|
| Fixed steps | chaining |
| Distinct input categories | routing |
| Independent subtasks / need confidence | parallelization |
| Subtasks unknown upfront | orchestrator-workers |
| Clear quality criteria, iterative refinement helps | evaluator-optimizer |
| Open-ended, many tool steps | agent |

## Verify
- [ ] Each added layer justified by an eval improvement versus the simpler baseline, with cost and latency recorded.
- [ ] Loops have explicit iteration and token caps.

## Checked
2026-11-01. Confirmed against Anthropic's Building effective agents (workflows vs agents, chaining, routing, sectioning and voting with the guardrail and code-vulnerability examples, orchestrator-workers, evaluator-optimizer with translation example, sandboxing and guardrails for agents) and the multi-agent research system post (subagents need an objective, output format, tool guidance; multi-agent about 15x more tokens than chat). Code blocks are illustrative pseudocode.
Method: documentation only; no commands were run.
