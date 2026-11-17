---
id: computing-software.web-development.web-accessibility.context-sensitive-help
name: context-sensitive-help
category: computing-software
field: web-development
product: web-accessibility
tags: [context-sensitive-help, wcag-3-3-5, inline-help, form-guidance, toggletips]
level: practitioner
status: docs-checked
description: "Providing context-sensitive help (WCAG 3.3.5): inline hints, toggletips, examples and help links next to complex inputs, wired up with aria-describedby without clutter."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/help.html
  - https://inclusive-components.design/tooltips-toggletips/
  - https://design-system.service.gov.uk/components/details/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context-sensitive help (3.3.5)

3.3.5 (AAA): context-sensitive help is available where text input is required. Users with cognitive disabilities, unfamiliar with jargon, or using translation benefit most.

## 1. Choose the lightest pattern that works
| Need | Pattern |
|---|---|
| Format or constraint ("8+ characters", "DD MM YYYY") | Visible hint text under the label, always shown |
| Why we ask / where to find a value (tax number on a letter) | Expandable `<details>` under the field |
| Short definition of a term | Toggletip button next to the label |
| Long process guidance | Link to a help page that opens without losing form state (new tab with warning, or a side panel) |

## 2. Hint text
```html
<label for="nino">National Insurance number</label>
<p id="nino-hint" class="hint">It's on your payslip or P60. For example, 'QQ 12 34 56 C'.</p>
<input id="nino" name="nino" aria-describedby="nino-hint nino-error" autocomplete="off" spellcheck="false">
```
`aria-describedby` reads the hint after the label; order references hint then error. Don't put hints in `placeholder` (disappears on typing, low contrast).

## 3. Toggletip
```html
<span class="field-label">Routing number
  <button type="button" aria-label="What is a routing number?" aria-expanded="false" aria-controls="rt-tip">?</button></span>
<div id="rt-tip" role="status" hidden>The 9-digit number at the bottom left of a cheque.</div>
```
Click to open (not hover-only); Esc closes; content in a live region or placed right after the button so screen readers reach it.

## 4. Writing help
- Plain language, examples in the exact accepted format, explain *why* for sensitive data.
- Accept multiple formats rather than over-explaining one (strip spaces, allow dashes).
- Help content must be keyboard reachable and not time out.

## Verify
- [ ] Each non-obvious input has a visible hint, toggletip or details; hints announced with the field; help never requires hover or leaving the form and losing data.

## Checked
2026-10-28 Confirmed on W3C Understanding SC 3.3.5 Help (Level AAA): context-sensitive help is available. Toggletip pattern and GOV.UK Details component are on the fetched pages. Removed the SC 3.2.6 reference (page not fetched).
Method: documentation only; no commands were run.
