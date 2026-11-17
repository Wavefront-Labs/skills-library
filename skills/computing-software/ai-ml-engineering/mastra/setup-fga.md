---
id: computing-software.ai-ml-engineering.mastra.setup-fga
name: setup-fga
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, fga, authorization, resourcemapping, permissionmapping, workos, multi-tenant, actor]
level: sme
status: docs-checked
description: "Configure Mastra fine-grained authorization: resource and permission mapping, stored-resource scoping, route policies, enforcement points and system actors."
sources:
  - https://mastra.ai/docs/auth/fga
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enforce "can this user do this on this specific resource" in a multi-tenant Mastra app. FGA needs a Mastra Enterprise Edition licence in production (works unlicensed in development).

## Configure (`server.fga`)
```typescript
server: {
  auth: new MastraAuthWorkos({ fetchMemberships: true, mapUserToResourceId: user => user.teamId }),
  fga: new MastraFGAWorkos({
    resourceMapping: {
      agent: { fgaResourceType: 'team', deriveId: ctx => ctx.user.teamId },
      thread: { fgaResourceType: 'workspace-thread', deriveId: ({ resourceId }) => resourceId },
    },
    permissionMapping: { [MastraFGAPermissions.AGENTS_EXECUTE]: 'manage-workflows' },
  }),
  storedResources: { scope: true },
}
```
(`MastraFGAPermissions` from `@mastra/core/auth/ee`.) `MastraFGAWorkos` needs `fetchMemberships: true`. Use `thread` (not legacy `memory`) as the key for memory authorization.

With `server.fga` set, protected actions are enforced and an action with no authenticated user is denied; without it checks are skipped.

- `deriveId` receives `user`, `resourceId` (owning Mastra resource, e.g. a thread's) and `requestContext`; return `undefined` to fall back to the original ID.
- `permissionMapping` translates Mastra permissions to provider slugs; unmapped strings pass through. `validatePermissions()` checks the full set at startup.

## Stored resources
FGA does not filter shared-storage records. `storedResources: { scope: true }` reads `MASTRA_RESOURCE_ID_KEY` (set by `mapUserToResourceId`) and filters list/read/update/publish/delete. Object form: `{ metadataKey, resolve: ({ user }) => ..., requireScope }`; with `requireScope` true or omitted, routes fail when no scope resolves.

## Route policy
Route is checked if it has route-level `fga` metadata, built-in metadata, or `resolveRouteFGA()` supplies it. Provider options: `requireForProtectedRoutes: true` denies unresolved protected routes; `auditProtectedRoutes: 'warn' | 'error'` (`error` fails startup). Prefer `createRoute({ ..., requiresAuth: true, fga: { resourceType, resourceIdParam, permission } })` from `@mastra/server/server-adapter`.

## Enforcement points
Agent `generate`/`stream` (`agents:execute`), workflow HTTP routes and `Workflow.execute()` (`workflows:execute`), tool execution (`tools:execute`; agent tools use `${agentId}:${toolName}`), thread/memory (`memory:read|write|delete`), stored resource routes. Direct `createRun().start()`, `resume()`, `restart()` are not independently checked; call them from a protected route or guard in code. For OAuth MCP servers configure `mapAuthInfoToUser`.

## Custom provider and system actors
Implement `IFGAProvider`: `check`, `require` (throw `FGADeniedError`), `filterAccessible`. For autonomous or scheduled agents pass `actor: true` or `{ actorKind: 'system', agentId?, permissions?, scope?, propagate? }`; a trusted actor skips `require()` after a tenant-scope check unless you implement `requireActor`. Rules: construct actors server-side only (built-in agent routes strip `actor`); pass it again on every resume; an `organizationId` must be set server-side; treat `actor.permissions` as an unverified claim and resolve real grants by `agentId`. `propagate: true` (object form only) forwards the actor to declarative `.then(agent)`/`.then(tool)` steps, never to custom `execute` functions; per-step override via `createStep(agent, { actor: undefined })`.

## Checked
Method: 2026-11-08 read the Mastra FGA docs page in full (served as markdown). Config, resource and permission mapping, stored-resource scoping, route policy, enforcement points, custom provider, system-actor and propagation trust rules all match the page; no content changed.
