---
id: computing-software.ai-ml-engineering.mastra.delegate-to-subagents
name: delegate-to-subagents
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, subagent, delegation, supervisor, agent, messagefilter, memory, ondelegationstart]
level: practitioner
status: docs-checked
description: "Delegate work from a Mastra supervisor agent to subagents: agents config, delegation hooks, message filtering, result context, memory isolation, iteration limits."
sources:
  - https://mastra.ai/docs/subagents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build a parent (supervisor) agent that delegates to specialist agents. Added in `@mastra/core@1.8.0`.

## Quickstart
Subagents need a clear `description`; add them to the parent's `agents`. The parent uses its instructions and each description to decide delegation.
```typescript
const researchAgent = new Agent({ id: 'research-agent', description: 'Gathers factual information and returns bullet-point summaries.', model: 'openai/<model>' })
const writingAgent = new Agent({ id: 'writing-agent', description: 'Transforms research into well-structured articles.', model: 'openai/<model>' })

const parentAgent = new Agent({
  id: 'parent-agent',
  instructions: 'Delegate to research-agent for facts, then writing-agent for content.',
  model: 'openai/<model>',
  agents: { researchAgent, writingAgent },
  memory: new Memory({ storage: new LibSQLStore({ id: 'storage', url: 'file:mastra.db' }) }),
})
const stream = await parentAgent.stream('Research AI in education and write an article', { maxSteps: 10 })
```
Good parent instructions list the available resources, delegation strategy and success criteria.

## Delegation hooks
Set under the `delegation` option, per call or in `defaultOptions`.
- `onDelegationStart(context)`: context has `primitiveId`, `prompt`, `iteration`, `requestContext`. Return `proceed` (false plus `rejectionReason` rejects), `modifiedPrompt`, `modifiedMaxSteps`, `threadMetadata`. The model-supplied `maxSteps` is capped at the subagent's `defaultOptions.maxSteps`; `modifiedMaxSteps` replaces the capped value and can raise it.
- `onDelegationComplete(context)`: has `primitiveId`, `result`, `success`, `error`, `messages`, `bail()`. `bail()` stops the parent loop. Return `{ feedback }` (saved to parent memory for the next turn) or `{ resultText }` (replaces the tool result text the parent sees now; a failed delegation still counts as failed). Prefer a curated message over forwarding `error.message`.
- A throwing hook does not stop delegation by default; `hookErrorStrategy: 'throw'` fails it instead. Failures are recorded under `__mastra_delegationHookErrors` on the request context.
- Values set with `context.requestContext.set(...)` in `onDelegationStart` reach the subagent; changes made inside the subagent do not affect the parent.

## Message filtering
Subagents get the full parent conversation by default. Narrow it:
```typescript
delegation: {
  messageFilter: ({ messages, primitiveId, prompt }) =>
    messages.filter(m => !JSON.stringify(m.content).includes('confidential')).slice(-10),
}
```

## Result context
The parent's model sees only the subagent's text, not nested tool calls or thread/resource IDs (app code can still read `subAgentToolResults` in the payload). `includeSubAgentToolResultsInModelContext: true` includes the full result. `enableResultReferences: true` gives results ids like `explorer-1` and adds a `contextFromRefs` input so later delegations reuse earlier text verbatim (held in memory for one run only).

Subagents cannot run client tools (tools without `execute`): the run stops with `finishReason: 'tool-calls'` and `subAgentPendingToolCalls` lists them. Give client tools to the parent, or use `suspend()` in the subagent's tool.

## Memory isolation
The subagent receives the full context, but only its delegation prompt and response are saved to its memory, on a fresh thread per invocation.

## Other controls
- `onIterationComplete(context)` on the parent call returns `{ continue, feedback }` to steer or stop the loop.
- An `abortSignal` passed to the parent is forwarded to subagents.
- `isTaskComplete: { scorers: [...], strategy: 'all' }` keeps iterating until scorers pass; `createRubricScorer({ model, criteria: [{ description }] })` comes from `@mastra/evals/scorers/prebuilt`.
- Tool approvals and `suspend()` in subagents surface on the parent stream.
- Background: enable the backgroundTasks manager on the Mastra instance, set `backgroundTasks: { tools: { researchAgent: { enabled: true, timeoutMs: 900_000 } } }` on the parent, and call `parentAgent.streamUntilIdle(...)` instead of `stream()`.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
