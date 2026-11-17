---
id: computing-software.web-development.frontend-development.system-font-stacks
name: system-font-stacks
category: computing-software
field: web-development
product: frontend-development
tags: [system-font-stack, system-ui, font-family, web-fonts, typography]
level: intro
status: docs-checked
description: "Using system font stacks for fast, native-looking text: system-ui and ui-* families, recommended stacks, emoji fallbacks, and system-ui pitfalls in some locales."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-family#generic-name
  - https://modernfontstacks.com/
  - https://github.com/system-fonts/modern-font-stacks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System font stacks

Zero download, zero layout shift, native feel. Good default for apps, dashboards and admin UIs.

## 1. Modern stacks
```css
:root {
  --font-sans: system-ui, sans-serif;
  --font-mono: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --font-rounded: ui-rounded, "Hiragino Maru Gothic ProN", Quicksand, Comfortaa, Manjari, "Arial Rounded MT", Calibri, sans-serif;
  --font-emoji: "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}
body { font-family: var(--font-sans), var(--font-emoji); }
code, pre, kbd { font-family: var(--font-mono); }
```
- `system-ui` is a CSS generic family meaning the platform's default user-interface font; it is supported on all modern operating systems.
- `ui-serif`, `ui-monospace` and `ui-rounded` are generic families too, but Modern Font Stacks notes SF Mono and SF Pro Rounded are reachable through them only in Safari on macOS 10.15+ and iOS 13.3+, hence the explicit fallback names.
- Modern Font Stacks (modernfontstacks.com) publishes vetted stacks by style, each listing which preinstalled fonts cover which operating systems.

## 2. Pitfalls
- Emoji: append the colour emoji fonts at the end of the stack, as Modern Font Stacks advises.
- Metrics differ per OS: line lengths and wrapping change. Use `ch`-based max-widths and test long labels on Windows and Android.

## 3. Mixing with a brand font
Use the brand font for headings only and the system stack for body text: one font file instead of four, and body text renders immediately.

## Verify
- [ ] Rendering checked on macOS, Windows, Android and one Linux distro; no font requests in the network panel for body text; emoji and code render with the intended fonts.

## Checked
2026-11-01. Confirmed against MDN font-family (system-ui, ui-serif, ui-monospace, ui-rounded generic names) and the Modern Font Stacks site and repository (system-ui note, monospace and rounded stacks, SF Mono and SF Pro Rounded availability, emoji font list). Removed: the per-OS system-ui mapping, the Windows-locale pitfall, the font-weight 500/600 claim, the digit-as-emoji claim, and the unverified serif and sans fallback lists.
Method: documentation only; no commands were run.
