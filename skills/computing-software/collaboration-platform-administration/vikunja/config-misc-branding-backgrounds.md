---
id: computing-software.collaboration-platform-administration.vikunja.config-misc-branding-backgrounds
name: config-misc-branding-backgrounds
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, project-backgrounds, unsplash-provider, legal-links, custom-logo, sentry-telemetry]
level: practitioner
status: docs-checked
description: "Configure project backgrounds including Unsplash, legal footer links, custom logos, the MOTD and Sentry error tracking in Vikunja."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Backgrounds: `backgrounds.enabled` default true. Providers: `backgrounds.providers.upload.enabled` (true) and `backgrounds.providers.unsplash.enabled` (false). For Unsplash create an application at unsplash.com and set `accesstoken` and `applicationid` (used for pingbacks).

Legal links: add any number of `legal.<link key>` entries, each with `text` and `url`, shown sorted by key. Environment form: `VIKUNJA_LEGAL_<LINK KEY>_TEXT` and `VIKUNJA_LEGAL_<LINK KEY>_URL`. `legal.imprinturl` and `legal.privacyurl` are deprecated.

Branding: `service.customlogourl` and `service.customlogourldark`; `service.allowiconchanges` (default true) allows occasion-based icon changes; `service.motd` is exposed by the `/info` endpoint.

Sentry: `sentry.enabled` and `sentry.frontendenabled` both default false and enable anonymous error tracking of API and frontend errors; DSNs are configurable.

`service.demomode` shows a red warning that data will be cleared; it was built for try.vikunja.io.

## Checked

2026-11-04: checked against config-raw.json (backgrounds, legal, sentry, service.* sections). Removed the line saying `/api/v1/info` lists background providers and legal links; the source only says `motd` is available from `/info`.

Method: documentation only; no commands were run.
