---
id: computing-software.ux-hci-design.design-systems.accessible-component-specs
name: accessible-component-specs
category: computing-software
field: ux-hci-design
product: design-systems
tags: [a11y-annotations, component-a11y-spec, ds-a11y-in-systems]
level: practitioner
status: draft
description: "Annotate designs with focus order, roles, names, states and keyboard behaviour before development."
sources:
  - https://www.w3.org/WAI/ARIA/apg/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accessibility annotations
For each component and flow specify: accessible name source, role, states, keyboard interaction (APG model), focus order and focus return, live announcements, contrast pairs, target sizes, reduced-motion behaviour, error and help text association.
Annotate in Figma using a11y annotation kits; add to the definition of done.

## Verify
- [ ] QA tests each annotated behaviour with keyboard and screen reader.
