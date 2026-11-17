---
id: computing-software.web-development.nextjs.nextjs-security-hardening
name: nextjs-security-hardening
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-security, taint-api, middleware-bypass, server-only, image-optimizer-ssrf, nextjs]
level: advanced
status: docs-checked
description: "Hardening Next.js apps: authorise in the data layer not just middleware, server-only and taint APIs, env exposure, image remotePatterns, security headers and patch hygiene."
sources:
  - https://nextjs.org/blog/security-nextjs-server-components-actions
  - https://nextjs.org/docs/app/guides/data-security
  - https://github.com/vercel/next.js/security/advisories
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/images
  - https://nextjs.org/docs/app/guides/content-security-policy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Next.js security hardening

## 1. Do not rely on middleware for authorization
Middleware is a convenient first gate (redirect anonymous users), not the boundary. CVE-2025-29927 let attackers skip middleware entirely with a crafted `x-middleware-subrequest` header on unpatched versions, and further Middleware/Proxy bypass advisories were published in 2026 (for example GHSA-492v-c6pp-mqqv and GHSA-36qx-fr4f-26g5). Check auth and permissions where data is read or mutated:
```ts
// lib/dal.ts
import "server-only";
export const getInvoice = cache(async (id: string) => {
  const user = await requireUser();                 // reads session cookie, throws/redirects if absent
  const inv = await db.invoice.findUnique({ where: { id } });
  if (!inv || inv.orgId !== user.orgId) notFound();
  return toInvoiceDTO(inv);                         // only fields the UI needs
});
```
Pages, route handlers and Server Actions all go through the data access layer.

## 2. Stop secrets reaching the client
- `import "server-only"` in modules with secrets/DB access, so that server-only code is not executed on the client (Next's data-security guide).
- Only `NEXT_PUBLIC_*` env vars are inlined into client bundles; never prefix secrets.
- Props passed from Server to Client Components are serialised into the HTML/RSC payload: pass DTOs, not ORM rows.
- Taint APIs (`experimental.taint: true`): `experimental_taintObjectReference("Do not pass user rows", userRow)`, `experimental_taintUniqueValue` for tokens.

## 3. Server Actions and route handlers
Treat as public endpoints: validate input (zod), authorise per object, rate-limit; keep `serverActions.allowedOrigins` tight behind proxies.

## 4. Other surfaces
- `images.remotePatterns`: list exact hosts, paths and search strings; Next's docs warn that omitting `protocol`, `port`, `pathname` or `search` implies a wildcard that may let malicious actors optimise URLs you did not intend.
- `redirect()` with user input: validate (open redirect).
- Security headers in `next.config` `headers()` or a proxy: CSP (Next's CSP guide covers nonces), HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `frame-ancestors`; `poweredByHeader: false` removes `x-powered-by`.
- `dangerouslySetInnerHTML` only with sanitised HTML.

## 5. Patch hygiene
Next.js has published critical advisories (for example remote code execution in the Image Optimization API and in `next/og`) as well as middleware/proxy bypass and cache-poisoning advisories. Subscribe to the GitHub security advisories, enable Dependabot/Renovate for `next`/`react*`, and patch within days.

## Verify
- [ ] Requests with `x-middleware-subrequest` do not bypass auth; every DAL function checks the user; `grep -r NEXT_PUBLIC_` shows no secrets.

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (guides/data-security, config taint, serverActions, images, poweredByHeader, content-security-policy) and the vercel/next.js security advisory list read through the GitHub API.
Confirmed: DAL and DTO approach, `server-only`, `NEXT_PUBLIC_` exposure rule, `experimental.taint` with `experimental_taintObjectReference` and `experimental_taintUniqueValue`, `serverActions.allowedOrigins` Origin comparison, `remotePatterns` wildcard warning, `poweredByHeader`, existence of the cited advisories and CVE-2025-29927.
Corrected or removed: the "fails the build" server-only claim, the "RSC deserialisation" advisory category (not found in the advisory list), and the open-proxy/SSRF wording for wildcards.
Method: documentation only; no commands were run.
