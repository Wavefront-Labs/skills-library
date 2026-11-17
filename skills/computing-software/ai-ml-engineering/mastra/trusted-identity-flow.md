---
id: computing-software.ai-ml-engineering.mastra.trusted-identity-flow
name: trusted-identity-flow
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, identity, oauth, auth, requestcontext, mapusertoresourceid, credentials, multi-tenant]
level: sme
status: docs-checked
description: "Design a trusted identity chain in Mastra: server.auth, mapUserToResourceId, ownership checks in tools, tenant credentials, MCP auth info and a pre-production checklist."
sources:
  - https://mastra.ai/docs/guides/authentication-identity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: carry a verified caller identity through agents, tools and outbound calls so the model cannot choose whose data it touches.

## Stages
| Stage | Mechanism |
| - | - |
| Authentication | `server.auth` |
| Identity propagation | `RequestContext` |
| Authorization | app checks, `server.rbac`, or `server.fga` |
| Outbound auth | trusted tool code or MCP connection config |

Boundaries: treat request data as untrusted until auth succeeds; the server owns reserved identity values; model-controlled tool input must not select ownership scope; credentials stay in trusted code.

## Establish identity
```typescript
server: {
  auth: {
    authenticateToken: async token => verifyAccessToken(token),
    mapUserToResourceId: (user: AuthUser) => `${user.workspaceId}:${user.id}`,
  },
}
```
- Use a canonical provider identifier (not mutable display names) and scope it enough to avoid cross-tenant collisions.
- Mastra routes are public when `server.auth` is not configured. If you set a custom `server.apiPrefix`, update the auth path config.
- Public custom routes need `requiresAuth: false`; public webhooks must still verify the provider signature.
- If `mapUserToResourceId` is missing, any authenticated caller can use any resource ID via `memory.resource`; Mastra logs a startup warning. Always set it when users share a deployment.
- Pick the boundary: `user.id` (private), `user.organizationId` (shared), or `${workspaceId}:${projectId}:${userId}`.

## Enforce at the data boundary
In a tool, read `requestContext.get('user')` from the `execute` second argument, throw if missing, and query with `ownerId: user.id`. The model may pick `status` but never `ownerId`. Same rule for custom routes and workflow steps. Personalising instructions or tool lists is not authorization.

## Outbound credentials
Forward a token only when the receiving service is meant to trust it. For multi-tenant services resolve a tenant credential in trusted tool code (e.g. `tenantCredentials.getBillingToken(user.organizationId)`), failing closed and returning least-privilege credentials. For external MCP servers that accept the caller's token read it from `MASTRA_AUTH_TOKEN_KEY`; an MCP server must not forward the MCP token it received to another API.

## MCP tools
Behind `server.auth` an `MCPServer` puts the caller in `authInfo`; tools read `mcp?.extra.authInfo?.extra?.user`. Mastra keeps any `req.auth` set by middleware, else uses `server.mcpOptions.setRequestAuth`. `MCPServer.mapAuthInfoToUser` maps back for FGA.

## Secrets
Keep tokens and tenant keys out of prompts and tool results. Keys starting `mastra__` or `__mastra_` are omitted from tracing spans and score records.

## Before production
Missing credentials return `401`; known user without permission returns `403`. Verify: anonymous requests rejected; invalid credentials leave no trusted context; webhook signatures checked; user A cannot read user B's thread; tool input cannot replace server-owned identity; secrets absent from model-facing and observability data; direct tests pass trusted `RequestContext` explicitly.

## Checked

Method: 2026-11-08 read the raw MDX of the Mastra Authentication and identity guide in full and compared each claim in the skill (stages, server.auth and mapUserToResourceId behaviour, tool ownership checks, outbound credentials, MCP authInfo bridge, reserved key redaction, 401/403 and the pre-production checklist); all are supported and unchanged.
