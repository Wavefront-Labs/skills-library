---
id: creative-arts.graphic-design.brand-identity.brand-typography-system
name: brand-typography-system
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, identity-system, brand-typography, typeface-selection, font-licensing, system-fonts, fallback-fonts, type-hierarchy, visual-identity, custom-typeface]
level: practitioner
status: draft
description: "Specify a brand typography system: primary and secondary typefaces, hierarchy rules, licensing for every channel, fallback fonts for Office and web, and when custom type pays off."
sources:
  - https://learn.microsoft.com/en-us/typography/fonts/windows_11_font_list
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brand typography system

**Goal:** typefaces and rules that make every piece of brand communication recognisable, usable by the
client's team, and legally licensed everywhere it appears.

## Choose the families
- **Primary:** carries the voice (headlines and often body). Needs weights, italics, languages and figures
  the brand will use.
- **Secondary (optional):** contrast for body or data (a serif with a sans, a mono for tech brands).
- Two families is usually enough; superfamilies (sans + serif) give contrast with harmony.
- **Custom or customised type** (bespoke font or modified retail font) pays off for large brands: distinct
  voice, no per-seat licence fees, but costs design time and money.

## Hierarchy rules
- Define headline, subhead, body, caption, label styles with size ratios, weights, case, tracking and
  leading, for print and for screen (see ui-type-ramps-and-type-tokens skill).
- Show do and don't examples: no more than two weights in one piece, headline case rules, alignment default.

## Licensing (plan before choosing)
- Desktop seats for designers and agencies, **web** (pageviews or self-hosted), **app embedding**,
  **ePub**, **broadcast/video**, **server** (dynamic image generation), and Office sharing.
- Check whether partners and printers need licences; budget per channel.

## Fallbacks
- **Office / Google Workspace:** specify a system font substitute with similar metrics (e.g. Arial or
  Aptos for a neo-grotesque, Georgia for a serif) for documents created by staff.
- **Web:** CSS font stack with fallback metrics (see web-font-loading-and-font-display).
- **Email:** web fonts work only in some clients; set a fallback that preserves layout.

## Gotchas
- A retail font many competitors already use weakens distinctiveness; check the category.
- Variable fonts may not be supported in older Office versions or some print RIPs; supply static instances.
- Missing language support (Greek, Cyrillic, Vietnamese) appears late in rollout; ask early.

## Verify
- [ ] Every channel has a licensed font or a defined fallback.
- [ ] Hierarchy specimen page shows each style with exact values.
