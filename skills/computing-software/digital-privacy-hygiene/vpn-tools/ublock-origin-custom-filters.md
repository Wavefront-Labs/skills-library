---
id: computing-software.digital-privacy-hygiene.vpn-tools.ublock-origin-custom-filters
name: ublock-origin-custom-filters
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, custom-filters, ublock-origin, tracker-blocking]
level: practitioner
status: draft
description: "Write uBlock Origin custom filters: network blocks, cosmetic hides, allowlist exceptions, the element picker and per-site switches, with safe syntax."
sources:
  - "https://github.com/gorhill/uBlock/wiki/Static-filter-syntax"
  - "https://github.com/gorhill/uBlock/wiki/Element-picker"
  - "https://github.com/gorhill/uBlock/wiki/Per-site-switches"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# uBlock Origin custom filters

**Goal:** remove a specific annoyance or tracker the lists missed, or fix one site without disabling uBO.

## Where
Dashboard > **My filters**. One filter per line; `!` starts a comment.

## Common filters
```
! Block a tracker domain everywhere
||tracker.example^
! Block a third-party script only on one site
||cdn.example.net/analytics.js$script,domain=news.example
! Hide an element (cosmetic)
news.example##.newsletter-popup
! Hide an element everywhere (careful)
##.cookie-wall
! Strip a tracking parameter
||example.com^$removeparam=ref
! Exception: allow a blocked request that breaks a site
@@||cdn.example.net/player.js$script,domain=video.example
```

## Element picker and zapper
- **Picker** (eyedropper icon): click the element, refine the selector with the sliders, Create. Adds a cosmetic
  filter to My filters.
- **Zapper** (lightning): removes an element temporarily for this page view only.

## Per-site switches (popup icons)
No large media, no cosmetic filtering, no remote fonts, **no JavaScript** for this site. Saved per hostname.
Click the big power button to disable uBO on a site entirely (whitelist), as a last resort.

## Gotchas
- Generic cosmetic filters (`##.class`) run on every site and can break layouts elsewhere; scope with a domain.
- Exceptions (`@@`) override lists globally if unscoped; always add `domain=`.
- Back up My filters (Dashboard > Settings > Back up to file).
