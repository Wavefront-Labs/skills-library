---
id: computing-software.ux-hci-design.wcag-accessibility.media-player-accessibility
name: media-player-accessibility
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [autoplay-audio-control]
level: practitioner
status: docs-checked
description: "Autoplay audio rule (WCAG 1.4.2): pause/stop or independent volume control for audio longer than 3 seconds."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoplay audio (SC 1.4.2, Level A)
- If audio on a page plays automatically for more than 3 seconds, provide either a way to pause or stop it, or a way to control its volume independently of the overall system volume.
- Muting the system volume does not count as pausing or stopping; both mechanisms must be independent of system volume.
- Best: start sound only on user request (G171), or put a control near the beginning of the page that turns off sound (G170); a sound that turns itself off within three seconds also passes (G60).
- Audio that starts as a direct result of an intentional user action (a clearly labelled play button) is not "plays automatically".
- Failures: a sound longer than 3 seconds with no way to turn it off (F23); an autoplaying HTML5 media element with no way to pause or stop it (F93).

## Verify
- [ ] Load the page with sound on: any audio that starts by itself can be paused, stopped or turned down independently of the system volume.

## Checked

- Date: 2026-11-09.
- Read Understanding SC 1.4.2 Audio Control (Level A) in full: the 3 second threshold, pause/stop or independent volume, muting not counting, sufficient techniques G60/G170/G171 and failures F23/F93.
- Removed: keyboard, focus, label, caption-toggle, speed-control and keyboard-trap requirements for players (not stated on the cited page). The skill is narrowed to autoplay audio.

Method: documentation only; no commands were run.
