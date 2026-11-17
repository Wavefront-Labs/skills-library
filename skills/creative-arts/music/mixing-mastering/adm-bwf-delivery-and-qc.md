---
id: creative-arts.music.mixing-mastering.adm-bwf-delivery-and-qc
name: adm-bwf-delivery-and-qc
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, dolby-atmos, spatial-audio, adm-bwf, master-file, atmos-delivery, distributor-delivery, loudness-qc, true-peak, 48-khz, 24-bit, metadata, isrc, atmos-qc]
level: advanced
status: draft
description: "Export and QC a Dolby Atmos music master: ADM BWF settings, loudness and true-peak checks, start/end rules, re-render checks and distributor requirements."
sources: ["https://professionalsupport.dolby.com/s/article/Dolby-Atmos-Renderer-v5-guide (export ADM BWF)", "https://professional.dolby.com/music/ (Dolby Atmos Music delivery)", "https://support.apple.com/guide/logicpro/export-a-dolby-atmos-adm-bwf-file-lgcpb7b09f0f/mac"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ADM BWF delivery and QC

**Goal:** an Atmos master file that passes distributor QC first time.

## 1. Export
- Format: **ADM BWF** (.wav with Audio Definition Model metadata), **48 kHz, 24-bit**. Exported from the renderer (Dolby Atmos Renderer: File > Export ADM BWF; Logic: File > Export > Project as ADM BWF).
- Contains all beds and objects plus positional and binaural metadata; it is not a playable stereo file.
- Some services/distributors also accept or require a Dolby Atmos master file set (.atmos); check the distributor's spec.

## 2. QC checklist
1. **Loudness**: integrated loudness at or below the platform target (Apple: no louder than **-18 LKFS**), **true peak at or below -1 dBTP**. Measure on the full program with the renderer's loudness analysis (it measures the 5.1 re-render).
2. **Start and end**: a short amount of silence/handles at start per spec; nothing cut off at the end (reverb tails complete).
3. **Sync with stereo**: the Atmos and stereo masters are usually expected to have matching song structure and start point; compare.
4. **Re-renders**: listen to 7.1.4, 5.1, stereo and binaural re-renders from the ADM for errors (missing objects, panning glitches).
5. **Object/bed count** within limits; no unused empty objects.
6. Re-import the ADM into a fresh renderer session and play it back as a final check.

## 3. Metadata and accompanying deliverables
- Distributor delivers the Atmos as a separate asset linked to the same ISRC/track as the stereo (follow the distributor's instructions; some assign a separate ISRC for the immersive version).
- Supply the stereo master too; Apple Music requires the stereo version to exist.

## Gotchas
- Exporting at 44.1 kHz or with the wrong frame rate: rejected.
- Overshooting loudness because only the binaural was checked.
- Clipping in individual objects that doesn't show on the master meter; check object meters.

## Verify
- Loudness report saved with the deliverable (integrated LKFS, true peak).
- ADM re-imported and played back without errors.
