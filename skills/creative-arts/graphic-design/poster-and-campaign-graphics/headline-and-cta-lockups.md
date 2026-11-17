---
id: creative-arts.graphic-design.poster-and-campaign-graphics.headline-and-cta-lockups
name: headline-and-cta-lockups
category: creative-arts
field: graphic-design
product: poster-and-campaign-graphics
tags: [graphic-design, poster-and-campaign-graphics, call-to-action, cta, headline-lockup, cta-button, campaign-copy, qr-code]
level: practitioner
status: draft
description: "Design headline plus call-to-action lockups: one clear verb, contrast and spacing for the action, print URL or QR rules, and consistency across formats."
sources:
  - https://help.figma.com/
  - https://www.w3.org/WAI/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Headline and CTA lockups

**Goal:** a reusable pairing of message and action that stays legible and well proportioned in every format of a campaign.

## 1. Write the pair
- **Headline:** the promise or hook, short.
- **CTA:** a specific verb plus outcome ("Book a tasting", "Get the guide"), not "Click here". One primary action per layout.

## 2. Hierarchy and spacing
- Headline largest; the CTA second-most prominent through contrast (filled button, or bold text on a solid ground), not size alone.
- Define the lockup as a unit with fixed proportions: space between headline and CTA, CTA padding, clear space around the group. Express spacing in a unit tied to type size (x-height or 0.5 em) so it scales.
- Keep CTA text to a few words; align it to the same axis as the headline.

## 3. Digital CTAs
- Touch targets: 44x44 px is a common platform guideline; WCAG 2.2 sets a 24x24 CSS px minimum at level AA. Give the button at least 3:1 contrast against its surroundings and 4.5:1 for its text.
- Do not communicate the action by colour alone.

## 4. Print CTAs
- Print cannot be clicked: provide a short URL, phone number or **QR code**. Keep a quiet zone around the QR code (four modules wide is the usual rule), high-contrast dark on light, and test scanning with at least two phones from the real reading distance using the printed proof.
- Prefer short, lower-case URLs or a vanity path; long case-sensitive URLs are error-prone in print.

## 5. Build once, reuse
Make the lockup a component (Figma component or Illustrator symbol) and resize variants from it; see `creative-arts.graphic-design.poster-and-campaign-graphics.campaign-adaptations-figma-auto-layout`.

## Failure modes
- Two competing CTAs of equal weight.
- CTA colour borrowed from the photo, low contrast.
- QR code too small or placed on a curved or glossy area.

## Self-check
Cover the headline: can you still see where to act? Test the QR code and URL from the printed proof.
