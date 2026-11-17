---
id: creative-arts.design-for-form-and-experience.interaction-design.applying-progressive-disclosure
name: applying-progressive-disclosure
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [progressive-disclosure, staged-disclosure, information-hierarchy, advanced-options, complexity-management, onboarding, accordion]
level: practitioner
status: draft
description: "Apply progressive disclosure: show core options first and reveal advanced ones on demand with clear triggers, staged flows, accordions and defaults, avoiding hidden essentials."
sources:
  - "Nielsen Norman Group - Progressive Disclosure (nngroup.com/articles/progressive-disclosure)"
  - "Jared Spool, Progressive Disclosure in User Interfaces (uie.com)"
  - "Interaction Design Foundation - Progressive Disclosure (interaction-design.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Progressive disclosure

**Goal:** reduce initial complexity while keeping power available.

## Patterns
- **Staged disclosure:** a wizard, or a series of questions where each reveals the next (`creative-arts.design-for-form-and-experience.interaction-design.building-multi-step-forms`).
- **Expand on demand:** accordions, "Show more", "Advanced options" toggles, details/summary, row expanders in tables.
- **Contextual reveal:** controls appear on hover or selection (a toolbar for selected text), always with a touch and keyboard alternative.
- **Conditional fields:** show fields only when relevant to previous answers.
- **Tiered help:** hint, then tooltip, then link to docs.

## Design rules
1. **Prioritise by frequency and importance:** 80 percent of users need 20 percent of features; surface those. Use research or analytics to decide.
2. **Make the trigger clear:** labelled, "Advanced settings" with a chevron, not an unlabelled icon; keep position stable.
3. **Keep the disclosed content close** to its trigger; avoid jumping context.
4. **Maintain state:** remember expansion; keep disclosed values visible in summaries.
5. **Limit levels** to two or three; deeper hides things.
6. **Never hide essentials** (required fields, critical warnings, price components).
7. **Accessibility:** `aria-expanded`, `aria-controls`, buttons (not divs), keyboard toggle; announce changes.
8. **Search** helps experts reach buried features.

## Test
Check that key tasks do not require unfound disclosures (first-click, task tests); monitor usage of advanced controls.

## Verify
- [ ] Core tasks need no disclosure; advanced options are findable.
- [ ] Triggers labelled; state preserved; keyboard and ARIA correct.
