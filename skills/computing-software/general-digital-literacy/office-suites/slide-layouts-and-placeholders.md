---
id: computing-software.general-digital-literacy.office-suites.slide-layouts-and-placeholders
name: slide-layouts-and-placeholders
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slides, slide-layouts, placeholders, new-slide, reset-slide, title-and-content, google-slides, impress]
level: intro
status: docs-checked
description: "Choose and change slide layouts, use placeholders instead of loose text boxes and reset a slide to its layout in PowerPoint, Google Slides and Impress."
sources:
  - https://support.microsoft.com/en-us/powerpoint/what-is-a-slide-layout
  - https://support.microsoft.com/en-us/powerpoint/edit-and-re-apply-a-slide-layout
  - https://support.microsoft.com/en-us/accessibility/powerpoint/use-keyboard-shortcuts-to-create-powerpoint-presentations
  - https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities
  - https://support.microsoft.com/en-us/powerpoint/create-and-print-a-presentation-in-outline-view
  - https://support.google.com/docs/answer/1694830
  - https://support.google.com/docs/answer/1705254
  - https://support.google.com/docs/answer/1696717
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/00/slide_menu.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slide layouts and placeholders

**Goal:** slides that are consistent and easy to restyle, built from layouts.

## New slide with a layout
- **PowerPoint:** Home › **New Slide** drop-down › pick a layout; `Ctrl+M` adds a new slide.
- **Google Slides:** **New slide** (`Ctrl+M`) adds one with the current layout; **New slide with layout**
  lets you pick.
- **Impress:** Slide › New Slide (`Ctrl+M`), then Slide › Layout.

## Change an existing slide
PowerPoint: Home › **Layout**. Google Slides: **Layout** on the toolbar. Impress: Slide › Layout.

## Placeholders vs text boxes
Placeholders are the dotted containers that come from the layout: they carry the theme's fonts, colours and
positions, and their titles and main text appear in Outline view. Use placeholders for titles and main
content rather than text boxes you draw yourself.

## Reset
Moved things around and it looks messy? PowerPoint Home › Slides group › **Reset** restores the slide's
placeholders and returns fonts, colours and effects to the template; your content stays.

## Gotchas
- Give every slide a unique title; people using screen readers navigate by slide titles. A title can sit off
  the slide if you need the space.
- After editing a layout in Slide Master, re-apply it (Home › Layout) to slides that already use it.

## Verify
- [ ] The Outline view shows every slide's title and bullets.

## Checked
2026-10-27, against Microsoft Support (What is a slide layout; Edit and re-apply a slide layout; create keyboard shortcuts; accessibility guide; Outline view; PowerPoint for Microsoft 365 and 2016-2024), Google Docs Editors Help (organize slides; layouts; keyboard shortcuts) and the LibreOffice help master branch (Slide menu). Confirmed: New Slide and Ctrl+M in all three apps, Google New slide with layout and the toolbar Layout button, Impress Slide › Layout, Home › Layout, placeholder definition, Reset behaviour, unique slide titles and off-slide titles, and re-applying edited layouts. Corrected the Google path "Slide › Apply layout" to the toolbar Layout button.
Method: documentation only; no commands were run.
