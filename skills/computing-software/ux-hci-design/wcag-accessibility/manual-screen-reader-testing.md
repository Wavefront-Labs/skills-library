---
id: computing-software.ux-hci-design.wcag-accessibility.manual-screen-reader-testing
name: manual-screen-reader-testing
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [screen-reader-testing, nvda-voiceover-testing]
level: practitioner
status: draft
description: "Smoke-test key journeys with NVDA, VoiceOver and TalkBack, with defined browser pairings."
sources:
  - https://www.w3.org/WAI/test-evaluate/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screen reader testing
- Common pairings: NVDA + Firefox/Chrome (Windows, free), JAWS + Chrome, VoiceOver + Safari (macOS/iOS), TalkBack + Chrome (Android).
- Test: headings and landmarks navigation, forms mode, dialogs, dynamic updates, tables, error messages.
- Learn core commands (e.g. NVDA Insert+F7 elements list; VoiceOver rotor).
- Record result per browser/AT pair in a matrix.

## Gotchas
- Behaviour differs by pairing; do not conclude from one.

## Verify
- [ ] Main journey completed with eyes closed on at least one screen reader.
