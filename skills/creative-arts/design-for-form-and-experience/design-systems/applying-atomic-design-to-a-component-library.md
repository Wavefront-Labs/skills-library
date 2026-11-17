---
id: creative-arts.design-for-form-and-experience.design-systems.applying-atomic-design-to-a-component-library
name: applying-atomic-design-to-a-component-library
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [atomic-design, atoms-molecules-organisms, atomic-design-hierarchy, component-hierarchy, brad-frost, component-taxonomy]
level: practitioner
status: draft
description: "Apply Brad Frost's atomic design to a component library: atoms, molecules, organisms, templates and pages, how to classify, and where the model is too rigid."
sources:
  - "Brad Frost, Atomic Design (atomicdesign.bradfrost.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Atomic design hierarchy

Brad Frost's atomic design describes a way of building interfaces as a hierarchy of five levels.

## The levels
1. **Atoms:** basic elements that cannot be broken down usefully: label, input, button, icon, colour, font.
2. **Molecules:** simple groups of atoms working together: a search field (label, input, button).
3. **Organisms:** relatively complex sections: a header with logo, navigation and search; a product card grid.
4. **Templates:** page-level layouts that place organisms and show content structure with placeholder content.
5. **Pages:** templates filled with real content, used to test the design in context (edge-case content too).

## Using it
- **Classify** components as a shared vocabulary; do not obsess over borderline cases (is a card a molecule or an organism?). Many teams combine the middle levels or use their own names (primitives, components, patterns).
- **Build bottom up, test top down:** make atoms from tokens (see `...design-systems.tokens-tiers-primitive-semantic-component`), compose upward, and check on pages with real content.
- **Reuse before creating:** before a new component, check whether existing atoms and molecules can compose it.
- **Organise in code and Figma** to match (folders or pages named by level, or by domain).
- **Document** each with usage and variants (see `...design-systems.writing-component-usage-guidelines`).

## Limits
The model is a mental model, not a rule. Patterns that cross levels, layout primitives and behaviour-heavy components fit awkwardly; adapt the labels to your team.

## Verify
- [ ] Each component has a stated level and the parts it is built from.
- [ ] No organism duplicates a molecule's markup.
- [ ] Pages test real content including long and empty cases.
