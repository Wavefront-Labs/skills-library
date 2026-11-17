---
id: computing-software.ai-ml-engineering.mastra.context-engineering-layers
name: context-engineering-layers
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, context, compaction, instructions, memory, rag, processors, signals]
level: advanced
status: docs-checked
description: "Decide what a Mastra agent sees: instructions, inline context, tools, RAG, workspace files, memory, observational memory, signals, plus processors and subagent filters."
sources:
  - https://mastra.ai/docs/guides/context-engineering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep model context relevant and current. Too little leaves gaps; too much raises cost and buries details well before the context limit.

## Pick the mechanism
| Need | Use | Model sees |
| - | - | - |
| Stable identity, rules | `instructions` | System context each call |
| Data from a DB/API | Tools | Tool definitions then selected results |
| Current app data | Inline context | Data interpolated into the user message |
| Large stable knowledge base | RAG | Relevant chunks from an index |
| User/org documents | Workspace filesystem | Files via read/search tools |
| Recent conversation, facts | Memory | History, observations or retrieved memories |
| Long conversation | Observational Memory | Dense observations plus recent unobserved messages |
| Events/state during a run | Signals | User, reactive, notification or state messages |
| Task-only instructions | Skills | Metadata, then instructions on demand |

## Instructions
System messages placed before conversation messages. Keep them to behaviour that applies to most calls. Make them dynamic with `instructions: ({ requestContext }) => ...` for per-request data (user, tenant, locale, role, flags). Anything evaluated at construction, including an interpolated `new Date()`, is fixed for the life of the process: compute dates inside a callback and pass an explicit `timeZone`. If the date must refresh across tool continuations or coexist with Studio overrides, use a `processInputStep` processor. Frequently changing instructions defeat provider prompt caching: keep the stable part first and pass changing background through messages or signals.

## Inline context
Interpolate only the labelled fields the model needs into the message. With memory enabled the user message is saved, so do not interpolate sensitive or temporary data. To affect one response without saving it, pass `context`:
```typescript
await supportAgent.generate('Recommend the next action.', {
  context: [{ role: 'user', content: 'The customer has an unresolved billing dispute.' }],
})
```

## Tools and RAG
Tools are the recommended way to fetch current data; the model supplies arguments, your code controls the query and returned fields. Use `toModelOutput` when the app needs the full result but the model needs a smaller one. For RAG, `createVectorQueryTool({ vectorStoreName, indexName, model: new ModelRouterEmbeddingModel('openai/text-embedding-3-small') })` from `@mastra/rag`; register the vector store on the same Mastra instance. Direct source-specific tools are often simpler and cheaper; choose RAG when semantic search over unstructured content is the real requirement, then limit with metadata filters, reranking and a conservative `topK`.

## Filesystem
A `Workspace` with `new LocalFilesystem({ basePath })`, `bm25: true`, `autoIndexPaths: ['**/*.md']` gives agents tools such as `mastra_workspace_read_file`, `mastra_workspace_list_files`, `mastra_workspace_grep`, `mastra_workspace_search`, `mastra_workspace_index`; call `await workspace.init()`. Changed files must be indexed before search returns their latest contents. Choose it when the source of truth is files the agent may list, read or update; choose standalone RAG when retrieval is the main need.

## Memory and Observational Memory
Memory needs a storage provider, and each call names a `resource` and `thread`: `generate(msg, { memory: { resource: 'user-123', thread: 'project-456' } })`. `new Memory({ options: { lastMessages: 20 } })` (default 10). A sliding window drops the oldest message each turn past the limit, invalidating the provider prompt cache. For long conversations Mastra recommends `new Memory({ options: { observationalMemory: true } })`: an Observer turns older messages and tool interactions into dense observations, reflection compresses them, no `lastMessages` needed. Observations are added in stable chunks to help prefix reuse; async buffered observations do not generate continuation hints (`currentTask`, `suggestedResponse`).

## Signals
Add context to a memory-backed thread: `sendMessage()` (active agent sees it now), `queueMessage()` (next turn), `sendSignal()` (background results, reminders, events), `sendStateSignal()` (changing state, kept as snapshots and deltas). State signals need memory and an existing thread; notification inbox signals need a storage adapter with notification support. Example: `agent.sendSignal({ type: 'notification', contents: '...', attributes: {...} }, { resourceId, threadId })` then `await result.accepted`. A processor can send a reactive signal in `processInputStep()`; set `transient: true` for the current model call only. Use `computeStateSignal()` when a processor owns the state.

## Controlling growth
- Compaction (summarize at a token threshold) is called a blunt fallback; Mastra does not provide it out of the box (build with a custom processor). Prefer Observational Memory.
- Processors: `ToolCallFilter` removes old tool calls/results from model input but keeps them in storage and UI; `ToolSearchProcessor` replaces a large tool catalog with search/load tools; `TokenLimiter` prunes non-system messages to a token budget. Start with `toModelOutput` for verbose results and `ToolCallFilter` for old tool use; add `TokenLimiter` as a final guard. `processInput`/`processInputStep` edits may be saved to memory; `processLLMRequest` edits apply to one provider call only.
- Subagents: the parent's conversation is forwarded by default; narrow it with `delegation: { messageFilter: ({ messages }) => messages.slice(-10) }`. By default only the subagent's text returns to the parent; keep `includeSubAgentToolResultsInModelContext` disabled unless the parent must reason over those details. `onDelegationStart` refines the child prompt; `onDelegationComplete` trims what returns.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
