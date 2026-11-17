---
id: computing-software.web-development.web-accessibility.pause-stop-hide-moving-content
name: pause-stop-hide-moving-content
category: computing-software
field: web-development
product: web-accessibility
tags: [enough-time, seizure-safety, pause-stop-hide, carousel-autoplay, wcag-2-2-2, auto-updating-content, marquee, background-video]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.2.2 Pause, Stop, Hide: pause controls for carousels, background video, animations and auto-updating feeds that move or update for over five seconds."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
  - https://www.w3.org/WAI/ARIA/apg/patterns/carousel/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pause, stop, hide moving content

**Goal:** moving, blinking, scrolling or auto-updating content can be stopped, so it doesn't distract users with attention disorders or make reading impossible.

## 1. The rule (2.2.2, A)
- Moving/blinking/scrolling content that starts automatically, lasts > 5 s, and is shown alongside other content -> a mechanism to **pause, stop or hide** it.
- Auto-updating content (news tickers, live scores, stock prices) that starts automatically and is presented with other content -> pause/stop/hide **or** control the update frequency.
- Exception: essential (a loading spinner during loading is fine).
Like 2.1.2, this criterion applies to all content on the page: the SC text says content that does not meet it can interfere with the use of the whole page.

## 2. Carousels
- Prefer no autoplay. If autoplay: visible Pause/Play button (first in the carousel's tab order), rotation stops on hover and when keyboard focus enters, and does not restart unless the user asks (APG).
- APG carousel pattern: `aria-roledescription="carousel"` on the container, slides `role="group" aria-roledescription="slide" aria-label="2 of 5"`, live region `aria-live="off"` while rotating and `polite` when paused (so manual navigation is announced).
- Respect `prefers-reduced-motion`: don't autoplay at all.

## 3. Background video and animations
- Autoplaying hero video: provide a pause button (and ideally a static poster for reduced motion); muted autoplay still counts as moving content.
- Lottie/CSS looped animations over 5 s: pause control or stop after 5 s (`animation-iteration-count` finite).
- Animated GIFs: use a `<video>` with controls or a click-to-play static image so there is a pause mechanism.

## 4. Auto-updating content
Live feeds: "Pause updates" toggle, or "N new items - show" button instead of inserting automatically (also prevents content jumping under the reader).

## Verify
- [ ] Every auto-moving element > 5 s has a keyboard-accessible pause/stop.
- [ ] Focus inside a carousel stops rotation.
- [ ] With reduced motion, nothing autoplays.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 2.2.2 Pause, Stop, Hide (Level A): moving, blinking or scrolling content that starts automatically, lasts more than five seconds and is presented in parallel with other content needs pause/stop/hide; auto-updating content needs pause/stop/hide or frequency control; the essential exception; and the whole-page interference note. APG carousel confirms the stop-on-focus/hover and no-restart behaviour. Removed the stop-permanently-on-interaction and GIF claims.

Method: documentation only; no commands were run.
