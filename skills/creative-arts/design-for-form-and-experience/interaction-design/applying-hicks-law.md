---
id: creative-arts.design-for-form-and-experience.interaction-design.applying-hicks-law
name: applying-hicks-law
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [hicks-law, choice-overload, laws-of-ux, decision-time, menu-design, simplicity, progressive-disclosure]
level: practitioner
status: draft
description: "Apply Hick's law: reduce decision time by cutting and grouping choices, highlighting a recommended option, chunking menus and revealing options progressively."
sources:
  - "Hick, On the rate of gain of information (1952) and Hyman (1953)"
  - "Jon Yablonski, Laws of UX (lawsofux.com/hicks-law)"
  - "Iyengar and Lepper, When Choice is Demotivating (2000)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hick's law and choice overload

**Law:** decision time rises with the number and complexity of options (roughly log2(n+1)). It is not "never exceed 7 items"; it is about reducing effort.

## Tactics
1. **Cut options:** remove rarely used choices; default sensibly; combine near-duplicates. Each option must earn its place.
2. **Group and categorise** (chunk) so users decide within a small set at a time: navigation categories, grouped settings, tabs for long forms.
3. **Highlight a recommendation:** "Most popular" or "Recommended" plan; visual emphasis on the best-for-most option; pre-select a default.
4. **Progressive disclosure:** show the common options first, reveal advanced ones on demand (`creative-arts.design-for-form-and-experience.interaction-design.applying-progressive-disclosure`).
5. **Sequence decisions:** break a big choice into steps (a guided finder: "What size room? What budget?").
6. **Support comparison** when choices are many and valuable (side-by-side table, 2-4 items), not a long scroll of unrelated cards.
7. **Reduce complexity of each option:** clear names, comparable attributes, plain pricing.
8. **Allow search and filtering** over very large sets (`creative-arts.design-for-form-and-experience.interaction-design.designing-filtering-and-sorting`).

## Caveats
- Experts want speed and shortcuts rather than reduced options (keyboard commands, recents).
- Do not hide critical options; when users know exactly what they want, many choices can be fine (large catalogues with strong search).
- In pricing pages, 3 tiers with a highlighted middle is common but test it.

## Verify
- [ ] Choice sets are chunked, defaulted and contain a recommended option.
- [ ] Advanced options are disclosed progressively.
