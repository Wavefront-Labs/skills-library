---
id: creative-arts.design-for-form-and-experience.ux-design.drawing-a-sitemap
name: drawing-a-sitemap
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [sitemap, site-map, ia-sitemap, site-structure, navigation-hierarchy, information-architecture]
level: practitioner
status: draft
description: "Draw a sitemap that shows pages, hierarchy and relationships: notation, depth and breadth choices, cross-links, annotations and how to keep it maintained."
sources:
  - "Louis Rosenfeld, Peter Morville and Jorge Arango, Information Architecture, 4th ed. (O'Reilly, 2015)"
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sitemaps

A sitemap is a diagram of the hierarchy and relationships of pages or content groups in a site or app. (Do not confuse it with an XML sitemap file for search engines.)

## Build
1. **Start from the content inventory** (see `...ux-design.running-a-content-inventory-and-audit`) and the research on grouping (see `...ux-design.running-an-open-or-closed-card-sort`).
2. **Draw the top level** (global navigation items), then children; use boxes for pages and lines for parent-child links; use a distinct notation for cross-links, external links, hidden or login-only pages, and templates.
3. **Balance breadth and depth:** shallow, broad structures often help scanning, but too many top-level choices overwhelm; test with a tree test.
4. **Number the nodes** (1.0, 1.1, 1.2) so wireframes and requirements can reference them.
5. **Annotate:** page name, template, owner, content source, audience, status, and URL pattern.
6. **Show states:** logged in vs out, roles, localised branches.
7. **Review** with stakeholders and users; keep a changelog.

## Tools
Any diagramming tool works (FigJam, Miro, Figma, Whimsical, OmniGraffle, spreadsheet with an outline); keep it in one place.

## Gotchas
- Mirroring the organisation chart instead of user needs.
- A sitemap that shows only pages, not how people move between them; pair with user flows.

## Verify
- [ ] Every page in the inventory is on the map or marked for removal.
- [ ] Labels came from research, not internal jargon.
- [ ] A tree test supports the top two levels.
