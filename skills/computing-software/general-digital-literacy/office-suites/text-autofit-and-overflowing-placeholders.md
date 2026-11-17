---
id: computing-software.general-digital-literacy.office-suites.text-autofit-and-overflowing-placeholders
name: text-autofit-and-overflowing-placeholders
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, slide-content, text-autofit, shrink-text-on-overflow, placeholder-overflow, text-box-options]
level: intro
status: docs-checked
description: "Control how PowerPoint and Google Slides handle text that overflows a placeholder: shrink on overflow, resize shape, split across slides, or stop autofit."
sources:
  - https://support.microsoft.com/en-us/powerpoint/split-body-text-between-two-slides
  - https://support.microsoft.com/en-us/office/graphics-visuals/format-object-text-box-pane
  - https://support.google.com/docs/answer/10364036
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Text autofit and overflowing placeholders

## PowerPoint (desktop)
When text starts to overfill a placeholder, the **AutoFit Options** button appears at its lower-left corner:
- **AutoFit Text to Placeholder** shrinks the text to fit (the default).
- **Stop Fitting Text to This Placeholder** lets it overflow.
- **Split Text Between Two Slides** (new slide with the same title, text divided roughly in half).
- **Continue on a New Slide** (new slide with the same title; keep typing there) or **Change to Two Columns**.
These options appear only on placeholders, not on text boxes you draw. PowerPoint for the web doesn't split
text automatically; cut and paste instead.
For a shape or text box: Format Shape › text box options › AutoFit: *Do not AutoFit*, *Shrink text on
overflow*, *Resize shape to fit text*; the same pane sets internal margins.

## Google Slides
Select the box › **Format › Format options › Text fitting** (or right-click › Text fitting): *Do not autofit*,
*Shrink text on overflow* (default for theme text placeholders), *Resize shape to fit text* (default for text
boxes). Tools › Preferences › *Use custom autofit preferences* changes the defaults.

## The real fix
Shrinking text makes slides hard to read. If text overflows: cut words, split into two slides, move detail
to speaker notes or a handout.

## Gotchas
- Autofit sizes differ slide to slide, so the deck looks inconsistent.
- New Google Slides text boxes resize to fit by default, so a long text box can grow off the slide.

## Verify
- [ ] Every body placeholder uses the same font size; no text crosses the slide edge in Slide Sorter.

## Checked
2026-10-27, against Microsoft Support (Split body text between two slides, PowerPoint for Microsoft 365 and 2019-2024; Format Object text box pane reference) and Google Docs Editors Help (Change how text fits in placeholders and text boxes). Confirmed: the AutoFit Options menu and its default, placeholder-only behaviour, no automatic split on the web, the AutoFit choices in the shape pane, Google Text fitting paths, options, defaults and custom preferences. Removed an unconfirmed global AutoCorrect setting, a font-size rule and a claim about PDF export.
Method: documentation only; no commands were run.
