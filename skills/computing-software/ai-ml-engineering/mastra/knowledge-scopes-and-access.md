---
id: computing-software.ai-ml-engineering.mastra.knowledge-scopes-and-access
name: knowledge-scopes-and-access
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, knowledge, scopes, access-control, roles, explainaccess, multi-tenant, alpha]
level: advanced
status: docs-checked
description: "Declare Mastra Knowledge scope types and access rules, set per-run scopes from server middleware, limit a single agent, and test roles with explainAccess."
sources:
  - https://mastra.ai/docs/knowledge/scopes-and-access
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control exactly what each agent run can see and change in Mastra Knowledge (alpha; isolation between scopes is not guaranteed, so do not store data that must never reach another customer or user).

## Declare scope types
No built-in types. Each `scopes` key is a pattern; `$name` segments match any value (`team:acme:support` matches `team:$orgId:$teamId`).

```typescript
scopes: {
  ...knowledgeMemoryScopes(),
  'team:$orgId:$teamId': { description: 'A team', belongsTo: 'org:$orgId',
    access: [{ principal: 'self', role: 'editor' }, { principal: 'org:$orgId', role: 'viewer' }] },
  'policy:$orgId': { description: 'Company policies', access: [{ principal: 'org:$orgId', role: 'viewer' }] },
  'audience:$orgId:public': { description: 'Pages for public visitors',
    access: [{ principal: 'self', role: 'viewer' }, { principal: 'org:$orgId', role: 'editor' }] },
}
```
`knowledgeMemoryScopes()` adds `org:`, `resource:` and `thread:`; a run owns its `resource:` and `thread:` scopes and edits its `org:` scope.

## Rules and roles
A rule has a `principal` (`self` = the scope being accessed, or a declared pattern) and a `role`; it applies when the run holds a matching scope. Reusing `$orgId` ties the principal to the same org. Roles are cumulative: viewer (search, read); contributor (create pages, add notes); editor (edit and move within scope, change note visibility, remove notes, pin); owner (move across scopes, merge, delete). `belongsTo` places a scope in the tree but grants no access. Scope declarations reference lists all fields and startup errors.

## Set a run's scopes (server only)
Middleware, with `getUser()` as your own lookup:

```typescript
requestContext.set(MASTRA_SCOPES_KEY, [`org:${user.orgId}`, ...user.teams.map(t => `team:${user.orgId}:${t}`), `resource:${user.id}`])
requestContext.set(MASTRA_RESOURCE_ID_KEY, user.id)
```
Imports from `@mastra/core/request-context`. Also set the resource ID key so thread ownership is checked against the same user. Direct call: `agent.generate(msg, { scopes: ['org:acme', 'team:acme:support'], memory: { resource: 'dana', thread: 'ticket-91' } })`. A run holds one `resource:` and one `thread:` scope; a differing `resource:` scope vs `memory.resource` fails the run. Pass raw IDs. Every run scope must match a declared type or tools fail.

## Narrow one agent
The agent's `scopes` list adds scopes; a function `({ scopes }) => ...` returns the final set, so it can grant less. The public FAQ example maps `org:acme` to `audience:acme:public` and keeps `resource:`/`thread:` scopes (it must return all of them or the run fails).

## How access is computed
Per tool call: start with run scopes, find rules whose principal matches, grant those roles, stop (roles do not chain; scopes do not inherit). Outside the reach, a page looks nonexistent; with a too-weak role the error names the needed role.

Notes are stamped with scopes: a run sees a note if it can read the page and at least one stamp (it need not hold it), and must be able to read the scope of every linked page. A note stamped `resource:dana` is only visible to Dana's runs; one stamped `team:acme:support` is visible to everyone who can read that team scope.

## Test with explainAccess()
```typescript
const roleOn = async (scopes: string[], scope: string) => (await knowledge.explainAccess(scopes, { scope })).role
expect(await roleOn(['org:acme'], 'team:acme:support')).toBe('viewer')
expect(await roleOn(['org:globex'], 'team:acme:support')).toBeNull()
```
Rules binding from a scope's address depend only on declarations; rules via `belongsTo` give no role until a writing run has placed the scope, so test those after a write. Server code only: never expose `explainAccess()` through an agent tool or a route without admin auth.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
