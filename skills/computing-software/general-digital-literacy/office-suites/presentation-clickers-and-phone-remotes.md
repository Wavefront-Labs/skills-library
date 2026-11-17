---
id: computing-software.general-digital-literacy.office-suites.presentation-clickers-and-phone-remotes
name: presentation-clickers-and-phone-remotes
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, pres-delivery, presentation-remote, clicker, presenter-view]
level: intro
status: docs-checked
description: "Advance slides with a USB clicker or your phone (PowerPoint mobile, Keynote Remote, Impress Remote), and fix a clicker that does nothing."
sources:
  - https://support.microsoft.com/en-us/accessibility/powerpoint/use-keyboard-shortcuts-to-deliver-powerpoint-presentations
  - https://support.microsoft.com/en-gb/office/present-a-slide-show-from-a-smartphone-and-use-a-laser-pointer-for-emphasis-485e8618-98ed-472b-84fa-443e23ea602a
  - https://support.apple.com/en-us/119886
  - https://support.google.com/docs/answer/1696787
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/impress_remote.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Presentation clickers and phone remotes

## USB or Bluetooth clicker
- A clicker works by sending key presses, so it only does something if the app understands those keys.
  PowerPoint advances on Page Down, Right/Down arrow, N, Enter or Space and goes back on Page Up,
  Left/Up arrow, P or Backspace. Google Slides' present shortcuts list the arrow keys.
- Blank-screen keys: in PowerPoint B (or .) shows black and W (or ,) white; press again to return.
  Google Slides also uses b and w.
- Physical lasers don't show for remote attendees; use the on-screen laser pointer instead (PowerPoint
  **Ctrl+L**, Mac ⌘+L; Google Slides **l**).

## Phone as remote
- **PowerPoint**: the PowerPoint mobile app can run the slide show from your phone, with a laser pointer
  that needs a Microsoft 365 subscription and a phone with a gyroscope; the phone screen reaches the
  projector by HDMI adapter or wireless display (AirPlay, Chromecast, Miracast).
- **Keynote**: turn on remotes in Keynote settings on the Mac, tap **Keynote Remote** in Keynote on the
  iPhone, then **Link** and match the four-digit code; newer devices connect over Wi-Fi when close by.
- **Impress**: install *Impress Remote* (The Document Foundation) on Android or iOS, pair by Bluetooth or
  the same network, then Slide Show › Slide Show Settings › **Enable remote control** and restart Impress.
  It shows slide thumbnails and speaker notes.

## When the clicker does nothing
1. Click once on the slide show window so it has focus (another app may have focus).
2. Fresh battery; plug the receiver straight into the laptop rather than a hub.
3. Check the receiver is working by pressing Page Down in any text editor.
4. Video calls: if you share a window, the presentation must be the active window for keys to reach it.

## Good practice
- Rehearse with the clicker; know which button goes back.
- Know the keyboard fallbacks (N/P, slide number + Enter to jump).

## Verify
- [ ] From the back of the room, forward, back and blank all work.

## Checked
2026-10-27, against Microsoft Support (PowerPoint delivery keyboard shortcuts for Windows and Mac; present from a smartphone with a laser pointer), Apple Support (Use Keynote Remote), Google Docs Editors Help (Present slides shortcuts) and the LibreOffice help master branch (Impress Remote guide). Confirmed: advance/back and black/white keys, laser pointer shortcuts, phone laser pointer requirements, Keynote Remote linking and Wi-Fi connection, and Impress Remote setup. Removed unconfirmed claims about PowerPoint pairing with a Windows PC over Bluetooth, a Google Slides phone-remote mode and laser colours.
Method: documentation only; no commands were run.
