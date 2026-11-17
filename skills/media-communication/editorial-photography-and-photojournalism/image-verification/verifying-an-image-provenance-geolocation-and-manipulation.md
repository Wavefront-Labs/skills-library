---
id: media-communication.editorial-photography-and-photojournalism.image-verification.verifying-an-image-provenance-geolocation-and-manipulation
name: verifying-an-image-provenance-geolocation-and-manipulation
category: media-communication
field: editorial-photography-and-photojournalism
product: image-verification
tags: [editorial-photography-and-photojournalism, image-verification, photo-verification, osint, open-source-investigation, fact-checking, provenance, reverse-image-search, google-lens, tineye, yandex-images, bing-visual-search, geolocation, chronolocation, suncalc, google-earth, street-view, exif, metadata-forensics, exiftool, manipulation-detection, ai-generated-images, deepfakes, c2pa, content-credentials, invid, forensically]
level: practitioner
status: draft
description: "Check a picture is what it claims: trace first appearance with reverse search, contact the source, geolocate and time it, read metadata, and spot edits and AI-generated fakes."
sources:
  - "First Draft / Verification Handbook (European Journalism Centre), paraphrased"
  - "Bellingcat online investigation guides, paraphrased"
  - "C2PA Content Credentials specification overview (c2pa.org), paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Verifying an image: provenance, geolocation and manipulation

**Goal:** before publishing a user-generated or handout picture, establish **who took
it, where, when, and whether it's been altered** — or state clearly what you couldn't
establish.

## 1. Preserve and record
Save the highest-resolution copy you can find, the URL, the account, the post time and
a screenshot of the post. Platforms delete; you need the trail. Log every step.

## 2. Provenance: find the first appearance
- Run **reverse image search** on several engines — Google Lens, TinEye (has "oldest"
  sort), Yandex Images, Bing Visual Search. Each indexes differently; one engine
  finding nothing proves little.
- Crop to distinctive parts and search again; flip horizontally (mirrored reposts).
- For video, extract keyframes (e.g. the InVID-WeVerify browser plugin) and search those.
- An earlier appearance with a different context = recycled image. This is the single
  most common misinformation pattern in breaking news.

## 3. Source contact
Find the earliest uploader and contact them directly: Did you take this? Where were you
standing? Can you send the original file? Ask for adjacent frames — a real photographer
usually has several. Check their account history for presence in that place. Ask for
permission and how they want to be credited (or not, if at risk).

## 4. Geolocation
Match visible features to maps and satellite imagery (Google Earth, Street View,
Mapillary, local mapping services): road markings, signage language and fonts,
skylines, mountains, shopfronts, utility poles, vegetation. Work from distinctive
landmarks inward. Record the coordinates and the matching features side by side.

## 5. Chronolocation (when)
- Shadows: direction and length vs sun position for the claimed place and date
  (SunCalc or similar). *Gives a plausible window, not an exact time.*
- Weather history for that day; seasonal vegetation; events visible (a known
  construction stage, a banner).
- Metadata time if present (often missing or wrong).

## 6. Metadata
`exiftool <file>` shows EXIF/XMP: camera model, capture time, GPS, software. Most
social platforms **strip** metadata, so absence isn't suspicious; presence can still be
faked. A file claiming to be original but showing editing software in the "Software"
tag deserves questions.
**Content Credentials (C2PA)**: if present, inspect them with a C2PA verify tool; they
record capture device and edits. Absence proves nothing — adoption is still partial.

## 7. Manipulation and AI-generated images
- Error-level and clone-detection tools (e.g. Forensically, FotoForensics) can hint at
  edits — treat as leads, not proof; recompression produces false positives.
- AI-image tells (unreliable and fading as models improve): malformed hands/text,
  inconsistent reflections and shadows, mismatched earrings, melting backgrounds,
  too-perfect skin. Prefer **provenance evidence** over visual tells.
- Detector services exist but have notable false-positive/negative rates; never use one
  as sole proof.

## 8. Publishing decision
State confidence plainly in the caption/story: "verified by <outlet> — located to
<place> and confirmed with the photographer", or "could not be independently verified".
Escalate graphic or sensitive images to an editor.

## Gotchas
- Speed pressure in breaking news is when recycled images get through; one reverse
  search costs a minute.
- Contacting a source can endanger them in hostile contexts; consider safety first.
- *Uncertain:* tool names and capabilities change fast; re-check which engines and
  plugins work before relying on them.

## Verify
- [ ] Earliest known appearance found with at least three reverse-search engines.
- [ ] Original uploader contacted or the attempt logged.
- [ ] Location matched to at least two independent features; coordinates recorded.
- [ ] Date/time consistent with shadows, weather and context.
- [ ] Manipulation/AI checks done and treated as leads; confidence stated in publication.
