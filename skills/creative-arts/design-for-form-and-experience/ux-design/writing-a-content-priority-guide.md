---
id: creative-arts.design-for-form-and-experience.ux-design.writing-a-content-priority-guide
name: writing-a-content-priority-guide
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [content-priority-guide, content-hierarchy, page-priority, content-first-wireframing, wireframing]
level: practitioner
status: draft
description: "Write a content priority guide for a page: list content, rank by user and business value, set reading order across breakpoints, then wireframe from it."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Content priority guides

A content priority guide ranks what goes on a page before layout, so the design follows importance and not the other way round. It is sometimes called a content hierarchy or a page table; the practice appears in content-first and mobile-first workflows.

## Steps
1. **List the content and functions** the page needs, from the sitemap, requirements and user tasks (see `...ux-design.drawing-a-sitemap`).
2. **Rank into tiers:**
   - **Primary:** the main purpose and its call to action; most users need it.
   - **Secondary:** supports the primary (proof, key details, related links).
   - **Tertiary:** occasional or reference items (legal, rarely used options).
3. **Check against users and business goals:** which tier does user research say each item belongs in; resolve conflicts with stakeholders.
4. **Set the order** for the narrowest screen first, as a single column list; this order becomes the reading order and screen-reader order.
5. **Note how it changes at wider breakpoints** (items that move beside others, collapse or hide); do not hide critical content on mobile.
6. **Attach to the wireframe** and use as the brief for content writers and designers.

## Format
A table: priority, content item, purpose, source, notes for each breakpoint.

## Verify
- [ ] The primary content occupies the top of the narrow layout.
- [ ] Every item has a reason and an owner.
- [ ] The guide matches the order in the wireframe and HTML.
