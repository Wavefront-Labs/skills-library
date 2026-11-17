---
id: creative-arts.animation.encode-delivery.netflix-delivery-spec
name: netflix-delivery-spec
category: creative-arts
field: animation
product: encode-delivery
tags: [netflix-delivery, delivery-spec, netflix, partner-help-center, deliverables, prores-proxy, nominal-loudness, timed-text, backlot]
level: sme
status: draft
description: "Plan an animated series delivery to Netflix's Partner Help Center specs: primary and secondary deliverables, video/audio/timed text requirements and QC fail points."
sources:
  - https://backlothelp.netflix.com/hc/en-us/articles/360053755033-Netflix-IMSC-1-1-Text-Profile
  - https://backlothelp.netflix.com/hc/en-us/articles/115000614752-Backlot-Delivery-Instructions-for-IMF
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delivering to Netflix specs

**Goal:** a delivery that passes Netflix QC without redelivery. The authority is the Netflix
Netflix Backlot help site (formerly the Partner Help Center, PHC); specs change, so read the current pages for your title type and
contract schedule before mastering. This skill is the planning checklist, not a copy of the spec.

## Deliverables map (typical for an original animated series)

| Category | Typical requirement (verify current PHC) |
|---|---|
| Primary video | IMF package per episode conforming to SMPTE ST 2067-21 (2016 or 2020 edition) Application 2E, per Netflix's 5.1 delivery spec (Netflix's Photon checker runs in the Backlot upload and blocks failing packages) (`creative-arts.animation.encode-delivery.imf-package-delivery`) |
| Source frame rate | native rate, no conversions; animation commonly 23.976 or 24 |
| Resolution | UHD 3840x2160 for originals that require 4K; check contract |
| HDR | Dolby Vision mastering with metadata, if contracted |
| Audio | 5.1 (and often Atmos) printmaster, stereo, M&E; 24-bit 48 kHz PCM |
| Loudness | dialogue-gated measurement per Netflix sound mix spec (`creative-arts.animation.sound-design.final-mix`) |
| Timed text | Per the Netflix Timed Text Style Guide; IMSC1.1 (Netflix text profile `nst1`) is currently a valid delivery format only for Japanese, other languages use TTML1 (confirm in your delivery requirements list) |
| Secondary | textless elements, trailers/key art, music cue sheets, dialogue lists, scripts |

## Workflow

1. At contract: get the delivery schedule (which deliverables, which languages) and the asset
   ID naming; set up the Backlot portal access.
2. Before mastering: lock frame rate, colour pipeline (see `creative-arts.animation.color.hdr-pq-hlg`
   if HDR), audio formats, and plan textless coverage (every shot with text needs a clean version).
3. Build masters, run your own QC first (`creative-arts.animation.encode-delivery.automated-file-qc`
   plus a full visual pass), then upload through Backlot/Aspera.
4. Track QC reports per asset; fix and resubmit as supplemental IMPs.

## Most common rejection reasons (from PHC QC guidance)

- Picture: dropped/duplicated frames, burned-in text in "textless", aliasing/banding, black
  frames not in the edit, inconsistent cadence.
- Audio: loudness out of tolerance, sync drift, channel mis-assignment, clicks/pops, missing
  M&E fill (dialogue-dependent effects missing from M&E).
- Timed text: reading speed and line-length violations, missing forced narratives, timing off
  shot changes.

## Gotchas

- Spec versions matter: note the PHC article version/date in the delivery bible.
- Netflix-approved cameras/frame rates guidance targets live action; animation sources are
  rendered, but the same "native frame rate, no pulldown" principle applies.

## Verify

A delivery checklist with every schedule line marked delivered and accepted in Backlot, and no
open QC fails.
