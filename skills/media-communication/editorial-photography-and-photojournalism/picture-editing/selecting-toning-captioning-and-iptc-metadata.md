---
id: media-communication.editorial-photography-and-photojournalism.picture-editing.selecting-toning-captioning-and-iptc-metadata
name: selecting-toning-captioning-and-iptc-metadata
category: media-communication
field: editorial-photography-and-photojournalism
product: picture-editing
tags: [editorial-photography-and-photojournalism, picture-editing, picture-editor, photo-editor, photo-desk, selecting, the-edit, toning, ethical-toning, photo-manipulation, crop, cropping, captions, caption-writing, credit-line, iptc, iptc-core, xmp, metadata, photo-mechanic, lightroom, bridge, exiftool, wire-photos, editorial-standards]
level: practitioner
status: draft
description: "Prepare news and feature pictures for publication: select from a take, tone within ethical limits, crop honestly, write captions and fill IPTC credit/caption metadata."
sources:
  - "NPPA Code of Ethics, paraphrased"
  - "IPTC Photo Metadata Standard (iptc.org), paraphrased"
  - "Wire-agency photo-editing guidelines as publicly described (e.g. AP, Reuters), paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Selecting, toning, captioning and IPTC metadata

**Goal:** the published picture is the strongest true frame, adjusted only as far as a
darkroom printer could honestly go, with a caption and metadata that would survive
a fact-check.

## 1. Selecting from a take
- Ingest with a fast browser (Photo Mechanic is the newsroom standard; Lightroom or
  Bridge work) and apply your IPTC template on ingest.
- First pass fast: tag anything sharp, well-exposed and meaningful. Don't zoom on every
  frame.
- Second pass: compare similars side-by-side at 100% for focus and expression (eyes
  open, no awkward mouth, hands not cutting faces).
- Choose for **news value first, aesthetics second**: the frame that shows what happened
  beats the prettier one that doesn't.
- Watch what the frame implies: a cropped gesture, a coincidental background (a sign
  behind a politician's head) can create a meaning that wasn't there.

## 2. Ethical toning limits
Allowed (typical wire/newspaper standard; *check your outlet's written policy*):
- global exposure, contrast, white balance, modest saturation;
- local dodging and burning that **doesn't change the content** (lifting a face in
  shadow);
- removing sensor dust spots;
- converting to black-and-white.
Not allowed:
- adding, removing, moving or cloning content (including distracting objects, wires,
  people);
- burning down a background until it disappears, or toning so heavily it changes the
  scene's mood or time of day;
- compositing or AI generative fill/expand;
- in many outlets, heavy noise reduction or sharpening that invents detail.
**Keep the original RAW/JPEG**; you may be asked to prove what was done.

## 3. Cropping
Crop to strengthen, not to change meaning. Don't crop out context that alters the story
(the police line, the crowd size, the other side of an argument). Keep enough
resolution for the intended use.

## 4. Caption writing
Wire-style caption: first sentence in present tense describing what's in the picture
— who (full name, identification left to right), what, where, when (day and date) —
then a background sentence in past tense. Example pattern:
"Firefighters work to contain a blaze at a warehouse in <town>, <region>, on Tuesday,
<date>. The fire broke out early Tuesday; no injuries were reported."
- Verify every name spelling and title.
- Don't describe emotions you can't know ("angry", "devastated") unless stated.
- Note any unusual circumstance: posed portrait, handout image, pool photo, picture
  from social media verified by the outlet, AI- or composite-generated illustration.

## 5. IPTC metadata
Fill at minimum (IPTC Core/Extension field names):
- **Description/Caption**, **Headline**, **Creator** (photographer), **Credit Line**,
  **Copyright Notice**, **Source**, **Date Created**, **City / State / Country**,
  **Keywords**, **Job ID/Transmission Reference** if the desk uses it.
- Check with `exiftool -IPTC:all -XMP:all <file>` that fields survived export; some
  web export presets strip metadata.

## Gotchas
- Camera clock wrong by an hour → wrong Date Created; fix in the ingest template.
- Social-media platforms strip metadata; credit must also be in the visible caption.
- *Uncertain:* exact ethical limits differ between outlets; the list above reflects
  common practice, not a single universal rule.

## Verify
- [ ] Chosen frame is the most accurate account, not just the most dramatic.
- [ ] Only permitted adjustments made; original file kept.
- [ ] Crop keeps context that matters.
- [ ] Caption answers who/what/where/when with verified names and the date.
- [ ] IPTC caption, creator, credit, copyright and date present after export (checked with exiftool).
