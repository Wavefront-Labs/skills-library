---
id: creative-arts.animation.encode-delivery.dcp-festival-master
name: dcp-festival-master
category: creative-arts
field: animation
product: encode-delivery
tags: [dcp, platform-master, digital-cinema-package, dcp-o-matic, smpte-dcp, interop, xyz, jpeg2000, festival, cinema-projection]
level: advanced
status: draft
description: "Make a DCP of an animated short for festival projection with DCP-o-matic: SMPTE vs Interop, flat/scope containers, XYZ conversion, audio mapping, naming, testing."
sources:
  - https://dcpomatic.com/manual
  - https://www.dcimovies.com/
  - https://isdcf.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DCP festival master

**Goal:** a Digital Cinema Package that plays on any festival's DCI server first time.
DCPs carry JPEG 2000 frames in X'Y'Z' colour, PCM audio, and XML playlists, on an ext2/ext3
or NTFS-formatted drive as the festival requests.

## Settings that matter

| Item | Choice |
|---|---|
| Standard | **SMPTE** (current); Interop only if a venue explicitly asks |
| Container | Flat 1998x1080 (1.85) or Scope 2048x858 (2.39); Full 2048x1080 only if required |
| Frame rate | 24 (most compatible); 25 accepted by most modern servers; avoid 23.976 (DCP has no 23.976) |
| Colour | source Rec.709 or P3 converted to XYZ by the tool |
| Audio | 24-bit 48 kHz PCM, 5.1 (L R C LFE Ls Rs) or stereo mapped to L/R |
| Bitrate | default 150-250 Mbps JPEG 2000 is plenty for animation |
| Encryption | none for festivals unless they ask for KDMs |

## DCP-o-matic workflow

1. New film; add the ProRes master (or 16-bit TIFF sequence) and the mix WAVs.
2. DCP tab: container Flat/Scope matching the film's aspect; resolution 2K; standard SMPTE.
3. Content - Video: set the colour conversion to the source (Rec.709 for a video-graded master).
   A 16:9 film in a Flat container is pillarboxed slightly; letterbox or crop deliberately.
4. Content - Audio: check the channel mapping (stereo mix to L and R only, not to centre).
5. Name with the ISDCF convention, e.g. `MyShort_SHR-1_F_EN-XX_INT_51_2K_FEST_20261016_SMPTE_OV`.
6. Make DCP, then copy to the drive with DCP-o-matic's Disk Writer (ext2 for most servers).

## The 23.976 problem

Animation rendered at 23.976 must be played at 24 (0.1% faster) in the DCP: DCP-o-matic
does this and resamples audio. Check runtime and that music pitch shift is acceptable.

## Gotchas

- Grading for cinema: a Rec.709 grade converts acceptably, but a P3 cinema grade on a projector
  looks better; at least check reds and saturated animation colour on a DCI-P3 projector.
- Loudness: cinemas play at reference level (fader 7); a web-mastered -14 LUFS mix will be
  painfully loud. Use a theatrical mix mastered to the cinema calibration (85 dBC per channel reference); ask the festival or mix stage for its loudness target.
- Subtitles: SMPTE DCP uses SMPTE timed text XML, burned-in subs are the safe festival choice.

## Verify

Play the DCP in DCP-o-matic's player and run its verifier (Tools - Verify DCP). Best: test on
a real cinema server at the festival's tech check or a local cinema before shipping.
