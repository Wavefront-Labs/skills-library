---
id: creative-arts.graphic-design.typography.letterspacing-capitals-and-small-caps
name: letterspacing-capitals-and-small-caps
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, kerning, tracking, letterspacing-caps, all-caps, tracking-values, css-letter-spacing, text-transform, labels, eyebrows]
level: intro
status: draft
description: "Letterspace all-caps and small-cap text so it breathes: typical tracking values, why not to track lowercase, trailing space, and CSS letter-spacing."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/letter-spacing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Letterspacing capitals and small caps

**Goal:** all-caps labels, headings and small caps that look even and open, not cramped.

## The rule
Capitals are designed to sit next to lowercase, so in strings of capitals the spacing looks tight and uneven.
Bringhurst: "letterspace all strings of capitals and small caps" - but not lowercase in text (lowercase letterspacing
damages word shapes; exceptions are deliberate display effects).

## Typical values
| Context | Tracking (Adobe, 1/1000 em) | CSS |
|---|---|---|
| All-caps text size labels, eyebrows, buttons | +50 to +100 | `letter-spacing: 0.05em-0.1em` |
| All-caps headings (large) | +20 to +50 (less at larger sizes) | `0.02em-0.05em` |
| Small caps in text | +50 to +80 | `0.05em-0.08em` |
| Very small caps text (< 8 pt / 12 px) | up to +100-150 | `0.1em-0.15em` |
Larger sizes need less; lighter weights tolerate more; condensed faces less.

## Setting
- **InDesign/Illustrator:** Character panel tracking; build it into the `Label` or `Small caps` character/paragraph
  style so it is consistent. Then kern problem pairs (see manual kerning).
- **CSS:** `text-transform: uppercase; letter-spacing: 0.08em;` - use em units so spacing scales with font size.
  Keep the source text in sentence case for accessibility (screen readers may spell out ALL-CAPS words) and copy-paste.

## Trailing space
Tracking adds space after the last letter too, so centred or right-aligned tracked text looks off-centre. In
InDesign, remove tracking from the last character; in CSS, compensate with `margin-right: -0.08em` (or padding on
the other side) on centred labels.

## Gotchas
- Turn off standard ligatures in tracked text (see ligatures skill).
- Word spacing should increase in proportion; heavily tracked lines can make word gaps look too small - add word spacing.
- Letterspacing lowercase body text to fit copy (copyfitting) is visible and amateurish - edit or resize instead.

## Verify
- [ ] All-caps and small-cap strings tracked by style; lowercase text not letterspaced.
- [ ] Centred tracked labels visually centred (trailing space handled).
