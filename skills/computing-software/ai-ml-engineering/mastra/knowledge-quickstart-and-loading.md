---
id: computing-software.ai-ml-engineering.mastra.knowledge-quickstart-and-loading
name: knowledge-quickstart-and-loading
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, knowledge, scopes, pinned, upsertpage, addnote, seeding, alpha]
level: practitioner
status: docs-checked
description: "Set up Mastra Knowledge (alpha): Knowledge instance, scopes, tools: true, Studio routes, then seed pages and notes from server code with upsertPage and addNote."
sources:
  - https://mastra.ai/docs/knowledge/overview
  - https://mastra.ai/docs/knowledge/load-your-content
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: give agents a shared graph of pages and notes that outlives conversations, and preload your own content.

Alpha caveats (page): API may change, added in `@mastra/core@1.82.0`; isolation between scopes is not guaranteed, so never store what must not reach another customer; no built-in importers or retention yet.

## Concepts
Page (name, description, markdown body; nests like folders, e.g. `org:acme#policies/refund`), note (short attributed fact on a page), link (`[[org:acme#policies/refund]]`), scope (e.g. `org:acme`; you declare kinds, your server decides which a run holds), role (viewer, contributor, editor, owner, from rules, computed per tool call). Memory holds conversation state; Knowledge holds cross-thread, cross-agent information.

## Quickstart
```typescript
const storage = new LibSQLStore({ id: 'storage', url: 'file:./mastra.db' })
export const knowledge = new Knowledge({ id: 'company', storage, scopes: { ...knowledgeMemoryScopes() }, tools: true })
export const agent = new Agent({ id: 'assistant', name: 'Assistant', instructions: '...', model: 'provider/model', memory: new Memory({ storage }), knowledge })
export const mastra = new Mastra({
  agents: { agent },
  knowledge: { company: knowledge },
  server: { apiRoutes: [...KNOWLEDGE_ROUTES] },
})
```
Imports: `Knowledge`, `knowledgeMemoryScopes` from `@mastra/core/knowledge`; `KNOWLEDGE_ROUTES` from `@mastra/server/server-adapter`. `tools` is off by default, so no tools without `tools: true`. Memory is optional if each call passes `scopes`, but pinned context needs Memory. `knowledgeMemoryScopes()` declares `org:`, `resource:` and `thread:` scopes. Run with scopes:

```typescript
await agent.generate('Our refund window is 30 days. Save that for the team.', {
  scopes: ['org:acme', 'resource:dana', 'thread:dana-1'],
})
```
The agent writes with `knowledge_page`, searches with `knowledge_search`, reads with `knowledge_read`. Search returns only pages the run can read. Scopes must come from server code, never the model or request body. Browse in Studio under Knowledge (`mastra dev`).

## Load content
Declare a scope for the content, readable but not editable by the org:

```typescript
'docs:$orgId': { description: 'Product docs', belongsTo: 'org:$orgId', access: [{ principal: 'org:$orgId', role: 'viewer' }] }
```
Seed from server code. A path like `guides/install` becomes `docs:acme#guides/install`, creating missing parents:

```typescript
await knowledge.upsertPage({ scope: `docs:${orgId}`, path: doc.slug, name: doc.title, body: doc.markdown, author: 'seed:docs' })
await knowledge.addNote({ scope: 'docs:acme', path: 'guides/install', text: 'Node 18 support ends on [[docs:acme#releases/2026-12]].', when: new Date('2026-11-01'), author: 'seed:docs' })
```
If `vector` and `embedder` are set, `upsertPage()` also embeds pages for search by meaning.

## Gotchas stated on the pages
- These methods skip run scopes and access rules: use only in trusted server code, never from an agent tool or an unauthenticated-admin route.
- Re-running a seed: `upsertPage()` skips unchanged pages; `addNote()` adds a duplicate each call (use `updateNote()` to change one).
- Documents deleted at the source stay; remove with `removePage()` (a page with children cannot be removed until they are).

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
