---
id: computing-software.web-development.web-accessibility.testing-with-disabled-users-and-assistive-tech
name: testing-with-disabled-users-and-assistive-tech
category: computing-software
field: web-development
product: web-accessibility
tags: [accessibility-testing, assistive-technology-testing, voice-control-testing, usability-testing, screen-magnifiers]
level: practitioner
status: docs-checked
description: "Testing with disabled participants and with assistive tech beyond screen readers: voice control, magnification, switch access, high contrast, and recruiting and running sessions."
sources:
  - https://www.w3.org/WAI/test-evaluate/involving-users/
  - https://www.w3.org/WAI/people-use-web/tools-techniques/
  - https://support.apple.com/guide/mac-help/use-voice-control-mchlb3d02b3e/mac
  - https://support.microsoft.com/en-us/windows/use-voice-access-to-control-your-pc-author-text-with-your-voice-4dcd23ee-f1b9-4fd1-bacc-862ab611f55d
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Testing with disabled users and assistive tech beyond screen readers

Conformance testing finds rule violations; real users find what's actually unusable.

## 1. Test with the AT yourself first
| AT | How to test | Common failures found |
|---|---|---|
| Voice control (macOS Voice Control, Windows Voice Access) | speak the visible label of each control | visible label differs from accessible name, unlabelled icon buttons, custom controls not exposed, hover-only menus |
| Screen magnification (screen magnifiers, built-in OS zoom) | navigate a flow zoomed in | content appearing far from trigger, toasts off-screen, tooltips that vanish, layout jumps |
| Browser zoom / text size | large zoom levels | reflow and clipping |
| High-contrast / forced colours modes | the OS high-contrast setting | invisible icons and focus rings, background-image-only buttons |
| Switch access (for example Apple Switch Control) | scanning through controls | too many tab stops, timeouts, drag-only interactions |
| Keyboard only | unplug mouse | traps, missing focus styles, unreachable controls |
| Reduced motion and reading tools | OS settings | animations ignoring preference, clipped text |
| Captions / no audio | mute | missing captions and transcripts |

## 2. Usability sessions with disabled participants
- Recruit through specialist agencies (for example specialist agencies or local disability organisations) - include a range: blind screen reader users (different expertise levels), low vision, deaf, motor, cognitive/learning disabilities.
- Let participants use **their own devices and settings** where possible.
- Pay participants fairly (allow for setup time); make consent forms, scheduling and the meeting tool accessible.
- Test prototypes early, not just before launch.
- Task-based: "Find and book an appointment for Tuesday" - observe, don't help; note workarounds.

## 3. Turn findings into fixes
Link each finding to the WCAG criterion if one applies, but keep usability issues that pass WCAG too. Share video clips (with consent) - they change team priorities faster than reports.

## Verify
Each release cycle includes at least one AT pass beyond screen readers; findings tracked to closure; research rounds scheduled regularly with disabled participants.

## Checked
2026-10-28 Removed unsourced figures and names: participant count, magnification factor, zoom range, the named recruitment agencies, payment-rate wording and WCAG numbers not on fetched pages. Confirmed on the W3C involving-users and tools-techniques pages and the Apple and Microsoft help pages: Voice Control, Voice Access, screen magnifiers, Switch Control, recruiting and compensating participants. Also removed the Show numbers and Show grid commands, ZoomText, Dragon, Android Switch Access, forced-colors emulation and reader-tool names (not on the fetched pages).
Method: documentation only; no commands were run.
