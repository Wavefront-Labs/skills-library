---
id: creative-arts.design-for-form-and-experience.interaction-design.structuring-global-navigation
name: structuring-global-navigation
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [global-navigation, navigation-design, mega-menu, navigation-structure, information-architecture, menu-design, nav-bar]
level: practitioner
status: draft
description: "Structure global navigation: pick 5-7 top-level labels from top tasks, choose a pattern, keep it persistent and consistent, mark the current location, and test with tree tests."
sources:
  - "Nielsen Norman Group - Top 10 Application-Design Mistakes and Navigation topic (nngroup.com/topic/navigation)"
  - "Nielsen Norman Group - Menu-Design Checklist: 17 UX Guidelines (nngroup.com/articles/menu-design)"
  - "Peter Morville and Louis Rosenfeld, Information Architecture, 4th ed. (O'Reilly, 2015), navigation systems"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Global navigation structure

**Goal:** people always know where they are, where they can go, and how to get back.

## Structure
1. **Start from top tasks and the IA** (`creative-arts.design-for-form-and-experience.ux-design.user-flows-and-low-fidelity-wireframes` for flows; card sort and tree test for labels). Navigation is the visible surface of the IA.
2. **Limit top level to about 5-7 items,** ordered by importance (first and last positions are remembered best); group the rest.
3. **Labels:** user words, specific and parallel ("Pricing", not "Solutions"). Avoid generic ("Resources") unless tree tests pass.
4. **Pattern:** horizontal top bar (desktop websites, 5-9 items), left sidebar (apps with many sections, 8+ items, collapsible), bottom tab bar (mobile, 3-5), hamburger or drawer only for secondary items on small screens.
5. **Keep it persistent and consistent** across pages: same position, order and labels; utility items (search, account, cart) in the usual place at the top right.
6. **Show location:** highlight the current section (not colour only: weight or underline plus `aria-current="page"`) and add breadcrumbs for deep sites.
7. **Dropdowns:** open on click for accessibility (hover alone fails touch and keyboard); at most two levels deep; large targets, forgiving hover paths.
8. **Make the parent clickable** as a landing page when it opens a submenu.

## Test
- **Tree test** (Optimal Workshop, Maze): 15-30 users find items by label; aim for 70+ percent success on key tasks.
- **First-click test** on the navigation bar.

## Verify
- [ ] 5-7 top items with user-language labels, validated in a tree test.
- [ ] Current location indicated visually and programmatically.
- [ ] Works by keyboard, touch and screen reader.
