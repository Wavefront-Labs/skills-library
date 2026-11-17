---
id: creative-arts.photography-fine-art.adobe-lightroom.black-and-white-mix
name: black-and-white-mix
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, bw-mix, lightroom-color, black-and-white-conversion, monochrome-profile, lightroom-classic]
level: practitioner
status: draft
description: "Convert to black and white in Lightroom Classic with a monochrome profile and the B&W Mix sliders, emulating colour filters and controlling tonal separation."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Convert photos to black and white)", "Ansel Adams, The Negative (filters for black-and-white)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Black and white mix

## Convert
1. Press `V` or choose **Black & White** at the top of the Basic panel. This applies the Adobe Monochrome profile (or choose a B&W creative profile, B&W 01-12, as a start).
2. The HSL panel becomes **B&W Mix** with eight colour sliders controlling the brightness each colour maps to.
3. **Auto** sets a mix based on the image; useful as a base.

## Emulating filters on film
| Look | Mix |
|---|---|
| Yellow filter (gentle sky darkening) | Blue -20, Yellow +10 |
| Orange filter | Blue -40, Aqua -20, Orange +20 |
| Red filter (dramatic black skies) | Blue -60 to -80, Aqua -40, Red/Orange +30 |
| Green filter (foliage lighter, skin darker) | Green +30, Yellow +10, Red -10 |

## Targeted adjustment
Click the target icon in B&W Mix, then drag on an area of the photo: dragging a sky down darkens all the colour bands in it.

## Tonal craft
- Separate subjects that share luminance but differ in hue (red flower against green leaves turn the same grey): push one band, pull the other.
- Then re-set Whites/Blacks; the mix moves tones.
- Tone the result with Color Grading (Highlights warm, Shadows neutral/cool) for a printed look.

## Gotchas
- Extreme mix values posterise smooth gradients and boost noise (especially Blue -80 skies). Check at 100%.
- Skin in red-filter mixes goes chalky; mask the face and correct locally.

## Verify
- [ ] Main subject separates from background in tone; no banding in skies.
