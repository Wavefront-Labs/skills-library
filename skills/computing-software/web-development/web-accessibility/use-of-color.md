---
id: computing-software.web-development.web-accessibility.use-of-color
name: use-of-color
category: computing-software
field: web-development
product: web-accessibility
tags: [distinguishable, use-of-color, wcag-1-4-1, links, charts, forms]
level: practitioner
status: verified
description: "Meeting WCAG 1.4.1 Use of Color: links distinguishable from text, form errors, status indicators and charts that don't rely on colour alone, with fixes and tests."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
  - https://www.w3.org/WAI/WCAG22/Techniques/general/G183
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F73
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use of colour

**1.4.1 (A):** colour isn't the only visual means of conveying information, indicating an action, prompting a response, or distinguishing an element. About 1 in 12 men (8%) and 1 in 200 women have a colour-vision deficiency (Colour Blind Awareness).

## 1. Inline links
Links in body text must be distinguishable without colour: keep the **underline** (best). If removing underlines, the link colour needs 3:1 contrast against surrounding text **and** a non-colour cue on hover and focus (technique G183) - in practice just underline.
```css
.prose a { text-decoration: underline; text-underline-offset: .15em; text-decoration-thickness: from-font; }
```
Navigation menus and buttons are recognisable by position/shape and are exempt from this specific technique.

## 2. Forms
- Errors: red border alone fails. Add an icon + error text ("Enter a valid email") linked with `aria-describedby`, and `aria-invalid="true"`.
- Required fields: asterisk/"(required)" text, not just a coloured label.

## 3. Status and data
- Status pills: text label ("Failed", "Passed") or distinct icons, not just red/green dots.
- Charts: direct labels, patterns/textures, different marker shapes, or line styles; legends ordered like the data.
- Calendars/availability: hatching or text for "booked" days.
- Diffs: `+`/`-` markers or `<ins>`/`<del>`.

## 4. Selected/current states
Tabs, filters, toggles: add a border, weight change, check icon or underline, plus programmatic state (`aria-selected`, `aria-pressed`, `aria-current`).

## 5. Not covered here
Contrast levels themselves are 1.4.3/1.4.11; 1.4.1 is about colour being the *only* cue.

## Verify
DevTools > Rendering > Emulate vision deficiencies (achromatopsia, deuteranopia, protanopia) and grayscale: every link, error, state and chart series remains identifiable.
