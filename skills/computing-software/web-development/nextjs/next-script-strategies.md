---
id: computing-software.web-development.nextjs.next-script-strategies
name: next-script-strategies
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-optimization, nextjs-metadata, next-script, third-party-scripts, script-strategy, afterinteractive, lazyonload, google-tag-manager, nextjs-third-parties]
level: practitioner
status: docs-checked
description: "Loading third-party scripts in Next.js with next/script strategies (beforeInteractive, afterInteractive, lazyOnload, worker), onLoad, CSP nonces and @next/third-parties."
sources:
  - https://nextjs.org/docs/app/api-reference/components/script
  - https://nextjs.org/docs/app/guides/third-party-libraries
  - https://web.dev/articles/optimizing-content-efficiency-loading-third-party-javascript
  - https://nextjs.org/docs/app/guides/content-security-policy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# next/script strategies

**Goal:** third-party tags load at the right time without blocking hydration or hurting INP.

## 1. Strategies
| Strategy | When it loads | Use for |
|---|---|---|
| `beforeInteractive` | Injected in initial HTML, before hydration (root layout only) | Bot detection, consent managers that must run first |
| `afterInteractive` (default) | After some hydration | Tag managers, analytics |
| `lazyOnload` | During browser idle after load | Chat widgets, social embeds, feedback tools |
| `worker` (experimental) | Web worker (the docs say it is not yet stable and does not yet work with the App Router) | Heavy analytics |

```tsx
import Script from 'next/script';
<Script id="ld" strategy="lazyOnload" src="https://widget.example.com/chat.js" onLoad={() => window.Chat?.init({ id: 'X' })} />
<Script id="config" strategy="afterInteractive">{`window.dataLayer=window.dataLayer||[];`}</Script>
```
- Give inline scripts an `id`, as the docs' examples do.
- `onLoad`/`onReady`/`onError` only work in Client Components and cannot be used with `beforeInteractive` (use `onReady` instead of `onLoad` there); `onReady` runs after the first load and on every re-mount (use it for re-initialising widgets after client navigation).
- `beforeInteractive` scripts run once per document load and are not run again by client-side navigation; `afterInteractive` and `lazyOnload` scripts load when a page or layout containing them is opened.

## 2. @next/third-parties
`<GoogleTagManager gtmId="GTM-XXXX" />`, `<GoogleAnalytics gaId=… />`, `<YouTubeEmbed>`, `<GoogleMapsEmbed>` - pre-tuned loading (facades for embeds). Use instead of hand-written snippets.

## 3. CSP
With a nonce-based CSP, Next.js reads the nonce from the `Content-Security-Policy` header and applies it to framework scripts, page bundles, inline scripts and styles it generates, and any `<Script>` that uses the `nonce` prop (the CSP guide sets the nonce in a proxy).

## 4. Discipline
Every tag costs main-thread time; audit with the browser Performance panel, and load marketing tags only after consent and only on pages that need them.

## Verify
- [ ] Performance panel: no third-party long tasks before hydration completes (except beforeInteractive ones).
- [ ] Widgets still initialise after client-side navigation.
- [ ] CSP has no violations for scripts loaded via next/script.

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (components/script, guides/third-party-libraries, guides/content-security-policy).
Confirmed: the four strategies and their descriptions, `beforeInteractive` only inside a root layout, `worker` not stable and not working with the App Router, `onLoad`/`onReady`/`onError` restrictions, `onReady` on re-mount, nonce application rules, `@next/third-parties` components.
Corrected or removed: the "Pages Router" and Partytown labels on `worker`, the unconfirmed "inline scripts need an id" requirement, the "loaded once per page lifecycle" claim (replaced with the documented per-strategy behaviour) and the Lighthouse audit name.
Method: documentation only; no commands were run.
