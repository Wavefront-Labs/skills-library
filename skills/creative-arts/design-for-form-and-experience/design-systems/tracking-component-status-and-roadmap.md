---
id: creative-arts.design-for-form-and-experience.design-systems.tracking-component-status-and-roadmap
name: tracking-component-status-and-roadmap
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [component-status, component-roadmap, design-system-roadmap, status-tracking, maturity-model, release-readiness, design-ops]
level: practitioner
status: draft
description: "Track design system component status and roadmap: define maturity stages with exit criteria, a status matrix across design, code and docs, and a public prioritised roadmap."
sources:
  - "Nathan Curtis (EightShapes), Design System Status / Component status (medium.com/eightshapes-llc)"
  - "Brad Frost - Design System roadmap and process (bradfrost.com)"
  - "Spotify Encore and GOV.UK component maturity labels (design-system.service.gov.uk/community/component-status)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Component status and roadmap

**Goal:** everyone can see which components are ready, in progress or planned, and trust the labels.

## Status stages with exit criteria
- **Proposed / Planned:** problem and demand documented.
- **In design:** research and variants done; accessibility approach drafted.
- **In development:** code built behind a flag or package tag.
- **Beta:** usable, API may change; real adopters testing.
- **Stable (released):** passes the release checklist: design spec, coded component with tests, accessibility audit (keyboard, screen reader, contrast), docs, Figma component with variants and properties, visual tests, changelog entry.
- **Deprecated / Removed:** with replacement and date (`creative-arts.design-for-form-and-experience.design-systems.versioning-deprecating-and-changelogging`).

## Status matrix
A table per component: Design status, Code status, Docs status, Accessibility status (not tested / partial / passed with date), Platforms (web, iOS, Android), Version introduced, Owner. Publish on the docs site and as a badge on component pages. Automate from package metadata and CI where possible.

## Roadmap
- Source work from intake requests and adoption data (`creative-arts.design-for-form-and-experience.design-systems.measuring-design-system-adoption`); score by number of requesting teams, effort and impact.
- Show **Now / Next / Later**, not dates, for anything uncertain; reserve 20-30 percent capacity for fixes and support.
- Review monthly with representatives of product teams; publish release notes at each iteration.

## Verify
- [ ] Each stage has written exit criteria; stable components pass the checklist.
- [ ] Status matrix visible and current; owners named.
- [ ] Roadmap derived from demand data and reviewed regularly.
