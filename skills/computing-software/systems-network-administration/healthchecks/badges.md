---
id: computing-software.systems-network-administration.healthchecks.badges
name: badges
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, status-badges, svg-badge, shields-io, three-state-badge]
level: intro
status: docs-checked
description: "Embed Healthchecks status badges for a project, a tag or one check: up, late and down states, SVG, JSON and Shields.io formats, and URL privacy."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/badges.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A badge can show the combined status of all checks in a project, of checks with a given tag, or of a single check. Badge URLs are public but hard to guess; they reveal only the label and aggregate status, and ping URLs cannot be derived from them.

States:
- up (green): all matching checks are up.
- late (orange): at least one check is late but still inside grace time.
- down (red): at least one matching check is down.

By default URLs report only up and down, treating late as up. The "Badge states" radio buttons switch to alternate URLs reporting all three.

Formats:
- SVG for an `<img>` element or Markdown.
- JSON with label and status, to render yourself or feed a hosted status page that watches the URL for the keyword "up".
- Shields.io endpoint JSON for extra styles (see shields.io/endpoint).

The exact URLs are shown on the Badges page in the dashboard. They are also available through the API (see api-badges-status).

## Checked

2026-11-04: confirmed against the Status Badges page (scope, hard-to-guess URLs, up/late/down, default up and down only, SVG/JSON/Shields.io formats).
Method: documentation only; no commands were run.
