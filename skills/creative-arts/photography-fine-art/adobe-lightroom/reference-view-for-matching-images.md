---
id: creative-arts.photography-fine-art.adobe-lightroom.reference-view-for-matching-images
name: reference-view-for-matching-images
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, reference-view, lightroom-presets, series-consistency, colour-matching, lightroom-classic]
level: practitioner
status: draft
description: "Match tone and colour across a series in Lightroom Classic using Reference View, locked references and Survey checks, so prints and books look consistent."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Reference view)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reference view for matching images

Reference View shows a fixed reference photo beside the photo you are editing, so you can match brightness, contrast and colour across a series.

## Use it
1. Develop module: press `Shift+R` (or the "R|A" button in the toolbar). Left = Reference, right = Active.
2. Drag a photo from the filmstrip onto the Reference pane, or right-click a photo > Set as Reference Photo.
3. Lock icon keeps the reference when you move between active photos.
4. Layout: side by side or top/bottom (toolbar menu).
5. Edit the active photo; the reference stays unchanged.

## Matching method
- Match **mid-tone brightness** first (exposure of the main subject), then white balance, then contrast and saturation.
- Compare the histograms visually and sample neutral or skin areas: both panels show RGB values under the cursor.
- Then copy shared settings with Sync where the light is the same.

## Series checks
- Grid with panels hidden (`Shift+Tab`) and grey background, thumbnail size large: odd ones out are obvious.
- Survey (`N`) the whole sequence; fix outliers in density and temperature.
- For prints, check soft-proofed versions side by side; papers shift differently.

## Gotchas
- Reference view is not available for photos without previews or offline without smart previews.
- Monitor brightness and room light influence judgement: calibrate to print brightness (80-120 cd/m2).

## Verify
- [ ] In Grid view at large thumbnails, no image reads noticeably darker, lighter, warmer or cooler than its neighbours unless intended.
