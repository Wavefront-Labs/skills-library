---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-mobile-navigation
name: designing-mobile-navigation
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [tab-bar, hamburger-menu, mobile-navigation, bottom-navigation, navigation-drawer, thumb-zone, mobile-ux]
level: practitioner
status: draft
description: "Design mobile navigation: bottom tab bar for 3-5 top destinations, labelled icons, hamburger or drawer only for secondary items, thumb-reachable controls and state memory."
sources:
  - "Apple Human Interface Guidelines - Tab bars (developer.apple.com/design/human-interface-guidelines/tab-bars)"
  - "Material Design 3 - Navigation bar and navigation drawer (m3.material.io/components/navigation-bar)"
  - "Nielsen Norman Group - Hamburger Menus and Hidden Navigation Hurt UX Metrics (nngroup.com/articles/hamburger-menus)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile navigation

**Goal:** top destinations are one tap away, reachable by thumb, and clearly labelled.

## Choose the pattern
- **Bottom tab bar (iOS) / navigation bar (Material):** 3-5 top-level destinations of equal importance; always visible; best discoverability and engagement.
- **Navigation rail / drawer:** tablets and apps with more than 5 destinations; Material drawer or iOS split view and sidebar.
- **Hamburger (hidden) menu:** NN/g found hidden navigation lowers discoverability and use; use it only for secondary or rare destinations, or in a combination (visible tabs plus "More").
- **Top app bar:** title, back, and 1-2 actions; not the primary navigation for the whole app.

## Details
1. **Icon plus text label** for each tab (icon-only is ambiguous); filled icon or colour for the active tab, plus label weight (not colour alone).
2. **Tap targets:** at least 44x44 pt (iOS) or 48x48 dp (Android); tab bar height about 49 pt iOS / 80 dp Material 3.
3. **Keep tab positions stable;** do not reorder dynamically or hide tabs.
4. **State memory:** each tab remembers its own stack; tapping the active tab pops to root and scrolls to top.
5. **Badges** on tabs for counts, sparingly.
6. **Thumb zone:** place frequent actions in the lower half; floating action buttons for the one primary action; avoid top-left only destinations on large phones.
7. Respect **safe areas** (home indicator, notch), system back gesture and Android back button behaviour.

## Verify
- [ ] 3-5 labelled tabs for primary destinations; active state is clear.
- [ ] Each tab keeps its own navigation state.
- [ ] Targets meet minimum sizes; works with system gestures.
