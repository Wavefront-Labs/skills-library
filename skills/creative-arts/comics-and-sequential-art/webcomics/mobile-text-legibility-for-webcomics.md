---
id: creative-arts.comics-and-sequential-art.webcomics.mobile-text-legibility-for-webcomics
name: mobile-text-legibility-for-webcomics
category: creative-arts
field: comics-and-sequential-art
product: webcomics
tags: [webcomics, webcomic-formats, screen-formats, mobile-legibility, lettering-size, font-size, contrast]
level: practitioner
status: draft
description: "Make webcomic lettering readable on phones: minimum font sizes per canvas width, balloon spacing, contrast, font choice, testing at device size and accessibility."
sources:
  - https://www.webtoons.com/en/creators101/webtoon-canvas
  - https://blambot.com/pages/comic-book-grammar-tradition
  - https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile text legibility

Most webcomic readers are on phones; a 800 px WEBTOON canvas is displayed at roughly 360-430 CSS px wide,
so text shrinks to about half its canvas size.

## Size rules of thumb
- WEBTOON-style 800 px-wide canvas: dialogue at roughly 22-30 px font size on the canvas, never smaller
  than ~20 px; captions similar; SFX larger.
- Working at 1600 px (2x)? Double those numbers.
- For page-format comics: test the exported web image on a phone; if you have to zoom, the text is
  too small.

## Layout
- Short lines (3-6 words), 2-4 lines per balloon; split long speeches into multiple balloons placed
  down the scroll.
- Generous padding inside balloons; leading about 110-120% of the font size.
- Balloons placed over flat or simple areas, not detailed art.
- Leave space between balloons so the reading order is obvious while scrolling.

## Fonts and contrast
- Comic lettering fonts designed for screens (clear open counters); avoid thin script fonts for dialogue.
- Mixed case is often more legible on screen than all caps for long text; choose one and be consistent.
- Dark text on white balloons; for coloured captions keep a contrast ratio of at least 4.5:1 (WCAG AA).

## Testing
- View the actual export on the smallest phone you can find, at normal reading distance.
- Use the platform preview (WEBTOON CANVAS has a mobile preview) before publishing.

## Gotchas
- Text added at the end in a separate pass is often undersized; letter early at final scale.
- Image compression blurs small anti-aliased text.

## Verify
- [ ] Every balloon readable on a small phone without zoom.
- [ ] Contrast checker passes for coloured captions.
