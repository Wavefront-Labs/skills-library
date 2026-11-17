---
id: creative-arts.game-design.systems-and-mechanics.living-design-docs-and-wikis
name: living-design-docs-and-wikis
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-and-mechanics, living-design-doc, design-wiki, design-documentation, confluence, notion]
level: practitioner
status: draft
description: "Run game design documentation as a living wiki: page structure, ownership, status labels, decision logs, links to data and tickets, and pruning stale pages."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.atlassian.com/software/confluence/templates/product-requirements
  - https://www.routledge.com/Game-Design-Workshop-A-Playcentric-Approach-to-Creating-Innovative-Games/Fullerton/p/book/9781032611631
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Living design docs and design wikis

**Goal:** documentation that stays true as the game changes, so the team trusts it.

Schell's documents chapter: design docs exist for memory and communication. Most teams
replace the monolithic up-front GDD with small, current, linked pages.

## Structure
- **Home:** vision, pillars, one-page concept, glossary, page index.
- **One page per feature, system, level and character.**
- **Data lives in sheets/tables** linked from pages, never pasted.
- **Decision log:** date, decision, reason, alternatives rejected.

## Page conventions
- Header block: owner, status (Draft / In review / Approved / Implemented / Deprecated),
  last-reviewed date, linked tickets.
- A one-line summary per significant change (page history keeps the detail).
- Templates (Confluence, Notion, Google Docs) so every page reads the same.

## Keeping it alive
1. The definition of done for a feature includes "doc updated".
2. Per-milestone doc review: owners confirm or mark pages Deprecated.
3. Link tickets both ways (tracker to page, page to epic).
4. Archive deprecated pages with a banner pointing to the replacement.
5. Keep a glossary for every term of art; disagreements over words become bugs.

## Gotchas
- Pages without an owner rot first; allow no orphans.
- Duplicate pages for one system cause conflicting builds; search before creating.
- Screenshots go stale fastest; caption them with the build number.

## Verify
- [ ] Every page has owner, status and last-reviewed date.
- [ ] Data linked, not copied.
- [ ] Decision log in use.
- [ ] Review cadence on the calendar.
