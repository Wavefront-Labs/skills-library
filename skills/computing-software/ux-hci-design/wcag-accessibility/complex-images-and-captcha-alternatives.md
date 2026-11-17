---
id: computing-software.ux-hci-design.wcag-accessibility.complex-images-and-captcha-alternatives
name: complex-images-and-captcha-alternatives
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [complex-image-description, captcha-alternatives]
level: practitioner
status: docs-checked
description: "Give complex non-text content text alternatives and provide CAPTCHA alternatives for different senses (SC 1.1.1)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Complex non-text content
- Charts, diagrams, audio recordings, pictures and animations are non-text content that needs a text alternative serving the equivalent purpose (SC 1.1.1).
- CAPTCHA: a text alternative describes the purpose of the CAPTCHA, and alternative forms of CAPTCHA using different modalities (different types of sensory perception) are provided.
- The Working Group notes that every type of CAPTCHA will be unsolvable by users with certain disabilities. Ways to reduce the barrier: offer more than two modalities, let users reach a human customer service representative who can bypass the CAPTCHA, or do not require CAPTCHA for authorised users.

## Verify
- [ ] A user without sight of the image can get the same data.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 1.1.1 Non-text Content: CAPTCHA purpose text, alternative forms for different sensory perception, the Working Group note and listed approaches, and charts/diagrams needing text alternatives. The page was searched for these claims rather than read line by line.
- Removed: the adjacent data table or prose summary advice, the map advice, the advice to avoid puzzle CAPTCHAs and the `aria-describedby` tip (not stated on the page).

Method: documentation only; no commands were run.
