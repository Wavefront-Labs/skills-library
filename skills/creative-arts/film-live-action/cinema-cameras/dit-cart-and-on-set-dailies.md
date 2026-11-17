---
id: creative-arts.film-live-action.cinema-cameras.dit-cart-and-on-set-dailies
name: dit-cart-and-on-set-dailies
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, dit-cart, cart-setup, dit-workflow, dailies-transcoding, on-set-transcode, dailies-with-lut, livegrade, silverstack, daylight, cdl-on-set]
level: practitioner
status: draft
description: "Design a DIT cart and workflow: hardware and power, offload and verification, live grading with CDLs, and transcoding dailies with LUT, burn-ins and synced sound on set."
sources:
  - "https://pomfort.com (Pomfort Silverstack and Livegrade documentation)"
  - "https://www.colorfront.com (Colorfront On-Set Dailies / Express Dailies)"
  - "https://www.blackmagicdesign.com/products/davinciresolve (DaVinci Resolve - dailies workflow)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DIT cart and on-set dailies

**Goal:** a cart that offloads safely, keeps the look consistent from set to edit, and
delivers editorial-ready dailies the same day.

## 1. Workflow design (prep)
With DP, post supervisor and editor agree: camera formats, number of copies (usually 3:
2 shuttle/backup + 1 for dailies/ LTO), checksum method, look pipeline (show LUT + CDL),
dailies codec (e.g. Avid DNxHD 36/115 or ProRes Proxy/LT), burn-ins, file naming, sound
sync responsibility, delivery method and deadlines. Write it as a one-page workflow
diagram.

## 2. Cart hardware
- Workstation (Mac Studio/Pro or PC) with fast I/O (Thunderbolt/PCIe), card readers for
  each camera media (Codex, AXS, CFexpress), RAID or NVMe working storage.
- **Reference monitor** (calibrated - Flanders/Sony) and a scope; a dark viewing area
  (hood/tent).
- **UPS** and clean power; network for wireless video/ Livegrade connections.
- Rugged cart (with wheels for location), weatherproofing, cooling.

## 3. Offload and verification
Use offload software (Silverstack, ShotPut Pro, Hedge, YoYotta) with **checksum
verification** (xxHash64 or MD5) to all destinations simultaneously. Don't clear cards
until verified copies exist on at least two separate drives and the camera team has
signed off. Generate the offload report.

## 4. Live grading
Livegrade (Pomfort) or similar: camera SDI -> LUT box -> monitor; DIT applies CDL
(slope/offset/power/saturation) per set-up with the DP, saving looks per clip; the
CDLs travel with the metadata to dailies and VFX.

## 5. Dailies transcoding on set
- Tools: DaVinci Resolve, Silverstack XT, Colorfront, Daylight.
- Apply the **show LUT + CDL**, sync sound (by timecode, check clap), add **burn-ins**
  (clip name, TC, scene/take) per editorial request, render to the edit codec with
  correct metadata (tape/reel names, TC).
- Verify a sample in the NLE; deliver to editorial (shuttle or upload) and to the
  review platform (Moxion, Frame.io, PIX).

## Gotchas
- Card formatted before verified backups.
- Uncalibrated monitor; DP approves looks that don't match grading.
- Dailies without reel/tape names - conform breaks later.
- Cart power off a noisy generator without UPS.

## Verify
- [ ] Workflow document agreed by DP, post and editorial.
- [ ] Offloads checksum-verified to multiple destinations; reports kept.
- [ ] CDLs saved per clip and passed on.
- [ ] Dailies with correct LUT, sync, burn-ins and metadata delivered on time.
