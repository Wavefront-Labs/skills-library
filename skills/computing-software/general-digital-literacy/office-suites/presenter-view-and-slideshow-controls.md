---
id: computing-software.general-digital-literacy.office-suites.presenter-view-and-slideshow-controls
name: presenter-view-and-slideshow-controls
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slideshow, presenting, presenter-view, slideshow-shortcuts, black-screen, laser-pointer, duplicate-vs-extend, second-monitor]
level: intro
status: docs-checked
description: "Present with Presenter View on two screens, use slideshow shortcuts (jump to slide, black screen, pointer, pen), and set up extend vs duplicate displays."
sources:
  - https://support.microsoft.com/en-us/powerpoint/training/start-the-presentation-and-see-your-notes-in-presenter-view
  - https://support.microsoft.com/en-us/accessibility/powerpoint/use-keyboard-shortcuts-to-deliver-powerpoint-presentations
  - https://support.microsoft.com/en-us/windows/how-to-use-multiple-monitors-in-windows-329c6962-5a4d-b481-7baa-bec9671f728a
  - https://support.microsoft.com/en-us/teams/meetings/share-slides-in-microsoft-teams-meetings-with-powerpoint-live
  - https://support.google.com/docs/answer/1696787
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/04/01020000.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/presenter_console.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Presenter View and slideshow controls

**Goal:** run a presentation smoothly, seeing your notes while the audience sees the slides.

## Start
| | From beginning | From current slide | Presenter View |
|---|---|---|---|
| PowerPoint (Windows) | `F5` | `Shift+F5` | `Alt+F5` (works on one screen for practice) |
| PowerPoint (Mac) | `⌘+Shift+Return` | `⌘+Return` | `Option+Return` |
| Google Slides | Mac `⌘+Shift+Enter`; or Slideshow drop-down › Presentation display options › Present from beginning | `Ctrl+F5` / **Slideshow** | Slideshow drop-down › Presenter view |
| Impress | `F5` | `Shift+F5` | Presenter Console starts with a second display |

## Displays
Windows `Win+P` › **Extend** so the projector shows slides and the laptop shows Presenter View
(Duplicate shows the same on both, so no private notes). Mac: turn off mirroring in Displays settings
(Microsoft's steps: Displays › Arrangement › clear *Mirror Displays*). PowerPoint: Slide Show tab › tick
*Use Presenter View* and choose the monitor; in Presenter View use **Display Settings › Swap Presenter
View and Slide Show** if they're backwards. Impress: Slide Show › Slide Show Settings › *Presenter console*;
the console's **Exchange** button swaps screens. Google Slides (Chrome): Slideshow drop-down ›
*Presentation display options* to pick the monitor.

## Controls during the show
| Key | PowerPoint (Windows) | Google Slides | Impress |
|---|---|---|---|
| next / previous | `N`, `Space`, `→` / `P`, `←` | `→` / `←` | `Space`, `→` / `←` |
| jump to slide | number + `Enter` | number + `Enter` | number + `Enter` |
| black / white screen | `B` / `W` | `b` / `w` | `B` / `W` |
| laser pointer | `Ctrl+L` | `l` | |
| pen / erase ink | `Ctrl+P` / `E` | pen via Options | `P` / `E` |
| all slides | `Ctrl+S` | | |
| end show | `Esc` | `Esc` | `Esc` |

PowerPoint Presenter View also shows the elapsed time, the next slide, *See all slides* and *Zoom into
slide* for detail. Google's `s` opens speaker notes during a show.

## Gotchas
- Turn on Do Not Disturb so chat pop-ups don't appear on the projected screen.
- Sharing in Teams: share the **PowerPoint window**, or use PowerPoint Live, which shows your notes next to the
  slides only to you.

## Verify
- [ ] Before the audience arrives, the projector shows slides and you see notes plus timer.

## Checked
2026-10-27, against Microsoft Support (Presenter view; delivery keyboard shortcuts for Windows, Mac and web; multiple monitors in Windows; PowerPoint Live in Teams), Google Docs Editors Help (Present slides) and the LibreOffice help master branch (Impress shortcut keys; Presenter Console). Confirmed: start shortcuts per app and OS, Alt+F5, Win+P display modes, Use Presenter View and Swap, Impress presenter console and Exchange, Google presentation display options, and the in-show key table. Corrected "G" for slide overview to Ctrl+S (All Slides) and the Google from-beginning shortcut, which Google does not list for Windows.
Method: documentation only; no commands were run.
