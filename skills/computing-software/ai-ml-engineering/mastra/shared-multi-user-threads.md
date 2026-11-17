---
id: computing-software.ai-ml-engineering.mastra.shared-multi-user-threads
name: shared-multi-user-threads
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, memory, multiuser, participants, resourceid, speaker-tagging, observational-memory, security]
level: advanced
status: docs-checked
description: "Share one Mastra memory thread among many users: shared resourceId, turn-tag speaker identity, picking a memory layer, participants working-memory template, and spoofing risk."
sources:
  - https://mastra.ai/docs/memory/multi-user-threads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let several people talk to one Mastra agent in a single thread while the agent can tell them apart.

## Share one resourceId
A thread belongs to exactly one `resourceId`, so key it on the conversation, not the user: `doc_${docId}` or `room_${roomId}`. Everyone then reads and writes the same history.

## Tag each user message
Wrap each user message in a `<turn>` tag carrying id, name and role so attribution survives into recalled history. The page's helper (adapt to your user shape):

```typescript
export function asUserTurn(speaker: { id: string; name: string; role: string }, text: string) {
  // escapeAttr escapes & " < > in each value
  return { role: 'user' as const,
    content: `<turn author_id="${id}" author_name="${name}" functional_role="${role}">\n${text}\n</turn>` }
}
```
Tell the agent in `instructions` how to read it, for example: address users by `author_name`, respect `functional_role`, attribute past statements from the surrounding `<turn>`, and do not echo `<turn>` tags. Call it with the same thread and resource for everyone:

```typescript
await collabAgent.generate([asUserTurn(alice, 'My favorite color is teal.')], {
  memory: { thread: 'doc_42', resource: 'doc_42' },
})
```

## Pick a memory layer
- Short threads or a verbatim who-said-what record: message history alone (`lastMessages: 20`).
- Long-running threads where per-user facts must outlive `lastMessages` (recommended): Observational Memory, `options: { lastMessages: 20, observationalMemory: true }`. The default Observer reads `<turn>` tags natively. OM needs `@mastra/libsql`, `@mastra/pg`, `@mastra/mongodb`, `@mastra/mysql`, `@mastra/convex` or `@mastra/oracledb`. If a weaker Observer model attributes facts to a generic `User`, use `observation.instruction` to explain the `<turn>` tag.
- No OM support, or a deterministic participants list needed: working memory with `scope: 'thread'` and a template containing `## Participants`, `## Open Questions`, `## Decisions`; instruct the agent to append a participant whenever a new `author_id` appears. The default template assumes one user per thread.

Use OM or working memory, not both; they overlap and add latency and token cost.

## Security
Take the speaker from your authenticated request context (see Request Context), never from the request body. If a client can pick its own `author_id`, one user can impersonate another. Build the `<turn>` tag on the server.

## Related
Memory overview "share memory between agents" and the working-memory template skills.

## Checked
Method: 2026-11-08 read the cited Mastra multi-user-threads page in full (served as markdown) and compared each claim. All claims matched; no content changes.
