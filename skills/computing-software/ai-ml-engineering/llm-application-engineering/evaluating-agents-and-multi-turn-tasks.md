---
id: computing-software.ai-ml-engineering.llm-application-engineering.evaluating-agents-and-multi-turn-tasks
name: evaluating-agents-and-multi-turn-tasks
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-evaluation, agent-evaluation, trajectory-evaluation, pass-at-k, simulated-users, sandboxed-environments]
level: practitioner
status: docs-checked
description: "Evaluate LLM agents: outcome checks on environment state, trajectory metrics, pass@k vs pass^k reliability, simulated users for multi-turn tasks, sandbox resets."
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://arxiv.org/abs/2406.12045
  - https://arxiv.org/abs/2310.06770
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluating agents and multi-turn tasks

**Goal:** measure whether an agent completes tasks correctly and reliably, not whether a single answer sounds good.

## Grade outcomes, not prose
Define each task with a verifiable end state:
- Code agents: automated tests pass (Anthropic notes code solutions are verifiable through automated tests, as in SWE-bench tasks built from real GitHub issues; human review is still needed for broader system fit).
- Ops/tool agents: the database row / ticket / calendar entry has the expected fields (tau-bench compares the database state at the end of a conversation with the annotated goal state).
- Research agents: required facts present with valid sources.
Check state with code where possible; use LLM judges only for parts code can't verify.

## Trajectory metrics
Log every step (tool calls, arguments, results, tokens). Track:
- Tool-call validity (schema errors, wrong tool), repeated identical calls (loops), unnecessary calls.
- Steps, tokens, wall time and cost per task.
- Policy violations (calling a write tool without confirmation, accessing forbidden resources).
A correct outcome with 40 steps and $3 cost may still be a regression.

## Reliability: pass@k vs pass^k
Agents are stochastic. Run each task k times:
- **pass@k:** at least one success in k - optimistic, suits "best of k with a verifier" setups.
- **pass^k:** tau-bench's reliability metric over multiple trials (all k succeed) - closer to what users experience when the same task recurs. tau-bench reports that even gpt-4o-class function-calling agents succeeded on under 50% of tasks and had pass^8 under 25% in the retail domain.
Report success rate with spread across runs, not one run.

## Multi-turn and simulated users
For conversational agents, a user simulator (an LLM) drives the conversation with a domain-specific API tools and policy guidelines on the agent side, and the task succeeds if the final database state matches the annotated goal state (tau-bench pattern). Validate the simulator (it can leak the answer or be unrealistically cooperative) by reading transcripts (practitioner advice).

## Environment hygiene
Anthropic recommends extensive testing of agents in sandboxed environments with appropriate guardrails, since autonomy brings higher costs and compounding errors. Practitioner advice:
- Reset sandboxes (containers, DB snapshots, mock APIs) per run; shared state makes runs dependent.
- Mock external services deterministically; record/replay for third-party APIs.
- Freeze time and random seeds in the environment where possible.

## Read transcripts
Aggregate scores tell you *that* it failed; transcripts tell you *why* (misread tool output, gave up early, ignored instructions). Review a sample of failures after every eval run and bucket them.

## Verify
- [ ] Every task has a programmatic success check on end state.
- [ ] Each task run k >= 3 times; pass^k reported.
- [ ] Cost and steps per successful task tracked alongside success rate.

## Checked
Method: docs-checked 2026-11-09 against the Anthropic Building effective agents post (read via keyword search), and the arXiv abstract pages for tau-bench (2406.12045) and SWE-bench (2310.06770); full papers not read. Dropped: the LangSmith source, the "60% pass^1 gives about 25% pass^4" figure (not supported), and the hidden-tests detail for SWE-bench. The trajectory-metrics and read-transcripts sections are practitioner guidance, not source-backed.
