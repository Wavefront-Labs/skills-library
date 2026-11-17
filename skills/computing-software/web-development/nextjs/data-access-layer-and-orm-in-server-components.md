---
id: computing-software.web-development.nextjs.data-access-layer-and-orm-in-server-components
name: data-access-layer-and-orm-in-server-components
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, data-access-layer, dto, prisma, drizzle, react-cache, server-components, authorization, web-development]
level: practitioner
status: docs-checked
description: "Building a Next.js data access layer: server-only modules, auth checks next to queries, DTOs, React cache() dedupe, and ORM client setup in dev and serverless."
sources:
  - https://nextjs.org/blog/security-nextjs-server-components-actions
  - https://nextjs.org/docs/app/guides/authentication#creating-a-data-access-layer-dal
  - https://react.dev/reference/react/cache
  - https://www.prisma.io/docs/orm/more/help-and-troubleshooting/nextjs-help
  - https://nextjs.org/docs/app/guides/data-security
  - https://nextjs.org/docs/app/api-reference/directives/use-cache
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data access layer and ORM use in server components

**Goal:** components never query the database directly; one layer authorises, queries and shapes data.

## 1. Why a DAL
Server components and actions make it easy to `await db.user.findMany()` anywhere - and to pass whole rows (password hashes, internal flags) to client props. Centralising data access gives one place for auth checks and output filtering.

## 2. Structure
```ts
// lib/dal.ts
import "server-only";
import { cache } from "react";
import { cookies } from "next/headers";

export const verifySession = cache(async () => {
  const token = (await cookies()).get("session")?.value;
  const session = await decrypt(token);
  if (!session?.userId) redirect("/login");
  return { userId: session.userId, role: session.role };
});

export async function getInvoice(id: string) {
  const { userId } = await verifySession();
  const inv = await db.invoice.findFirst({ where: { id, ownerId: userId } });   // authorise in the query
  if (!inv) return null;
  return { id: inv.id, total: inv.total, status: inv.status };                 // DTO, not the row
}
```
`cache()` deduplicates within one request: many components calling `verifySession()` hit the DB once.

## 3. ORM client setup
Dev hot reload creates new clients and exhausts DB connections. Singleton:
```ts
import "server-only";
const g = globalThis as unknown as { prisma?: PrismaClient };
export const db = g.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== "production") g.prisma = db;
```
Serverless: use a connection pooler or serverless-capable driver recommended by your database and ORM vendor. Prisma 7 builds the client with a driver adapter (`new PrismaClient({ adapter })`, see Prisma's Next.js guide); the `globalThis` singleton is unchanged.

## 4. Mutations
Server actions call DAL functions, never raw ORM in the action body. Each action re-checks auth (actions are public endpoints) and validates input with zod.

## 5. Avoid N+1 in component trees
Components each fetching per item cause N queries. Fetch lists with relations in one DAL call (`include`/joins) or batch with DataLoader-style `cache()` per id.

## 6. Caching
`"use cache"` with `cacheTag` needs `cacheComponents: true` (Next 16) and replaces `unstable_cache`; use either only for data that isn't per-user, or include the user id in arguments.

## Verify
- [ ] `grep -rn "prisma\.\|db\." app/` - no direct ORM calls in components/actions.
- [ ] Requesting another user's id via URL returns 404/null.
- [ ] Client props contain no sensitive fields (inspect RSC payload in Network tab).

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (guides/data-security, use-cache, unstable_cache), Prisma docs source (prisma/docs main, commit of 2026-10-25: Next.js troubleshooting and v7 Next.js guide).
Confirmed: DAL recommended for new projects that runs on the server, authorises and returns DTOs, `server-only`, React `cache()` for in-request sharing, Prisma `globalThis` singleton for hot reload, `use cache` requires `cacheComponents`, `unstable_cache` replaced by `use cache` in Next 16.
Corrected or removed: unsupported vendor-specific serverless driver list and the edge/TCP claim; Prisma 7 adapter note added.
Method: documentation only; no commands were run.
