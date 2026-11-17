---
id: computing-software.ai-ml-engineering.mastra.studio-auth-rbac
name: studio-auth-rbac
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, studio, auth, rbac, roles, permissions, simpleauth, security]
level: advanced
status: docs-checked
description: "Secure Mastra Studio and API routes with server.auth, pass tokens via auth_header, and apply role-based access control with default roles, permissions and role mapping."
sources:
  - https://mastra.ai/docs/studio/auth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: one `server.auth` config gates both the Studio login screen and all API routes; `server.rbac` controls what each user can do. Without auth, Studio and every API route are public.

Licensing: in production, Studio sign-in with a third-party provider, RBAC and fine-grained authorization need a Mastra Enterprise Edition license; Simple Auth, JWT and API-route auth do not. Everything works without a license in development. On Mastra platform, Studio gets platform auth by default (only org members sign in) and `server.auth` covers API routes only; set `MASTRA_PLATFORM_STUDIO_AUTH=disabled` to opt out.

## Quickstart
```typescript
import { Mastra } from '@mastra/core'
import { SimpleAuth } from '@mastra/core/server'

export const mastra = new Mastra({
  server: {
    auth: new SimpleAuth({
      tokens: { 'my-api-key': { id: 'user-1', name: 'Alice', role: 'admin' } },
    }),
  },
})
```
Studio shows a login screen and all built-in (`/api/agents/*`, `/api/workflows/*`, ...) and custom routes require authentication, from Studio or direct calls. Studio discovers login methods and the user's permissions from `GET /api/auth/capabilities`.

Login UI by provider type: SSO only gives an SSO button; credentials only gives an email/password form; both shows both. Sign-up can be enabled per provider; when disabled Studio hides the link.

## Token via URL
An embedding app can open `https://your-studio-host/?auth_header=Bearer%20your-token`. The value fills the `Authorization` header only (include the scheme prefix, e.g. `Bearer`). Studio reads it once, sends it on every API request in that session, removes it from the address bar (keeping other params and the hash), and keeps it in memory only (not persisted across reloads). URLs can leak via history, referrers and access logs; the host app is responsible.

## RBAC
Default roles from `@mastra/core/auth/ee`: `owner` (`*`), `admin` (read, write, execute, publish, share; no delete), `member` (read, execute), `viewer` (read-only).
```typescript
import { StaticRBACProvider, DEFAULT_ROLES } from '@mastra/core/auth/ee'
server: {
  auth: new SimpleAuth({ tokens: {
    'admin-key': { id: 'user-1', name: 'Alice', role: 'admin' },
    'viewer-key': { id: 'user-2', name: 'Bob', role: 'viewer' },
  } }),
  rbac: new StaticRBACProvider({ roles: DEFAULT_ROLES, getUserRoles: user => [user.role] }),
}
```
Studio hides actions a user lacks permission for (viewers see no delete buttons; members cannot modify agent config).

Permission format `{resource}:{action}` with optional id: `*`, `*:read`, `agents:*`, `agents:execute`, `agents:read:my-id`. Resources include `agents`, `workflows`, `tools`, `datasets`, `memory`, `scores`, `observability`; actions are `read`, `write`, `create`, `delete`, `execute`, `publish`, `share`.

Map identity-provider roles (e.g. Clerk organizations, WorkOS groups):
```typescript
new StaticRBACProvider({
  roleMapping: { 'org:admin': ['*'], 'org:member': ['*:read', '*:execute'], 'org:viewer': ['*:read'] },
  getUserRoles: user => user.providerRoles,
})
```

## Checked
Method: 2026-11-08 read the Mastra Studio auth docs page in full (served as markdown). Licensing notes, quickstart, capabilities endpoint, auth_header handling, default roles, permission format, roleMapping and login-method claims all match the page; no claims changed or removed.
