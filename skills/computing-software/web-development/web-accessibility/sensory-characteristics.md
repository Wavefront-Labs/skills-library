---
id: computing-software.web-development.web-accessibility.sensory-characteristics
name: sensory-characteristics
category: computing-software
field: web-development
product: web-accessibility
tags: [info-and-relationships, sensory-characteristics, wcag-1-3-3, instructions, content-design]
level: practitioner
status: docs-checked
description: "Writing instructions that don't rely only on shape, colour, size, position or sound (WCAG 1.3.3), with rewrite examples and checks for responsive and voice contexts."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/sensory-characteristics.html
  - https://www.w3.org/WAI/WCAG22/Techniques/general/G96
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F14
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensory characteristics

**1.3.3 (A):** instructions for understanding and operating content don't rely solely on sensory characteristics such as shape, colour, size, visual location, orientation or sound.

## 1. Rewrites
| Fails | Passes |
|---|---|
| "Click the round button to continue." | "Select **Continue** (the round button below)." |
| "See the sidebar on the right for details." | "See **Related documents** (in the sidebar) for details." |
| "Required fields are shown in red." | "Fields marked * (required) must be completed." plus `required` |
| "Press the green button to accept." | "Press **Accept**." |
| "The instructions above explain..." | "The **Before you start** section explains..." (linked) |
| "When you hear the beep, start speaking." | Add a visible "Recording now" indicator and text cue |
| "Use the arrow icon to expand." | "Use **Show more** to expand." (button has that name) |

## 2. Why it matters beyond screen readers
- Responsive layouts move "right sidebar" content below the main column on phones - positional words become false.
- Colour-blind users can't distinguish red vs green cues.
- Voice-control users need the control's visible name to say it.
- Screen magnifier users see a small part of the page; "above"/"below" may be off-screen.

## 3. Pattern
Reference the **visible label text** (which equals the accessible name) and optionally add the sensory hint as secondary information. Position words are fine as supplementary ("the Search box at the top of the page").

## 4. Audits
Search content and UI strings for: "click the", "red", "green", "left", "right", "above", "below", "round", "square", "icon", "beep", "sound". Common in onboarding tooltips, help articles, error messages and form hints.

## Verify
Read instructions with the screen off (or via screen reader) and on a phone layout: can you still identify the referenced control?

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 1.3.3 and techniques G96 and F14.
- Confirmed: 1.3.3 is Level A and covers shape, colour, size, visual location, orientation and sound; G96 (textual identification) and F14 (identifying content only by shape or location) exist as cited; position words are acceptable as supplementary information.
- Nothing was removed.
Method: documentation only; no commands were run.