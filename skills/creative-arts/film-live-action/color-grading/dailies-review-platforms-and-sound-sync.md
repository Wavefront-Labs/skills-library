---
id: creative-arts.film-live-action.color-grading.dailies-review-platforms-and-sound-sync
name: dailies-review-platforms-and-sound-sync
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, film-live-action, dailies-platforms, dailies-streaming, dailies-review-app, dailies-sound-sync, sync-in-dailies, dailies-audio, moxion, pix, frame-io, ale-metadata]
level: practitioner
status: draft
description: "Deliver dailies for review: syncing production sound by timecode and clap, metadata (ALE), secure streaming platforms (Moxion, PIX, Frame.io), and permissions and watermarking."
sources:
  - "https://www.moxion.io (Moxion - secure dailies review)"
  - "https://frame.io (Frame.io - review and Camera to Cloud)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve - audio sync by timecode/waveform for dailies)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dailies: review platforms and sound sync

**Goal:** by the next morning, the director, producers and studio watch correctly synced,
correctly coloured dailies on a secure platform, and editorial has matching media.

## 1. Sound sync
- Import production sound (poly BWF with iXML metadata) and camera media.
- **Sync by timecode** (Resolve: select clips > *Auto Sync Audio > Based on Timecode*;
  Silverstack/Daylight/ Colorfront similar), then **verify the clap** on every take - fix
  offsets (often whole frames from TC drift).
- Choose **channels**: editorial usually wants the mix track + iso tracks (all channels)
  embedded; review dailies need the **mix** only.
- Takes recorded MOS: mark them; wild tracks: add to a sound bin with metadata.
- Carry **scene/take** metadata from the sound report to the clips (iXML) - critical
  for editorial bins.

## 2. Metadata for editorial
Export an **ALE** (Avid Log Exchange) or provide metadata in the dailies files: tape/ reel
name, source TC, scene, take, camroll, soundroll, circled takes, CDL values. Burn-ins per
editorial request.

## 3. Review platforms
- **Moxion**, **PIX**, **Frame.io**, **DAX**, **Sohonet/ ClearView** - studio-approved
  platforms with per-user **forensic or visible watermarking**, DRM, expiring access,
  device control.
- Upload review-quality H.264/H.265 (HD, ~10-20 Mbps) with the dailies look; organise by
  shoot day and scene; notify viewers.
- Mobile apps for producers on the go; downloads disabled by default.
- Comments/ circled takes from viewers can feed back to editorial.

## 4. Timeline
Same-night or next-morning delivery is standard; publish a schedule (cut-off time for
footage arriving at the lab, upload time). Log every delivery.

## Gotchas
- Trusting TC sync without checking claps; one frame out looks bad on close-ups.
- Losing scene/take metadata - editorial bins unsorted.
- Wrong LUT on review dailies; producers panic about the look.
- Unwatermarked links forwarded around.

## Verify
- [ ] All takes synced and clap-checked; MOS and wild tracks labelled.
- [ ] ALE/metadata delivered with editorial media.
- [ ] Platform permissions, watermarking and expiry set.
- [ ] Delivery schedule met and logged.
