---
id: creative-arts.animation.encode-delivery.mezzanine-master
name: mezzanine-master
category: creative-arts
field: animation
product: encode-delivery
tags: [mezzanine, platform-master, prores-422-hq, dnxhr-hqx, master-file, upload-master, intermediate, generation-loss, ffmpeg]
level: practitioner
status: verified
description: "Produce the mezzanine master every other version is made from: codec choice (ProRes/DNxHR), tagging, audio, naming, and why platforms prefer it over H.264 uploads."
sources:
  - https://support.apple.com/en-us/102207
  - https://support.google.com/youtube/answer/1722171
  - https://ffmpeg.org/ffmpeg-codecs.html#ProRes
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Mezzanine master

**Goal:** one high-quality, visually lossless file per episode from which every deliverable
(web H.264, HLS, social cutdowns, DCP, archive) is derived, so no deliverable is ever made from
another lossy deliverable.

## Spec for an HD/UHD SDR animation show

| Item | Choice |
|---|---|
| Codec | ProRes 422 HQ; ProRes 4444 if alpha or heavy graphics; or the mezzanine codec the delivery spec names |
| Bit depth | 10-bit (`yuv422p10le`) |
| Raster/rate | native show resolution and frame rate, progressive |
| Colour | Rec.709/BT.1886, tagged (`creative-arts.animation.encode-delivery.colour-metadata-tags`) |
| Audio | PCM 24-bit 48 kHz: stereo mix on 1-2, plus 5.1 / M&E tracks if produced |
| Head/tail | no bars/slate in a platform mezzanine; facility masters may require them |
| Name | `SHOW_S01E01_TITLE_MEZZ_PRHQ_2398_v003.mov` style: show, ep, kind, codec, rate, version |

```bash
ffmpeg -i final_conform.mov -i final_mix.wav -map 0:v -map 1:a \
  -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a pcm_s24le SHOW_S01E01_MEZZ_PRHQ_24_v001.mov
```

`-profile:v 3` = 422 HQ in `prores_ks` (0 proxy, 1 LT, 2 standard, 3 HQ, 4 4444, 5 4444 XQ).
`-vendor apl0` claims the stream was produced by the Apple encoder (ffmpeg-codecs, `vendor`).

## Why upload the mezzanine

Platforms re-encode uploads (see YouTube's recommended upload encoding settings). A high-quality mezzanine gives their encoder the best source; uploading an already-compressed H.264 adds a generation of loss. Upload bandwidth is the main cost.

## Gotchas

- ProRes mezzanines are large (see Apple's ProRes documentation for data rates). Plan storage.
- Render from the comp in RGB 16-bit or EXR, then make the mezzanine once; do not make it from
  an H.264 review file "because it was already exported".
- Keep the mezzanine's version number aligned with the edit version that produced it.

## Verify

```bash
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,sample_rate:stream_tags= -of compact mezz.mov
```

Then visual compare one frame against the comp render (difference blend should be near black).

## Checked

2026-10-28. Confirmed in ffmpeg-codecs for `prores_ks`: profiles proxy, lt, standard, hq, 4444, 4444xq (so `-profile:v 3` is hq) and the `vendor` option with `apl0`; YouTube's recommended upload encoding settings page is readable. Removed: DNxHR HQX and shop-type statements, the 176 Mbit/s and 80 GB/hour figures, the 'only cost' wording.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: the ProRes command (`-profile:v 3 -vendor apl0 -pix_fmt yuv422p10le`, bt709 tags, `pcm_s24le`): ffprobe reported prores HQ, yuv422p10le, 1920x1080, 24/1 and pcm_s24le 48000. Profiles 0 to 5 probed as Proxy, LT, Standard, HQ, 4444 and XQ. Not run: the visual difference check, YouTube and Apple data-rate pages (documentation only).

Method: documentation plus commands run (ffmpeg 8.0.1).
