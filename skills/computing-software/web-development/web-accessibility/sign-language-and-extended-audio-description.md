---
id: computing-software.web-development.web-accessibility.sign-language-and-extended-audio-description
name: sign-language-and-extended-audio-description
category: computing-software
field: web-development
product: web-accessibility
tags: [sign-language-interpretation, extended-audio-description, wcag-1-2-6, wcag-1-2-7, aaa-media]
level: advanced
status: docs-checked
description: "Meeting the AAA media criteria: sign language interpretation (1.2.6), extended audio description (1.2.7), media alternatives (1.2.8), and production and player choices."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/sign-language-prerecorded.html
  - https://www.w3.org/WAI/WCAG22/Understanding/extended-audio-description-prerecorded.html
  - https://www.w3.org/WAI/media/av/sign-languages/
  - https://www.w3.org/WAI/media/av/description/
  - https://github.com/ableplayer/ableplayer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sign language and extended audio description (AAA)

Not required for AA conformance (1.2.6, 1.2.7 and 1.2.8 are all Level AAA). Relevant where sign language is the audience's first language and captions in a second language are not equivalent.

## 1. Sign language (1.2.6)
- Use qualified interpreters in the audience's sign language (ASL, BSL and Auslan are different languages).
- Production: a solid background and clothing that contrasts with the signer's skin tone, with all movements and facial expressions clearly visible.
- Delivery options:
  1. Burned-in picture-in-picture: simplest, always present.
  2. A separate signed version of the video, offered via a clearly labelled toggle.
  3. A synchronised second video in the player (e.g. Able Player's sign language window) that users can move and resize.
- Live events: show the interpreter on the main stream, not only in a meeting gallery tile that may be hidden.

## 2. Extended audio description (1.2.7)
When pauses in dialogue are too short to describe essential visuals, the video **pauses** while the description plays, then resumes.
- Implementation: a second rendition with frames held for descriptions, or player support for text descriptions (WebVTT `kind="descriptions"`) read by TTS with pausing (Able Player supports this).
- Write descriptions for what is needed to understand the content, not everything on screen.

## 3. Media alternative (1.2.8)
A full text alternative (descriptive transcript) including dialogue and visual information, for prerecorded media. Usually the cheapest AAA win, and useful for search and skim reading.

## 4. Prioritising
Ask the audience: Deaf users typically value sign language and good captions; blind users value audio description and descriptive transcripts. Start with the content that matters most (onboarding, legal rights, safety).

## Verify
- [ ] Signed version or overlay present and legible on mobile; extended descriptions pause video correctly; descriptive transcript linked next to the player.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 success criteria, W3C WAI media guide (sign languages, description, player), Able Player README.
- Confirmed: 1.2.6 Sign Language, 1.2.7 Extended Audio Description and 1.2.8 Media Alternative are Level AAA; sign languages differ by region (ASL, BSL, Auslan); background and clothing guidance; Able Player supports synchronized sign language and pausing for text-based description.
- Removed (no documentation found): the one-quarter video height figure, the Deaf-interpreter remark and the claim that these criteria are often required for public-sector audiences.
Method: documentation only; no commands were run.