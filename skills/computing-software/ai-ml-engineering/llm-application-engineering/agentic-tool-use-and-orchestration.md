---
id: computing-software.ai-ml-engineering.llm-application-engineering.agentic-tool-use-and-orchestration
name: agentic-tool-use-and-orchestration
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm, agents, tool-use, function-calling, orchestration, react, multi-step-reasoning, guardrails, loop-detection, agent-failure-modes, planning, tool-selection, context-window-management]
level: advanced
status: docs-checked
description: "Build LLM agents that call tools reliably: tool schema design, loop/retry limits, error feedback to the model, and the specific ways agent loops fail in production."
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agentic tool use: building loops that don't run away

**Goal:** an agent loop (LLM calls tools, observes results, decides next step) that converges on real tasks and fails safely when it doesn't.

## 1. Start simple, pick the pattern (Anthropic)
- Anthropic distinguishes **workflows** (LLMs and tools orchestrated through predefined code paths) from **agents** (LLMs dynamically direct their own process and tool use). Find the simplest solution and add complexity only when it demonstrably improves outcomes; for many applications a single LLM call with retrieval and in-context examples is enough. Agentic systems trade latency and cost for task performance.
- Workflow patterns: prompt chaining (fixed subtasks, optional programmatic gates between steps), routing (classify then specialise; for example easy questions to a smaller model), parallelization (sectioning independent subtasks, or voting), orchestrator-workers (subtasks not predictable in advance, such as multi-file code changes), evaluator-optimizer (generate and critique in a loop when criteria are clear).
- Agents suit open-ended problems where the number of steps cannot be predicted. They are "typically just LLMs using tools based on environmental feedback in a loop"; at each step they need ground truth from the environment (tool results, code execution), may pause for human feedback at checkpoints, and should have stopping conditions such as a maximum number of iterations. Autonomy means higher costs and compounding errors, so test extensively in sandboxes with guardrails.
- Frameworks can obscure prompts and responses; start with the LLM API directly and understand any framework's underlying code.

## 2. Tool schema design is most of the reliability
Anthropic's guidance on the agent-computer interface (ACI), invest as much as in human-computer interfaces:
- Put yourself in the model's shoes: a good tool definition often includes example usage, edge cases, input format requirements and clear boundaries from other tools; write parameter names and descriptions like a docstring for a junior developer, especially with many similar tools.
- Test how the model uses your tools with many example inputs and iterate; "poka-yoke" the arguments so mistakes are harder. Anthropic's SWE-bench agent had the model make mistakes with relative file paths once it left the root directory; requiring absolute paths fixed it, and they spent more time optimising tools than the overall prompt.
- Choose output formats the model finds easy: give it room to think before it commits, stay close to naturally occurring text (markdown over code in JSON, which needs escaping), and avoid overhead like counting lines for a diff.
Practitioner advice (not in the post): disambiguate same-named parameters (`order_id`, `user_id`); prefer fewer, well-separated tools and measure selection accuracy on your own eval as the tool count grows; return structured, truncated or paginated results rather than raw dumps.

## 3. The loop (practitioner advice)
- Standard shape: model emits a tool call, you execute it, append the result (including the real error message, so the model can self-correct), call the model again.
- Cap iterations and wall-clock time in code; detect exact-repeat tool calls and return corrective feedback instead of letting them loop.
- Define an explicit stop condition (a final-answer tool or termination format) instead of inferring "done" from no tool call.
- For long plans, plan-then-execute is easier to log and debug than re-deciding the whole plan each turn; Anthropic's principle is to show the agent's planning steps explicitly (transparency).

## 4. Failure modes specific to agents (practitioner advice)
- **Context bloat:** tool results accumulate; re-inject core instructions or compact older results.
- **Compounding hallucination:** have the agent cite which tool result supports a claim and spot-check.
- **Over-eager tool use:** add an instruction and an example of answering directly; measure tool calls on inputs that need none.
- **Destructive actions:** gate writes, deletes, payments and external messages with code-level confirmation or dry-run, not the system prompt alone.
- **Partial failure:** decide deliberately how a failed call in a multi-call turn is surfaced; never drop its result silently.

## Verify
- [ ] A single-call or workflow solution was considered before building an agent.
- [ ] Every tool has a description a new engineer could follow without reading the implementation.
- [ ] Iteration cap and wall-clock timeout enforced in code.
- [ ] Irreversible tool actions gated by a code-level confirmation or dry-run.
- [ ] Agent tested in a sandbox with guardrails before production.

## Checked
Method: docs-checked 2026-11-09 against the Anthropic Building effective agents post (read in full). Dropped: the docs.anthropic.com tool-use source (not read) and the claims that tool-selection accuracy degrades past 15-20 tools and that plan-then-execute is more token-efficient (not in the post). The original source URL pointed to /research/; the post lives under /engineering/. Sections 3 and 4 and the labelled practitioner lines are unsourced advice.
