---
id: computing-software.general-digital-literacy.office-suites.rehearse-timings-and-record-slideshow
name: rehearse-timings-and-record-slideshow
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slideshow, rehearse-timings, record-slideshow, speaker-coach, kiosk-mode, auto-advance, narration]
level: intro
status: docs-checked
description: "Rehearse with timings and Speaker Coach, record narration and video over slides, and set up self-running (kiosk) presentations in PowerPoint and Impress."
sources:
  - https://support.microsoft.com/en-us/powerpoint/training/create-a-self-running-presentation
  - https://support.microsoft.com/en-us/powerpoint/rehearse-your-slide-show-with-speaker-coach
  - https://support.microsoft.com/en-us/powerpoint/training/record-a-slide-show-with-narration-and-slide-timings
  - https://support.microsoft.com/en-us/powerpoint/turn-your-presentation-into-a-video
  - https://support.google.com/docs/answer/1696787
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/rehearse_timings.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/show.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rehearse timings and record a slideshow

**Goal:** know your talk fits the slot, or produce a self-running narrated deck.

## Rehearse
- **PowerPoint:** Slide Show › **Rehearse Timings**: the Rehearsal toolbar times each slide (Next, Pause,
  Slide Time, Repeat). At the end it shows the total and asks whether to keep the timings; Slide Sorter
  then shows each slide's time.
- **Rehearse with Coach / Speaker Coach** (Microsoft 365; Windows, Mac, web, mobile): gives feedback on pacing,
  filler words, inclusive language and reading the slide text, then a Rehearsal Report. It is for practice
  only and adds no timings. English only; needs a microphone and internet.
- **Impress:** switch to Slide Sorter and start the show with the **Rehearse Timings** icon; click the timer to
  advance.
- Google Slides: Slideshow › Options › *Auto advance options* sets a fixed advance speed.

## Record narration
PowerPoint for Microsoft 365: the **Record** tab (or the Record button) opens the recording view with camera,
microphone, teleprompter (your notes) and pens; record per slide, then **Export › Export Video**. Classic:
Slide Show › Record Slide Show records voice, ink, laser pointer and timings, re-recording a slide replaces
its narration; then File › Export › Create a Video.

## Self-running (kiosk)
PowerPoint: Slide Show › Set Up Slide Show › *Browsed at a kiosk (full screen)* loops until Esc and needs
saved timings or navigation links. Per slide: Transitions › Advance Slide › *After* (seconds).
Impress: Slide Transition deck › Advance Slide › *After*, Apply Transition to All Slides; Slide Show › Slide Show
Settings › *Loop and repeat after*.

## Gotchas
- Leftover rehearsal timings make a live show advance on its own: Slide Show › clear **Use Timings** (or
  use Clear › timings) before presenting live.
- Record with a headset mic in a quiet room; Microsoft recommends a quiet place for rehearsal too.

## Verify
- [ ] Total rehearsal time leaves a comfortable margin inside your slot.

## Checked
2026-10-27, against Microsoft Support (Create a self-running presentation; Speaker Coach; Record a slide show with narration and slide timings; Turn your presentation into a video; Microsoft 365 and 2016-2024), Google Docs Editors Help (Present slides) and the LibreOffice help master branch (Rehearse timings; Showing a slide show). Confirmed: Rehearse Timings toolbar and prompt, Speaker Coach feedback, platforms, English-only and no-timings notes, the new Record tab and Export Video, classic Record Slide Show behaviour, kiosk looping, Advance Slide After, Use Timings and Clear, Google auto-advance, and Impress rehearse/loop settings. Removed an unconfirmed minutes-per-slide rule.
Method: documentation only; no commands were run.
