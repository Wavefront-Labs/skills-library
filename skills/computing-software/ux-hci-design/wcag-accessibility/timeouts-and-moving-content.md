---
id: computing-software.ux-hci-design.wcag-accessibility.timeouts-and-moving-content
name: timeouts-and-moving-content
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [timing-adjustable, pause-stop-hide, wcag-enough-time]
level: practitioner
status: docs-checked
description: "Let users extend, disable or pause time limits and moving or auto-updating content (SC 2.2.1, 2.2.2)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html
  - https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 2.2.1 Timing Adjustable (A) and 2.2.2 Pause, Stop, Hide (A)
- 2.2.1: for a time limit set by the content, let the user turn it off, adjust it, or extend it. To allow extending, warn the user before time expires, give at least 20 seconds to respond with a simple action, and allow extending at least ten times.
- 2.2.1 exceptions: real-time events (such as an auction), essential time limits, and limits longer than 20 hours.
- 2.2.2: moving, blinking or scrolling content that starts automatically, lasts more than 5 seconds and is presented in parallel with other content needs a way to pause, stop or hide it, unless essential.
- 2.2.2: auto-updating information that starts automatically and is presented in parallel with other content needs a way to pause, stop or hide it, or to control the update frequency, unless essential.

## Verify
- [ ] Carousel has a pause button; session warning appears with extend option.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 2.2.1 Timing Adjustable and Understanding SC 2.2.2 Pause, Stop, Hide (both Level A): 20 seconds, ten times, 20 hours, 5 seconds, real-time (auction) and essential exceptions. Pages were searched for these claims rather than read line by line.
- Removed: the "tickers" example and the "user-controlled refresh" wording (replaced by the SC wording).

Method: documentation only; no commands were run.
