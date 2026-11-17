---
id: creative-arts.design-for-form-and-experience.interaction-design.applying-jakobs-law-and-web-conventions
name: applying-jakobs-law-and-web-conventions
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [jakobs-law, design-conventions, web-conventions, familiarity, patterns, mental-models, laws-of-ux]
level: practitioner
status: draft
description: "Apply Jakob's law: follow established conventions for common patterns, deviate deliberately with evidence, and check patterns against what users know from other sites."
sources:
  - "Jakob Nielsen, Jakob's Law of Internet User Experience (nngroup.com/videos/jakobs-law-internet-ux)"
  - "Jon Yablonski, Laws of UX (lawsofux.com/jakobs-law)"
  - "Nielsen Norman Group - Consistency and Standards (nngroup.com/articles/consistency-and-standards)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jakob's law and web conventions

**Law:** users spend most of their time on other sites, so they expect yours to work like those.

## Conventions to keep (examples)
- Logo top-left linking home; global navigation top or left; search top right with a magnifier; cart top right on shops; account/profile top right.
- Blue underlined text for links; buttons look like buttons; primary action at the end of the flow on the right (LTR); form labels above or beside fields; hamburger icon for a collapsed menu on mobile (with a label where possible).
- Standard icons (magnifier, trash, share, heart, cog) and gestures (pull to refresh, swipe back).
- Checkout order: cart, shipping, payment, review; footer with contact, legal and sitemap links.
- Keyboard: Tab order, Esc closes, Enter submits, Ctrl/Cmd+Z undoes, Space activates buttons.

## Procedure
1. **List patterns** your design uses; for each, note the dominant convention (look at 5-10 leading sites and platform guidelines).
2. **Match by default.** Innovation belongs in your value proposition, not in how a login form works.
3. **If you deviate,** write the reason and expected benefit, and test it (a first-click test, an A/B test; `creative-arts.design-for-form-and-experience.ux-design.designing-an-ab-test`). Make the unconventional pattern self-explanatory with strong signifiers.
4. **Respect platform conventions** (iOS back swipe, Android back button, desktop menus).
5. **Keep internal consistency** too; do not use two patterns for the same task.
6. **Redesign carefully:** big changes to familiar layouts cause temporary performance drops; offer a transition (preview, opt-in, tours).

## Verify
- [ ] Each pattern compared with the convention; deviations justified and tested.
- [ ] Platform-specific behaviours preserved.
