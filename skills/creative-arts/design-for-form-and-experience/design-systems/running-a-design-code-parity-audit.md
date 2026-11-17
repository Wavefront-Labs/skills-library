---
id: creative-arts.design-for-form-and-experience.design-systems.running-a-design-code-parity-audit
name: running-a-design-code-parity-audit
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [parity-audit, design-code-parity, component-audit, figma-vs-code, drift, design-system-qa, interface-inventory]
level: practitioner
status: draft
description: "Run a design-code parity audit: compare Figma components with coded ones for anatomy, variants, states, tokens and accessibility, and log gaps with owners and fixes."
sources:
  - "Nathan Curtis (EightShapes), Design System Parity / Parity-checking (medium.com/eightshapes-llc)"
  - "Brad Frost, Atomic Design (atomicdesign.bradfrost.com)"
  - "Figma Dev Mode and Storybook docs for inspecting live components (help.figma.com, storybook.js.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design and code parity audit

**Goal:** the library in Figma and the coded library describe the same components, so designers and developers stop surprising each other.

## Scope
Pick components in priority order (most used first, by adoption data; `creative-arts.design-for-form-and-experience.design-systems.measuring-design-system-adoption`). Audit one at a time using the live Storybook and the published Figma component.

## Checklist per component
1. **Anatomy and naming:** same parts and names (Figma layer names and component property names vs code props and slots).
2. **Variants and props:** every Figma variant maps to a prop value and vice versa; boolean and instance-swap properties match (`creative-arts.design-for-form-and-experience.design-systems.connecting-figma-to-code-with-code-connect`).
3. **States:** default, hover, focus, pressed, disabled, loading, error present in both.
4. **Tokens:** colours, spacing, radius, type and motion use the same tokens; no raw values in either; compare computed values.
5. **Responsive behaviour and sizing** (hug/fill vs width rules).
6. **Content and truncation** behaviour.
7. **Accessibility:** focus ring, roles, keyboard, contrast, touch target in both representations; annotations present in Figma.
8. **Docs and status** consistent.

## Output
A matrix: component x checks with pass / drift / missing, severity, owner (design or engineering), and the fix. Screenshot pairs (Figma vs rendered) help. Create tickets for drifts, schedule fixes, and re-audit after release.

## Prevent drift
Single token source, Code Connect mappings, visual regression tests, changes landing in design and code in the same release, and a parity check in the contribution checklist.

## Verify
- [ ] Each audited component has a completed checklist and ticketed drifts.
- [ ] Drift trend (percent matching) tracked per release.
