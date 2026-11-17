---
id: computing-software.ai-ml-engineering.mastra.choose-multi-agent-pattern
name: choose-multi-agent-pattern
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, handoff, supervisor, council, multi-agent, workflows, subagents]
level: practitioner
status: docs-checked
description: "Pick a Mastra multi-agent pattern (handoff, workflow, supervisor, council) by who stays in control, and map each to its Mastra implementation."
sources:
  - https://mastra.ai/docs/guides/multi-agent-systems
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose the coordination pattern for a multi-agent Mastra system based on which component stays in control.

## When to go multi-agent
Start with one agent. Add agents when the structure clearly improves quality, speed or reliability, for example: the task spans different kinds of work (research, planning, writing, review), one agent would need too much context or too many tools, parts can run in parallel, stages need different prompts/models/guardrails, or you want clear boundaries between routing, execution and synthesis.

## The four patterns
| Pattern | Who stays in control | Use when | Tradeoff | Mastra implementation |
| - | - | - | - | - |
| Handoffs | Current specialist | Ownership should move between specialists | Context transfer matters more | Agents with workflows and memory |
| Workflows | Execution graph | The path is known in advance | Less adaptive when the task changes | Workflows |
| Supervisor | One lead agent | Delegation must adapt during execution | Depends on good delegation and clear boundaries | Supervisor agents (subagents) |
| Council | Final synthesis step | Needs multiple independent perspectives | Higher cost and latency | Agents plus workflow parallelism |

- Handoff: the first agent does not stay in charge; the active specialist owns the next part of the interaction. Decide what the next agent inherits and what stays scoped. A workflow can route, but the defining feature is that ownership moves.
- Workflow: control logic lives in steps, branches, loops and parallel blocks, so it is predictable and easy to debug and audit. Workflows can themselves implement handoffs and councils.
- Supervisor: a lead agent decides when to delegate, which specialist, what context to pass and how to combine results. Define subagents through the `agents` property and coordinate with `stream()` or `generate()`. Mastra offers delegation hooks, message filtering and memory isolation between agents.
- Council: several agents work the same problem independently, then a synthesis or review step compares outputs. Best for ambiguous, evaluative or high-stakes questions. Mastra has no dedicated council primitive: run agents in parallel (workflow `.parallel()`) and add a final synthesis step.

## Combining
A workflow can contain supervisor-driven steps; a handoff flow can start with a routing workflow; a council can run inside a workflow and feed an approval step; a supervisor can delegate to a workflow for a fixed-structure task.

Choose by the coordination problem, not the task label.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
