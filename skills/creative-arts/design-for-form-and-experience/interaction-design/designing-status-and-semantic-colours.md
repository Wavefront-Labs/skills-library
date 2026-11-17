---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-status-and-semantic-colours
name: designing-status-and-semantic-colours
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [status-colors, semantic-color, success-warning-error, alerts, ui-color, color-roles, accessibility]
level: practitioner
status: draft
description: "Design status and semantic colours: success, warning, error, info with tints for backgrounds, accessible contrast, and icon plus text so colour never carries meaning alone."
sources:
  - "WCAG 2.2 Success Criterion 1.4.1 Use of Color (w3.org/TR/WCAG22/#use-of-color)"
  - "Material Design 3 - Color roles (error, on-error, error-container) (m3.material.io/styles/color/roles)"
  - "Carbon Design System - Status indicators (carbondesignsystem.com/patterns/status-indicator-pattern)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Status and semantic colour

**Goal:** status colours that are consistent, accessible and not the only signal.

## Set
Four core statuses: **success** (green), **warning** (amber), **error/danger** (red), **info** (blue); plus neutral and optional "pending". Define each as a small ramp: a strong tone for icons, text and borders; a light tint for backgrounds; a dark tone for text on the tint.
- Example roles per status: `status-error-fg` (text/icon), `status-error-bg` (tint), `status-error-border`, `status-error-solid` (button fill).
- Warning amber needs dark text; white on yellow fails contrast.

## Accessibility rules
- **Never colour alone** (WCAG 1.4.1): pair with an icon, label or pattern. About 8 percent of men have red-green colour vision deficiency; success/error pairs in green/red are the worst offenders (`creative-arts.design-for-form-and-experience.interaction-design.designing-for-colour-vision-deficiency`).
- Contrast: text on tinted background at least **4.5:1**; icons and borders at least **3:1** (1.4.11).
- Test in greyscale and with a CVD simulator (Figma Stark, Color Oracle).

## Usage
- Same meaning everywhere: do not use red for a non-error emphasis.
- Reserve error red for errors and destructive actions; use neutral or brand for delete confirmations as appropriate.
- Define them as semantic tokens (`color.feedback.error`) referencing the palette so themes (dark mode) can remap (`creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale`).
- Keep message copy specific; colour supports it.

## Verify
- [ ] Each status has icon, text and colour; passes 4.5:1 / 3:1.
- [ ] Greyscale and CVD checks pass.
- [ ] Status tokens map correctly in light and dark themes.
