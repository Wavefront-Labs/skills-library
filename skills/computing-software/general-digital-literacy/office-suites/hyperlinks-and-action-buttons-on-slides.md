---
id: computing-software.general-digital-literacy.office-suites.hyperlinks-and-action-buttons-on-slides
name: hyperlinks-and-action-buttons-on-slides
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, pres-content, action-buttons, slide-hyperlinks, interactive-presentation]
level: intro
status: docs-checked
description: "Link slide objects to other slides, websites or files, add action buttons for kiosk-style or non-linear decks, and test that links work in Slide Show."
sources:
  - https://support.microsoft.com/en-us/powerpoint/add-commands-to-your-presentation-with-action-buttons
  - https://support.microsoft.com/en-us/accessibility/powerpoint/use-keyboard-shortcuts-to-create-powerpoint-presentations
  - https://support.microsoft.com/en-us/accessibility/powerpoint/use-keyboard-shortcuts-to-deliver-powerpoint-presentations
  - https://support.microsoft.com/en-us/powerpoint/use-zoom-for-powerpoint-to-bring-your-presentation-to-life
  - https://support.microsoft.com/en-us/powerpoint/training/create-a-self-running-presentation
  - https://support.google.com/docs/answer/1696717
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/orgchart.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hyperlinks and action buttons on slides

## Link any object (PowerPoint)
- Select text, a shape or picture and press **Ctrl+K** (insert a hyperlink).
- **Insert > Action** opens Action Settings: on the *Mouse Click* or *Mouse Over* tab choose
  *Hyperlink to* (next, previous or last slide, another presentation, a web page, or *Other File*),
  *Run program*, *Run macro* (needs a macro-enabled show), or tick *Play sound*.

## Action buttons
- **Insert > Shapes**, then a shape under **Action Buttons** at the bottom of the gallery.
- Drag to draw it; the Action Settings dialog opens so you can assign the action.

## Zoom for non-linear decks
- **Insert > Zoom > Summary Zoom / Slide Zoom / Section Zoom** makes clickable thumbnails that jump to
  slides or sections; the Zoom tab's *Return to Zoom* option brings you back.

## Kiosk use
- **Slide Show > Set Up Slide Show > Browsed at a kiosk (full screen)** loops until Esc. Add slide
  timings or navigation links, or the show will not advance past the first slide.

## Google Slides and Impress
- Google Slides: select the object and press **Ctrl+K** (insert or edit link).
- Impress: select the object › Slide Show › **Interaction** to make it go to another slide when clicked.

## Gotchas
- During a PowerPoint show, **Tab** moves to the next hotspot (links, triggers, media) and **Enter**
  opens the selected link, which helps when the mouse is awkward.

## Verify
- [ ] Slide Show › From Current Slide (or run from the start) and click every link and button once.

## Checked
2026-10-27, against Microsoft Support (PowerPoint for Microsoft 365 and 2016-2024: action buttons, create and deliver keyboard shortcuts, Zoom for PowerPoint, self-running presentations), Google's Slides keyboard shortcuts page and the LibreOffice help master branch (Impress flowchart/interaction guide). Confirmed: Ctrl+K, the Action Settings options, Action Buttons location in Shapes, Zoom types and Return to Zoom, kiosk looping and the need for timings or links, Tab/Enter hotspot keys, Google Ctrl+K, and Impress Slide Show › Interaction. Removed an unconfirmed list of button names and claims about Normal-view clicks and PDF export.
Method: documentation only; no commands were run.
