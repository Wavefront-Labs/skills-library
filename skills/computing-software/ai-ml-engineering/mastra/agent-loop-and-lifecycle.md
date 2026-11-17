---
id: computing-software.ai-ml-engineering.mastra.agent-loop-and-lifecycle
name: agent-loop-and-lifecycle
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, lifecycle, loop, requestcontext, processors, durable-agents, stopwhen, maxsteps]
level: sme
status: docs-checked
description: "Follow a Mastra agent run: preparation, loop iterations and model steps, processor hook order, stop conditions, finalization, retries, and regular vs durable runs."
sources:
  - https://mastra.ai/docs/guides/agent-lifecycle
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: reason correctly about what happens in a `generate()` / `stream()` call, where each processor hook runs, and where `RequestContext` values must be set.

## Levels
- Run: everything from one `generate()`/`stream()` call to the final result or error (including pause/resume for durable runs).
- Loop iteration: one pass starting with a model step plus any requested tool work.
- Model step: one provider request/response with the input/output processors around it. An iteration commonly equals one model step, but the page calls that implementation behaviour, not a stable contract.

## Phases
1. Preparation: validate `RequestContext`; resolve model, instructions, workspace, skills and other dynamic config; build the message list from input and memory; prepare tools and processors. These do not happen in one strict sequence.
2. Loop: model call, then tools if requested, then maybe another iteration.
3. Finalization.

## RequestContext boundary
A value only affects work that has not happened yet.
- `generate()`/`stream()` validate `RequestContext` before calling `getDefaultOptions()`, so a function-based default cannot supply a missing required value.
- Values needed by validation, model, instructions, skills, workspace, input processors used by `processInput`, or dynamic tools: set before the call (usually server middleware or caller code).
- Values for later processor factories/hooks or tool execution: before the call when practical, or in `processInput`.
- Resumed durable work: set at the trusted request/resume boundary.
- Model reasoning: put it in instructions or messages; `RequestContext` is not added to the prompt.
- Do access checks outside the agent; the context carries the result and does not replace authorization. Use one context per independent request.

## Hook order around each model step
`processInputStep` -> `processLLMRequest` (provider-facing prompt) -> provider stream with `processOutputStream` per chunk -> `processLLMResponse` -> `processOutputStep` (before local tools) -> tool input processing, approval, execution -> `processToolResult` (before the raw result enters messages). A deferred provider-executed result that arrives in a later stream runs `processToolResult` when it arrives.

What persists:
- `processInput` / `processInputStep` change the live message list; changes may be saved by memory processors.
- `processLLMRequest` changes only that provider call (use for temporary rewrites).
- `processOutputStream` changes streamed chunks.
- `processToolResult` allows validation or redaction before later steps or persistence.
- `processOutputResult` (finalization) can change returned messages and metadata.

## When the loop stops
A final response with no tool request; a `stopWhen` condition; the `maxSteps` limit; task-completion, goal or subagent delegation outcomes; a terminal finish reason, error, processor tripwire or abort. Treat `maxSteps` as a bound on model steps and use `stopWhen` for application-specific completion rules.

## Finalization
`processOutputResult` runs once per request on the completed result, even if the provider throws. Configured output processors run first, then auto-attached memory output processors. Messages may lack a final assistant reply (for example when `maxSteps` ends on a tool call).

## Errors, retries, aborts
- `processAPIError` may change the request or messages and request another provider attempt. Its retries and tripwire retries share the `maxProcessorRetries` bound. With error processors configured and `maxProcessorRetries` omitted, Mastra applies a default budget; set it explicitly for a specific limit.
- `abort()` from an input/output processor raises a tripwire; `retry: true` lets an eligible check replay the model step with feedback. A tripwire without retry stops normal execution and appears in the result or stream.
- An external abort signal stops loop execution and ends the stream, keeping the partial result where supported.

## Regular vs durable
A regular run lives in the current process. A durable agent wraps the same loop in a workflow, persists run state and publishes events through PubSub; persistent production backends are needed for state to survive restarts. Durable runs can suspend (for example a tool awaiting approval) and resume.
- Only serializable `RequestContext` entries are snapshotted. Rebuild functions, class instances and connections from stable identifiers at the resume boundary.
- Initial `processInput` is skipped when a durable run resumes from a stored snapshot (wakes that start a fresh segment, including signal and schedule wakes, run it again). So repeat authoritative enrichment on resume, store only serializable scope, and do not rely on a one-time `processInput` side effect.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
