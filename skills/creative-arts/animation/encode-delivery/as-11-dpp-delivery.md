---
id: creative-arts.animation.encode-delivery.as-11-dpp-delivery
name: as-11-dpp-delivery
category: creative-arts
field: animation
product: encode-delivery
tags: [as-11, dpp, delivery-spec, broadcast, mxf, avc-intra, xdcam-hd, uk-broadcast, ebu-r128, pse, harding]
level: sme
status: draft
description: "Deliver programmes to UK broadcasters as AS-11 UK DPP HD MXF files: codec, audio tracks, R128 loudness, PSE flash testing, segmentation metadata."
sources:
  - https://www.thedpp.com/tech/as-11-dpp
  - https://tech.ebu.ch/publications/r128
  - https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-codes/broadcast-code
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AS-11 UK DPP delivery

**Goal:** a file a UK broadcaster (BBC, ITV, Channel 4, Channel 5, Sky) ingests without QC
failure. AS-11 UK DPP HD is a constrained MXF OP1a file with mandatory descriptive metadata;
broadcasters publish the DPP technical standards and their own supplements.

## Core technical requirements (check the current DPP spec)

| Item | Requirement |
|---|---|
| Wrapper | MXF OP1a, AS-11 shim |
| Video | 1920x1080i25 (or 1080p25 where allowed), AVC-Intra 100 |
| Audio | PCM 24-bit 48 kHz, typically 4 or 16 tracks with a defined track layout (stereo on 1-2, plus M&E or 5.1 as required) |
| Loudness | EBU R128: -23 LUFS integrated (±0.5 LU, ±1 LU live), true peak max -1 dBTP |
| Line-up | bars and tone / ident clock per spec |
| PSE | photosensitive epilepsy test passed (Harding/Ofcom guidance) |
| Metadata | AS-11 core and UK DPP fields: title, episode, programme ID, segmentation (parts and durations), audio track layout, subtitles/sign/AD flags |

## Animation-specific risks

- **Frame rate:** UK HD is 25. Animation made at 24 needs a 4% speed-up
  (`creative-arts.animation.encode-delivery.frame-rate-conversion`); plan audio pitch policy.
- **PSE / flashing:** cartoon flashes, strobing explosions, rapid red transitions and
  high-contrast stripe patterns fail Harding tests. Run the analysis on the cut before
  picture lock, not after.
- **Saturated colour:** keep within EBU R103 gamut tolerances; illegal chroma fails QC.

## Making the file

Usually produced by finishing tools (Avid, Resolve with AS-11 export, Vantage, Cinedeck) or by
a facility. `bmx` tools (`bmxtranswrap`, part of the open-source bmx library) can wrap AS-11
UK DPP with a metadata framework file:
```bash
bmxtranswrap -t as11op1a --dm-file as11 as11_core.txt --dm-file dpp dpp_meta.txt \
  --seg segments.txt -o PROG_ID.mxf input.mxf
```

## Gotchas

- Segmentation durations must sum exactly to programme duration (parts separated by breaks).
- Track layout metadata must match the actual audio, or AD and M&E get routed wrongly on air.
- R128 for UK is -23 LUFS, not streaming's -24/-27 dialogue-gated or YouTube's -14 reference.

## Verify

Run a DPP-compliant QC tool (Baton, Vidchecker, Aurora, or the broadcaster's portal check) and
a Harding PSE test; both pass with no errors, and MXF metadata reads back with `mxf2raw --info`.
