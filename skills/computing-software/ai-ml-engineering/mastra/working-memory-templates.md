---
id: computing-software.ai-ml-engineering.mastra.working-memory-templates
name: working-memory-templates
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, memory, workingmemory, template, schema, resource-scope, thread-scope, zod]
level: practitioner
status: docs-checked
description: "Configure Mastra working memory: resource vs thread scope, Markdown templates vs zod schemas, merge semantics, seeding values, read-only mode, supported adapters."
sources:
  - https://mastra.ai/docs/memory/working-memory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep persistent, always-available facts about a user or task in a Mastra agent via working memory.

## Enable
```typescript
memory: new Memory({ options: { workingMemory: { enabled: true } } })
```
Working memory is a Markdown block the agent updates over time (via the `updateWorkingMemory` tool). A default template is used if you give none.

## Scope
- `scope: 'resource'` (default): persists across all threads for the same `resourceId`; pass `memory: { thread, resource }` on calls.
- `scope: 'thread'`: isolated per thread.
Switching scope means the agent will not see memory from the other scope. Resource scope needs an adapter supporting the `mastra_resources` table: `@mastra/libsql`, `@mastra/pg`, `@mastra/oracledb`, `@mastra/upstash`, `@mastra/mongodb`.

## Template (Markdown, replace semantics)
```typescript
workingMemory: { enabled: true, scope: 'resource', template: `# User Profile
- **Name**:
- **Location**:
- **Preferences**:
` }
```
The agent must supply the complete memory content on each update. Template design tips from the page: short focused labels, consistent casing, minimal placeholder hints (`[e.g., Formal]`), abbreviate long values, and put update rules in the agent's `instructions`. If the agent is not updating it when expected, add instructions on how and when to use the template.

## Schema (JSON, merge semantics)
Give `schema` (any Standard JSON Schema, e.g. zod) instead of `template`; setting both is not supported.
```typescript
workingMemory: { enabled: true, schema: userProfileSchema }
```
Merge semantics: object fields deep-merge; set a field to `null` to delete it; arrays are replaced entirely.

Concurrency: with `scope: 'resource'` and an atomic-merge adapter (currently `@mastra/pg`), merges run in a row-locked transaction; other adapters only serialize writers inside one process. Merge from code with:
```typescript
await memory.mergeWorkingMemory({ threadId: 'thread-1', resourceId: 'user-123', workingMemory: { preferences: { tone: 'formal' } } })
```
It throws if working memory is not schema-based and resource-scoped, or the adapter lacks atomic merges; check `await memory.supportsAtomicWorkingMemoryMerge()` first.

## Seed or update programmatically
- At thread creation: `memory.createThread({ threadId, resourceId, title, metadata: { workingMemory: '# Patient Profile\n- Name: ...' } })`.
- On an existing thread: `memory.updateThread({ id, title, metadata: { ...thread.metadata, workingMemory: '...' } })`.
- Directly: `memory.updateWorkingMemory({ threadId, resourceId, workingMemory: '...' })` (resourceId required for resource scope).

## Read-only
Pass `memory: { thread, resource, options: { readOnly: true } }` on a call so the agent sees working memory but cannot update it (routing agents, subagents).

## State signals (experimental)
`useStateSignals: true` delivers working memory as a `state` signal (`stateId: 'working-memory'`) instead of in the system message, and the tool is registered as `setWorkingMemory`. Storage is unchanged. Not supported with template working memory `version: 'vnext'`.

## With Observational Memory
`observationalMemory.observation.manageWorkingMemory` lets OM update working memory for the agent.

## Checked
Method: 2026-11-08 read the cited Mastra working-memory page in full (served as markdown) and compared each claim. All claims matched; no content changes.
