---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-mega-menus
name: designing-mega-menus
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [mega-menu, mega-menus, dropdown-navigation, navigation-design, large-menus, menu-design]
level: practitioner
status: draft
description: "Design mega menus that work: reserve them for large catalogues, group links with headings, open on click or forgiving hover, support keyboard and touch, and keep them scannable."
sources:
  - "Nielsen Norm Group - Mega Menus Work Well for Site Navigation (nngroup.com/articles/mega-menus-work-well)"
  - "W3C WAI - Menus Tutorial and fly-out menus (w3.org/WAI/tutorials/menus)"
  - "Baymard Institute - Mega dropdown usability (baymard.com/blog/mega-dropdown-navigation)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mega menus

**Goal:** expose a large, structured set of destinations in one view when a standard dropdown cannot.

## Use when
Large e-commerce, media and enterprise sites with 2 levels of categories and many items. For simple sites, a plain dropdown or no submenu is better.

## Design
- **Group links under clear headings,** 3-5 columns, scannable lists; show only the most popular 5-8 links per group with a "View all" link. Not a wall of links.
- **Flat, 2 levels only;** no menu inside a menu. Mark top categories as clickable landing pages.
- **Activation:** open on **click or tap** (and keyboard Enter/Space); for hover, add 100-300 ms open delay and a forgiving diagonal path (hover intent) so the pointer does not close it when moving. Close on Esc, outside click, and focus leaving.
- **Visuals:** consistent typography, optional icons or one or two promo images (avoid distracting banners); large touch targets (at least 44 px); sufficient contrast over the page.
- **Mobile:** replace with an accordion or drill-down drawer with back; do not shrink a mega menu.
- **Keep the menu panel attached** to its trigger, with an arrow or highlight showing the active item.

## Accessibility
`<nav>` with buttons that toggle `aria-expanded`; focus moves in order into the panel; Esc returns focus to the trigger; no `role="menu"` unless implementing full arrow-key menubar behaviour; links are plain links. Content must be reachable without hover.

## Verify
- [ ] Two levels, grouped under headings, view-all links present.
- [ ] Opens by click and keyboard, hover has intent delay.
- [ ] Mobile alternative; focus management correct.
