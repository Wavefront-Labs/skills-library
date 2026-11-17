---
id: creative-arts.graphic-design.poster-and-campaign-graphics.banner-ad-file-weight
name: banner-ad-file-weight
category: creative-arts
field: graphic-design
product: poster-and-campaign-graphics
tags: [graphic-design, poster-and-campaign-graphics, display-ads, banner-ads, ad-file-size, iab-standard-sizes, html5-banners, animated-gif, file-weight]
level: practitioner
status: draft
description: "Design display banner ads to standard sizes within platform file-weight limits: layout for small formats, optimise assets, animation limits and the final spec check."
sources:
  - https://www.iab.com/
  - https://help.figma.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Display banner ads and file weight

**Goal:** a banner set that meets each ad platform's size and weight limits and still communicates at a glance.

## 1. Sizes
Common IAB standard display sizes (px) include 300x250 (medium rectangle), 728x90 (leaderboard), 160x600 (wide skyscraper), 300x600 (half page), 970x250 (billboard) and 320x50 (mobile leaderboard). Which to build depends on the publishers and platform; get the list from the media plan.

## 2. Layout for tiny formats
- One message, one logo, one CTA; drop secondary copy.
- Add a **border or contrasting edge** so a white-background banner does not dissolve into the page.
- Build a master (see `creative-arts.graphic-design.poster-and-campaign-graphics.campaign-adaptations-figma-auto-layout`), then re-lay each size rather than scaling.
- Keep text legible at the smallest size; test the smallest format first.

## 3. File weight
- Each platform sets an initial-load limit. Typical values for static and animated image files are around the low hundreds of KB, with larger allowances for zipped HTML5 bundles. **Limits differ by platform and change; read the current spec sheet before building.**
- Optimise: JPEG for photos, PNG-8 or SVG for flat graphics, WebP where supported; strip metadata; subset or outline fonts; reuse assets.
- HTML5 banners: compress images, avoid heavy libraries, and use the platform's click-tag convention.

## 4. Animation
- Keep it short and looped a limited number of times; many platforms cap length and loop count (check the spec).
- First frame and last frame should each work as a static fallback; put the message and CTA in the end frame.
- Avoid rapid flashing; WCAG 2.x sets a threshold of no more than three flashes in any one second.

## 5. QA
Preview in the platform's checker, confirm file sizes, check on high-density displays, and keep the editable source.
