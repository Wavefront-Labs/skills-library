---
id: creative-arts.design-for-form-and-experience.prototyping.building-realistic-high-fidelity-mockups
name: building-realistic-high-fidelity-mockups
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [realistic-content, device-mockup, high-fidelity-mockup, mockups, hi-fi-design, presentation-mockups, content-design]
level: practitioner
status: draft
description: "Build high-fidelity mockups with realistic content, data and edge cases, then present them in device mockups with correct scale, lighting and context."
sources:
  - "Nielsen Norman Group - articles on realistic content and designing with real data (nngroup.com)"
  - "Material Design and Apple HIG - Layout with real content and device sizes (m3.material.io, developer.apple.com/design)"
  - "Figma Community - Mockup plugins and device frames (figma.com/community)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Realistic content and device mockups

## Realistic content
- **Replace lorem ipsum** with plausible copy, names, prices, dates, images and numbers drawn from real sources: a data sample, product feed, or writer-provided copy. Realistic data exposes layout, truncation and hierarchy problems.
- **Vary the content:** short and long names (2 and 40 characters), missing images, many and zero items, different languages (German, Arabic RTL, CJK), large numbers, long emails; create a **content matrix** of edge cases and design each.
- **Diverse, inclusive data:** names, avatars and scenarios from different backgrounds; avoid stereotypes.
- Tools: Figma **Content Reel**, **Faker**-based plugins, Google Sheets synced with the Google Sheets Sync plugin, unsplash/pexels with licences, **Lorem Picsum**, AI image tools (watermarked or clearly flagged).
- Legal: avoid real people's data and trademarks; use sample brands or fictional ones.

## Device mockups for presentation
1. **Design at actual sizes:** iPhone 15 (393x852 pt), common Android (360x800 dp), desktop 1440x900; use official device frames and safe areas, status bar, home indicator.
2. **Show context:** place screens on devices in a scene (desk, hand, street) via Figma/Photoshop mockup templates, Mockuuups Studio, Shots, Rotato, or 3D tools (Blender with device models); match perspective, scale and lighting; keep UI crisp at 2x.
3. **Real-state screens:** show the primary flow (3-5 frames) plus key states (loading, error, empty) as a storyboard or filmstrip.
4. Maintain readability: do not shrink screens below legibility; add callouts where needed.
5. **Export** at 2x-3x PNG or MP4 for motion with screen recordings captured from the prototype on device.

## Verify
- [ ] Content realistic with edge cases designed; no lorem ipsum remains.
- [ ] Device frames and sizes accurate.
- [ ] Exports sharp and annotated for the audience.
