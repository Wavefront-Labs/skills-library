---
id: creative-arts.graphic-design.poster-and-campaign-graphics.social-media-graphics-sizes-and-safe-zones
name: social-media-graphics-sizes-and-safe-zones
category: creative-arts
field: graphic-design
product: poster-and-campaign-graphics
tags: [graphic-design, poster-and-campaign-graphics, ad-specs, media-specs, social-media-graphics, safe-zones, instagram, facebook, linkedin, tiktok, youtube-thumbnail, stories, reels, aspect-ratio, campaign]
level: practitioner
status: draft
description: "Design social graphics to platform specs: core ratios and pixel sizes, UI safe zones for stories and reels, phone legibility and export settings."
sources:
  - https://www.facebook.com/business/ads-guide
  - https://help.instagram.com/1631821640426723
  - https://business.linkedin.com/marketing-solutions/success/ads-guide
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Social media graphics: sizes and safe zones

**Goal:** posts and ads that are not cropped, covered by platform UI, or unreadable on a phone.

## Core ratios (check the platform's current spec page before production: they change)
| Ratio | Pixel size | Where |
|---|---|---|
| **4:5** | 1080 x 1350 | Instagram/Facebook feed portrait (max feed real estate) |
| 1:1 | 1080 x 1080 | Feed square, carousels, LinkedIn |
| **9:16** | 1080 x 1920 | Stories, Reels, TikTok, YouTube Shorts |
| 16:9 | 1920 x 1080 | YouTube, X/Twitter video, LinkedIn video |
| 1.91:1 | 1200 x 628 | Link previews, LinkedIn/Facebook link ads |
| YouTube thumbnail | 1280 x 720 | min width 640 |
Design a **master** in 9:16 and 4:5 and adapt; most campaigns need 1:1, 4:5, 9:16 and 1.91:1.

## Safe zones for vertical full-screen (9:16)
Platform UI covers the top (profile, close) and bottom (caption, CTA buttons, comments).
Common rule (Meta guidance for Stories/Reels ads): keep text, logos and key art out of the
**top ~14% (about 250 px)** and **bottom ~20-35% (about 340-670 px for Reels)** of the 1920 px
height, and away from the right edge on Reels/TikTok where action buttons sit. Put a
safe-zone overlay layer in your template (download platform templates where offered).

## Grid profile thumbnails
Instagram profile grid crops posts to a **3:4** centre preview (recently changed from 1:1);
keep the key message in the centre.

## Legibility on a phone
- Minimum text roughly **40-60 px** on a 1080-wide canvas for secondary text; headline larger.
  Test at actual phone size (view at 33% on a monitor, or send to your phone).
- High contrast, few words (one message per frame); captions carry the detail.
- Meta no longer penalises the 20% text rule, but text-heavy ads still perform worse.

## Export
- PNG for flat graphics with text (avoid JPEG artefacts on type); JPEG 80-90% for photos.
- sRGB colour space with profile; platforms recompress, so start sharp.
- Video: H.264 MP4, AAC audio, captions burned in or as SRT.

## Gotchas
- Carousels: all images take the ratio of the first one.
- Link-preview images are pulled from the page's `og:image`; supply 1200x630.

## Verify
- [ ] Safe-zone overlay checked on every vertical asset.
- [ ] Viewed on a real phone in the platform's preview (or a test post/ad preview).
- [ ] Files named by platform and ratio (`campaign_story_9x16_v2.png`).
