---
id: computing-software.web-development.web-accessibility.accessible-media-player-and-autoplay
name: accessible-media-player-and-autoplay
category: computing-software
field: web-development
product: web-accessibility
tags: [time-based-media, accessible-media-player, autoplay-audio, wcag-1-4-2, wcag-2-2-2, audio-control, autoplay-policy]
level: practitioner
status: docs-checked
description: "Choosing and configuring accessible media players: keyboard-operable labelled controls, caption and description toggles, no autoplaying audio (1.4.2), and pausing motion."
sources:
  - https://www.w3.org/WAI/media/av/player/
  - https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html
  - https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
  - https://github.com/ableplayer/ableplayer
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Accessible media player and autoplay

## 1. Player requirements (W3C WAI media player checklist)
- All controls reachable and operable by keyboard with visible focus; logical tab order.
- Controls have accessible names and states ("Play"/"Pause" toggle, "Mute" pressed, volume slider with `aria-valuetext`).
- CC button for captions, selector for audio-described version/track, transcript link.
- Captions styleable or honour OS/browser caption preferences.
- Sufficient contrast between colours for text, controls and backgrounds.
- Don't hide controls permanently on autoplay "hero" videos.
Player support differs: Able Player supports captions, text-based description (including pausing the video for it), synchronized sign language and an interactive transcript; Video.js supports description only where the audio has space unless extended with a plug-in (W3C media guide). Check any player against the W3C checklist.

## 2. Autoplay rules
- 1.4.2 (A): audio that plays automatically for more than 3 seconds needs a mechanism to pause or stop it, or to control its volume independently of the system volume. Best: never autoplay sound.
- 2.2.2 (A): moving content (background/hero video) that starts automatically, lasts more than five seconds and is presented in parallel with other content needs a mechanism to pause, stop or hide it.
- Respect `prefers-reduced-motion`: don't autoplay decorative video; show the poster.
```html
<video autoplay muted loop playsinline poster="hero.jpg" id="hero"></video>
<button type="button" aria-pressed="false" id="hero-toggle">Pause background video</button>
<script>
if (matchMedia("(prefers-reduced-motion: reduce)").matches) hero.removeAttribute("autoplay");
</script>
```

## 3. Custom controls
- Use real `<button>`s, `<input type="range">` for seek/volume with `aria-label` and `aria-valuetext="1 minute 20 seconds of 4 minutes"`.
- Space/Enter on buttons; arrow keys on sliders (native range gives it).
- Don't capture global keyboard shortcuts that conflict with screen readers (single-key shortcuts need 2.1.4 handling).

## 4. Embeds
Give the iframe a `title` (axe rule `frame-title`).

## Verify
Operate the player keyboard-only and with a screen reader; load the page and confirm no sound plays; reduced-motion setting stops background video.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 1.4.2 and 2.2.2 text, W3C WAI media guide (player), Able Player README, axe-core 4.14 rule descriptions.
- Confirmed: 1.4.2 is Level A with a 3-second threshold; 2.2.2 is Level A with a five-second threshold and applies to content presented in parallel with other content; the W3C player checklist (keyboard support, visible focus, labels, contrast, caption display settings); Able Player and Video.js description support; the axe `frame-title` rule exists.
- Removed (no documentation found): "at the start of the page", the target-size item, the Plyr, Media Chrome and YouTube remarks and the `cc_load_policy` parameter.
Method: documentation only; no commands were run.