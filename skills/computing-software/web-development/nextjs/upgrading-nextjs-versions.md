---
id: computing-software.web-development.nextjs.upgrading-nextjs-versions
name: upgrading-nextjs-versions
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-upgrade, next-codemod, async-request-apis, nextjs-15, nextjs-16, nextjs]
level: practitioner
status: docs-checked
description: "Upgrading Next.js major versions: running the upgrade codemod, Next 15 async request APIs and caching default changes, newer release changes, and a safe rollout checklist."
sources:
  - https://nextjs.org/docs/app/guides/upgrading/version-15
  - https://nextjs.org/docs/app/guides/upgrading/codemods
  - https://nextjs.org/blog
  - https://nextjs.org/docs/app/guides/upgrading/version-16
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Next.js versions

## 1. Process
1. Read the version's upgrade guide and blog post end to end.
2. Upgrade one major at a time; get the current major's latest minor clean first.
3. Run the codemod CLI:
```bash
npx @next/codemod@canary upgrade latest     # bumps next/react, runs relevant codemods interactively
npx @next/codemod@latest next-async-request-api .   # individual transform example
```
4. Fix TypeScript errors (`next build` type-checks), then lint and tests.
5. Deploy to a preview environment; compare caching behaviour, response headers and Web Vitals before production.

## 2. Next 15 changes that bite
- **Async request APIs**: `cookies()`, `headers()`, `draftMode()`, and page/layout `params` / `searchParams` return Promises: `const { slug } = await params`. Client components use `React.use(params)`.
- **Caching defaults flipped**: `fetch` is not cached by default (opt in with `cache: "force-cache"` or `use cache`); GET route handlers are dynamic by default; the client router cache no longer reuses page segments on `<Link>`/`useRouter` navigation (opt back in with `staleTimes`).
- React 19 is required for the App Router.
- `next/font` replaced `@next/font`; `experimental.serverComponentsExternalPackages` became `serverExternalPackages`.

## 3. Later releases
Next 16: Turbopack is stable and the default for `next dev` and `next build` (a custom `webpack` config makes `next build` fail unless you opt out), the minimum Node.js is 20.9, synchronous access to the request APIs is fully removed, the `middleware` file is deprecated and renamed `proxy` (Node.js runtime only), `next lint` is removed, and `cacheComponents: true` opts into Cache Components and `use cache`. The `upgrade` codemod does not run every migration codemod, so also run `next-async-request-api` if you still use synchronous access. Read the exact list for your target version.

## 4. Watch for
- Third-party packages pinned to older React/Next peer versions (auth libraries, MDX, CMS SDKs).
- Custom webpack config: needs Turbopack equivalents or an explicit webpack opt-out.
- Self-hosting: Node version minimums, standalone output changes, image optimisation (sharp) installs.

## Verify
- [ ] `next build` passes with no deprecation warnings; preview deploy shows identical cache headers for key routes and no regression in Web Vitals.

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (guides/upgrading: version-15, version-16, codemods).
Confirmed: `npx @next/codemod@canary upgrade latest`, `npx @next/codemod@latest next-async-request-api .`, async `cookies()`/`headers()`/`draftMode()`/`params`/`searchParams` in 15, `fetch` and GET route handlers not cached by default in 15, client router cache segment reuse change and `staleTimes`, `@next/font` replaced by `next/font`, `serverExternalPackages` rename, React 19 for the App Router, Turbopack default, Node.js 20.9 minimum, `middleware` to `proxy`, `next lint` removal, `cacheComponents`.
Corrected or removed: the vague "renamed/rewired" and "replacing earlier experimental flags" wording, and the `staleTimes.dynamic` value.
Method: documentation only; no commands were run.
