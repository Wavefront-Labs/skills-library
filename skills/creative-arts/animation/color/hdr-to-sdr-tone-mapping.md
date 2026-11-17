---
id: creative-arts.animation.color.hdr-to-sdr-tone-mapping
name: hdr-to-sdr-tone-mapping
category: creative-arts
field: animation
product: color
tags: [tone-mapping, hdr, sdr-derivative, zscale, tonemap-filter, hable, mobius, bt2390, ffmpeg, davinci-resolve, gamut-mapping]
level: advanced
status: draft
description: "Derive an SDR Rec.709 version from a PQ HDR master: grade-managed trims in Resolve, or ffmpeg zscale/tonemap for quick derivatives, with gamut handling."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#tonemap-1
  - https://ffmpeg.org/ffmpeg-filters.html#zscale-1
  - https://www.itu.int/pub/R-REP-BT.2390
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HDR to SDR tone mapping

**Goal:** an SDR version that looks intended, not a squashed HDR. Tone mapping compresses
luminance (thousands of nits to ~100) and gamut (Rec.2020/P3 to Rec.709).

## Best: colourist-controlled

- Dolby Vision 100-nit trim (`creative-arts.animation.color.dolby-vision-trims`), or
- A separate SDR grade pass in Resolve starting from the HDR grade, with the output set to
  Rec.709 Gamma 2.4 and Resolve's tone mapping (DaVinci or Luminance mapping) as the start point.

## Quick derivative with ffmpeg (previews, social, review copies)

```bash
ffmpeg -i hdr_pq.mov -vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,\
tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" \
  -c:v libx264 -crf 18 -color_primaries bt709 -color_trc bt709 -colorspace bt709 sdr.mp4
```

- `zscale=t=linear:npl=100` linearises PQ with 100 nits as nominal peak (raise `npl` to darken
  less aggressively).
- Convert primaries to BT.709 in linear float, then tone map, then re-encode BT.709.
- Operators: `hable` (filmic, preserves highlights, can look dark), `mobius` (keeps in-range values
  untouched, gentle), `reinhard`, `clip` (no mapping). Animation with bright flat skies often
  looks best with `mobius` and a slight gamma lift afterwards.
- Requires ffmpeg built with libzimg (`ffmpeg -filters | grep zscale`).

## Gamut

Saturated animated colours outside Rec.709 clip by channel and shift hue (a magenta glow turns
pink-blue). `desat` in `tonemap` reduces highlight saturation to avoid it; Resolve's gamut mapping
(Colour Space Transform, saturation knee) does it better.

## Gotchas

- Static tone mapping treats a night scene and a day scene the same; dynamic (DV) or graded SDR is
  needed for broadcast-quality SDR.
- Never derive SDR from an 8-bit HDR proxy; start from the 10-bit+ PQ master.
- Tag the output correctly; an untagged SDR derivative of an HDR file is often shown as HDR by players.

## Verify

Compare the SDR derivative with the HDR on the reference display side by side for faces, skies and
emissive FX: no hue shifts in saturated FX, shadows not crushed, mid-tones similar in feel.
