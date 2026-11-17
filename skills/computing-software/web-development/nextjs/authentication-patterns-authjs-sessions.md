---
id: computing-software.web-development.nextjs.authentication-patterns-authjs-sessions
name: authentication-patterns-authjs-sessions
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, nextjs-authentication, authjs, next-auth, sessions, middleware, proxy, authorization, web-development]
level: practitioner
status: docs-checked
description: "Implementing auth in Next.js App Router: Auth.js v5 setup, cookie sessions, optimistic proxy/middleware checks vs DAL checks, and protecting actions and routes."
sources:
  - https://nextjs.org/docs/app/guides/authentication
  - https://authjs.dev/getting-started/installation?framework=next.js
  - https://nextjs.org/blog/cve-2025-29927
  - https://nextjs.org/docs/app/api-reference/file-conventions/proxy
  - https://github.com/vercel/next.js/security/advisories/GHSA-f82v-jwr5-mffw
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication patterns in Next.js

**Goal:** sign-in that works across server components, actions, route handlers and middleware, with authorisation enforced where data is read.

## 1. Auth.js (NextAuth v5)
```ts
// auth.ts
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [GitHub],
  session: { strategy: "jwt" },          // or database sessions with an adapter
  callbacks: { session({ session, token }) { session.user.id = token.sub!; return session; } },
});
// app/api/auth/[...nextauth]/route.ts
export const { GET, POST } = handlers;
```
Env: `AUTH_SECRET` (`npx auth secret`), `AUTH_GITHUB_ID`, `AUTH_GITHUB_SECRET`. Use `await auth()` in server components, actions and route handlers.
Next's docs list Better Auth and Clerk among other auth libraries, and show a hand-rolled stateless session with `jose` (they recommend `iron-session` or `jose` for session management).

## 2. Layers of checks
| Layer | Purpose | Reliable? |
|---|---|---|
| `middleware.ts` / `proxy.ts` (Next 16) | optimistic redirect of logged-out users, read cookie only | no - never the only check |
| Data access layer | verify session, authorise per resource | yes |
| Server actions / route handlers | re-verify session and role every call | yes |
| UI | hide buttons | cosmetic |

CVE-2025-29927 let attackers skip middleware with a crafted `x-middleware-subrequest` header (fixed in 12.3.5/13.5.9/14.2.25/15.2.3); further Middleware/Proxy bypass advisories were published in 2026 (for example GHSA-492v-c6pp-mqqv and GHSA-6gpp-xcg3-4w24). Treat middleware and proxy as optimistic checks only.

## 3. Middleware/proxy example
```ts
export default auth((req) => {
  if (!req.auth && req.nextUrl.pathname.startsWith("/dashboard"))
    return Response.redirect(new URL("/login", req.nextUrl));
});
export const config = { matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"] };
```
Keep it fast: no DB queries per request. In Next 16 the file is `proxy.ts` (the `middleware` convention is deprecated and `proxy` runs on the Node.js runtime only); Auth.js documents `export { auth as proxy } from "@/auth"` there.

## 4. Server actions
```ts
"use server";
export async function deletePost(id: string) {
  const session = await auth();
  if (!session) throw new Error("Unauthorized");
  await db.post.delete({ where: { id, authorId: session.user.id } });
}
```

## 5. Session cookie hygiene
Next's docs list the cookie options `HttpOnly`, `Secure`, `SameSite`, `Max-Age`/`Expires` and `Path`; set an expiry and refresh it deliberately.

## 6. Layout pitfall
A check in `layout.tsx` doesn't re-run on client navigation between its pages. Check in each page or the DAL.

## Verify
- [ ] Calling a protected server action via raw POST without a cookie fails.
- [ ] Sending `x-middleware-subrequest` headers doesn't expose protected data (running a patched version).
- [ ] Logged-out users requesting `/dashboard` are redirected and protected data is never rendered.

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (guides/authentication, file-conventions/proxy, guides upgrading to 16), Auth.js docs source (nextauthjs/next-auth main, commit of 2026-07-22: installation and environment variables), GitHub security advisory GHSA-f82v-jwr5-mffw and the repository advisory list.
Confirmed: `AUTH_SECRET` and `npx auth secret`, `AUTH_GITHUB_ID`/`AUTH_GITHUB_SECRET`, `app/api/auth/[...nextauth]/route.ts` exporting `handlers`, `export { auth as proxy }`, middleware renamed to proxy in Next 16, optimistic checks in proxy versus data-layer checks, layout checks not re-running on navigation (partial rendering), CVE-2025-29927 patched versions (12.3.5, 13.5.9, 14.2.25, 15.2.3).
Corrected or removed: the unsupported Lucia mention, the localStorage and rolling-refresh cookie advice (replaced by the documented cookie options), and the missing 2026 bypass advisories.
Method: documentation only; no commands were run.
