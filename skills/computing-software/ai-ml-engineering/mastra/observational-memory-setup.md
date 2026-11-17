---
id: computing-software.ai-ml-engineering.mastra.observational-memory-setup
name: observational-memory-setup
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, memory, observationalmemory, reflection, observer, async-buffering, extractors, retrieval]
level: advanced
status: docs-checked
description: "Set up and tune Mastra Observational Memory: thresholds, async buffering, idle activation, retries, extractors, retrieval recall tool, models, hooks and scopes."
sources:
  - https://mastra.ai/docs/memory/observational-memory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: compress long Mastra agent conversations into an observation log with background Observer and Reflector agents, and tune it.

## Enable
`npm install @mastra/memory@latest @mastra/libsql@latest`, then `memory: new Memory({ options: { observationalMemory: true } })`. A storage provider is required (on `Mastra` or the Agent). Supported adapters: `@mastra/pg`, `@mastra/libsql`, `@mastra/mysql`, `@mastra/mongodb`, `@mastra/convex`, `@mastra/oracledb`. Default model is `'auto'`; pass `{ model: '<provider/model>' }` to pin one. From a client app send only the new message; set `retainFullInput: true` in `memory.options` only if you need input processed exactly as sent.

## How it works
- Observer: when message-history tokens exceed `observation.messageTokens` (default 30,000), it writes dense observations (typically 5x to 40x compression).
- Reflector: when observations exceed `reflection.observationTokens` (default 40,000) it rewrites the whole log, condensing older material harder. Memory stays bounded.
- Default cycle: buffer roughly every 6k tokens (`bufferTokens: 0.2`); at 30k buffered chunks activate and about 6k of recent history remains (`bufferActivation: 0.8`).

## Settings (async buffering is on by default)
| Setting | Default | Meaning |
| - | - | - |
| `observation.bufferTokens` | 0.2 | buffer every 20% of `messageTokens`, or an absolute count; `false` disables async buffering for both stages |
| `observation.bufferActivation` | 0.8 | fraction cleared on activation |
| `observation.blockAfter` | 1.2 | synchronous observation fallback (values below 100 multiply `messageTokens`; 100 or more are absolute and must exceed `messageTokens`) |
| `reflection.bufferActivation` | 0.5 | start background reflection at 50% of `observationTokens` |
| `reflection.blockAfter` | 1.2 | synchronous reflection fallback |
| `activateAfterIdle` | none | activate buffered observations after idle: ms, `"5m"`, `"auto"`, or `{ default: 'auto', anthropic: '1h' }` |
| `activateOnProviderChange` | false | activate when the next step uses a different provider/model |

Reflections do not inherit top-level idle or provider-change settings; set them under `reflection`. `"auto"` cannot see per-message cache TTLs (e.g. Anthropic `cacheControl` ttl `1h`), so use the per-provider object and keep it in sync by hand. `observation.bufferOnIdle: true` buffers at end of turn. `shareTokenBudget` pools budgets and currently requires `bufferTokens: false`. `observation.previousObserverTokens` (number, `0` to omit, `false` default) limits previous observations sent to the Observer.

## Retries and failure policy
Per stage: `observation: { maxRetries: 8, failurePolicy: 'continue' }` (and `reflection`). Defaults: `maxRetries` 8, `failurePolicy` `'abort'`. With `'continue'`, failed input stays pending and the turn proceeds, but a sustained outage moves the failure to the main model's context limit. Background buffering failures never stop the turn (reported as `om_buffering_failed`).

## Extractors
```typescript
observation: { extract: [new Extractor({ name: 'User profile', instructions: '...', schema: z.object({ timezone: z.string().optional() }) })] }
```
`Extractor` is from `@mastra/memory`. With a `schema` it runs as a follow-up structured request; without it, an inline string extractor. `includePreviousExtraction: false` hides the last value. `onExtracted` can normalize values. Read results from the stream chunks `data-om-observation-end` and `data-om-buffering-end` (`extractedValues`, `extractionFailures`). `observation.manageWorkingMemory: true` lets the Observer maintain working memory. `observation.observeAttachments` accepts `false`, a mimeType glob array or `'auto'`.

## Retrieval mode
`retrieval: true` registers a `recall` tool for browsing raw messages across the resource's threads; `retrieval: { vector: true }` adds semantic search over observation groups (needs vector store and embedder on `Memory`); `scope: 'thread'` restricts to the current thread; `instructions` appends custom guidance.

## Models
`autoModels` changes the per-provider pick, `resolveModel` builds the model with your routing. `ModelByInputTokens({ upTo: { 5_000: '...', 20_000: '...' } })` selects by input size (inclusive bounds; throws if input exceeds the largest). Use a 128K+ context, fast model. Use separate `observation.model` and `reflection.model` if one condenses poorly.

## Scope
Thread scope is the default and needs a `threadId` or it throws. `scope: 'resource'` is deprecated; use `retrieval` plus resource-scoped working memory for cross-thread continuity (switching does not migrate old observations).

## Hooks
`hooks`: lifecycle (`onObservationStart/End`, `onReflectionStart/End`) and transform (`beforeObservation`, `afterObservation`, `beforeReflection`, `afterReflection`). `skillResultRedactor()` from `@mastra/memory/hooks` strips skill tool results before observation. After hooks are not a redaction boundary for extractor results.

## Misc
Temporal gap markers: `temporalMarkers: true` (inserted at gaps of 10 minutes or more). Studio's agent Memory tab shows token progress and observations.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
