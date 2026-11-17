---
id: computing-software.web-development.nextjs.next-third-parties-tag-manager-and-embeds
name: next-third-parties-tag-manager-and-embeds
category: computing-software
field: web-development
product: nextjs
tags: [next-third-parties, google-tag-manager, google-analytics, third-party-scripts, nextjs]
level: practitioner
status: docs-checked
description: "Loading Google Tag Manager, Analytics, Maps and YouTube with @next/third-parties: setup, sending events, performance impact, consent handling, and when to use next/script instead."
sources:
  - https://nextjs.org/docs/app/guides/third-party-libraries
  - https://github.com/vercel/next.js/tree/canary/packages/third-parties
  - https://developers.google.com/tag-platform/security/guides/consent
  - https://nextjs.org/docs/app/api-reference/components/script
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @next/third-parties

Wrappers for popular third parties that load after hydration and use optimised embeds.

## 1. Google Tag Manager / Analytics
```tsx
// app/layout.tsx
import { GoogleTagManager } from "@next/third-parties/google";
export default function RootLayout({ children }) {
  return (<html lang="en"><GoogleTagManager gtmId="GTM-XXXXXXX" /><body>{children}</body></html>);
}
// sending events from client code
"use client";
import { sendGTMEvent } from "@next/third-parties/google";
<button onClick={() => sendGTMEvent({ event: "signup_click", plan: "pro" })}>Sign up</button>
```
- `GoogleAnalytics gaId="G-XXXX"` + `sendGAEvent("event", "purchase", { value })` if using gtag directly.
- Pageviews on client navigations: Google Analytics tracks pageviews when the browser history state changes; verify that Enhanced Measurement's "Page changes based on browser history events" option is enabled, and disable the default pageview if you send them manually (see the Next docs).
- Next's docs recommend configuring Google Analytics through Tag Manager when GTM is already included, rather than also adding `GoogleAnalytics`.

## 2. Embeds
```tsx
import { YouTubeEmbed, GoogleMapsEmbed } from "@next/third-parties/google";
<YouTubeEmbed videoid="ogfYd705cRs" height={400} params="controls=0" />     // uses lite-youtube-embed facade
<GoogleMapsEmbed apiKey={process.env.NEXT_PUBLIC_MAPS_KEY!} height={300} width="100%" mode="place" q="Brisbane,Australia" />
```
`YouTubeEmbed` uses `lite-youtube-embed` under the hood; `GoogleMapsEmbed` lazy-loads the embed below the fold through the `loading` attribute.

## 3. Consent
Tags must respect consent (GDPR/ePrivacy). Set Google Consent Mode defaults **before** GTM loads:
```tsx
<Script id="consent-default" strategy="beforeInteractive">{`
  window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}
  gtag('consent','default',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});`}</Script>
```
Update with `gtag('consent','update',{...})` from your consent banner. Or only render `<GoogleTagManager>` after consent is granted.

## 4. Performance
Audit GTM tags regularly and remove unused ones. The `next/script` `worker` strategy is not yet stable, does not work with the App Router, and is not guaranteed to support all third-party scripts.

## 5. Other scripts
For vendors without a wrapper use `next/script` with `strategy="afterInteractive"` (default) or `lazyOnload`.

## Verify
- [ ] Tag fires once per page view including client navigations (GTM preview mode); no tags fire before consent; Lighthouse third-party summary acceptable.

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (guides/third-party-libraries, components/script) and Google Tag Platform consent guide (fetched 2026-10-25).
Confirmed: `GoogleTagManager` placement inside `<html>` and loading after hydration, `sendGTMEvent`, `GoogleAnalytics` and `sendGAEvent('event', name, params)`, `YouTubeEmbed` (`videoid`, `params`, `height`), `GoogleMapsEmbed` (`apiKey`, `mode`, `q`), GA history-change pageviews, `gtag('consent','default'|'update', ...)` with `ad_storage`, `analytics_storage`, `ad_user_data` and `ad_personalization`, consent defaults before measurement commands.
Corrected or removed: the unsupported GTM History Change trigger advice, the "use only one of GTM or GA" rule (replaced with the Next recommendation), the INP and Partytown claims.
Method: documentation only; no commands were run.
