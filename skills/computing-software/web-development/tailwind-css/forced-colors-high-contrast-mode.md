---
id: computing-software.web-development.tailwind-css.forced-colors-high-contrast-mode
name: forced-colors-high-contrast-mode
category: computing-software
field: web-development
product: tailwind-css
tags: [css-color, forced-colors, windows-high-contrast, system-colors, forced-color-adjust, high-contrast-mode, contrast-themes]
level: practitioner
status: docs-checked
description: "Supporting Windows contrast themes via forced-colors: what the browser overrides, system colour keywords, restoring lost borders/focus/icons and testing in emulation."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors
  - https://developer.mozilla.org/en-US/docs/Web/CSS/system-color
  - https://blogs.windows.com/msedgedev/2020/09/17/styling-for-windows-high-contrast-with-new-standards-for-forced-colors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forced-colors (Windows contrast themes)

**Goal:** the UI stays usable when users force a high-contrast palette.

## 1. What the browser does in forced colours
Overrides `color`, `background-color`, `border-color`, `outline-color`, `fill`/`stroke` (for some SVG), `text-decoration-color`, `column-rule-color` with the user's system colours; **removes `box-shadow` and `text-shadow`**, and background images behind text get a backplate. `background-image` gradients are removed in some cases.

## 2. Common breakages
| Problem | Fix |
|---|---|
| Buttons/cards defined only by background colour lose their shape | Add `border: 1px solid transparent` (becomes visible in forced colours) |
| Focus ring made with box-shadow disappears | Use `outline` (or add `outline: 2px solid transparent` alongside the box-shadow) |
| Custom checkboxes/toggles invisible | Use system colours inside `@media (forced-colors: active)` |
| Icon fonts / SVG with hard-coded fills vanish | `fill: currentColor`; for important images `forced-color-adjust: none` only on that element |
| Selected state shown by colour only | Add a border/underline/icon change |

```css
@media (forced-colors: active) {
  .toggle[aria-checked="true"] .knob { background: Highlight; }
  .toggle { border: 1px solid ButtonText; }
  .badge { border: 1px solid CanvasText; }
}
```
System colour keywords: `Canvas`, `CanvasText`, `LinkText`, `VisitedText`, `ButtonFace`, `ButtonText`, `ButtonBorder`, `Highlight`, `HighlightText`, `GrayText`, `Field`, `FieldText`, `AccentColor`.

## 3. forced-color-adjust
`forced-color-adjust: none` opts an element out (keeps your colours) - use sparingly for things like colour swatches or brand logos where the actual colour is the content. Never on whole components.

## 4. Test
- Real: turn on a Windows contrast theme (Settings > Accessibility > Contrast themes) and test in your target browsers.
- Emulation: browser DevTools can emulate the `forced-colors: active` media feature.

## Verify
- [ ] All controls have visible boundaries and states in at least one light and one dark contrast theme.
- [ ] Focus indicator visible everywhere.
- [ ] Icons conveying meaning remain visible.

## Checked
2026-10-28 Confirmed on MDN (forced-colors, system-color) and the Microsoft Edge blog: box-shadow and text-shadow forced to none, text backplates, forced-color-adjust, the system colour keyword list including AccentColor. Removed: the unsourced share-of-users claim and the named Windows theme list. DevTools emulation is stated generically.
Method: documentation only; no commands were run.
