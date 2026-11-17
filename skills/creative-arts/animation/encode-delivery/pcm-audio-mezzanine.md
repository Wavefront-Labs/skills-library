---
id: creative-arts.animation.encode-delivery.pcm-audio-mezzanine
name: pcm-audio-mezzanine
category: creative-arts
field: animation
product: encode-delivery
tags: [pcm-audio, audio-mux, muxing, pcm_s24le, 48khz, mezzanine, prores, wav, mov, lossless-audio, ffmpeg]
level: practitioner
status: verified
description: "Carry uncompressed PCM audio in mezzanine and master files: 24-bit 48 kHz, codec choice per container, avoiding lossy round trips and sample-rate surprises."
sources:
  - https://ffmpeg.org/ffmpeg-codecs.html#Audio-Encoders
  - https://partnerhelp.netflixstudios.com/hc/en-us
  - https://support.google.com/youtube/answer/1722171
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# PCM audio in mezzanines

**Goal:** the master's audio is bit-identical to the mix. Lossy audio (AAC, MP3, AC-3) belongs
only in the final consumer encode; every earlier file carries PCM.

## The standard

- **48 kHz, 24-bit** linear PCM. 48k is the video/broadcast rate; 44.1k is music/CD and must
  be resampled once, carefully, if a score arrives that way.
- `pcm_s24le` is ffmpeg's 24-bit little-endian PCM codec; use a container the delivery spec allows for PCM (MOV for a ProRes/PCM master here).

```bash
# picture from the render, audio from the final mix, no audio re-encode beyond PCM wrap
ffmpeg -i picture_prores.mov -i final_mix_48k24.wav -map 0:v -map 1:a \
  -c:v copy -c:a pcm_s24le -shortest master.mov
```

## Resampling once, properly

```bash
ffmpeg -i score_44k1.wav -af "aresample=48000:resampler=soxr:precision=28" -c:a pcm_s24le score_48k.wav
```
Needs an ffmpeg built with libsoxr: on the Windows essentials build `resampler=soxr` fails with `Requested resampling engine is unavailable`; drop it to use the default resampler. Use the soxr resampler (`precision=28` is SoX's Very High Quality setting; the default 20 suits a 16-bit destination, per the ffmpeg-resampler manual). Never let the NLE or ffmpeg resample implicitly at mux time, and never
upsample 16-bit to 24-bit then call it 24-bit source.

## Bit depth on the way down

Going 32-bit float or 24-bit to 16-bit (only when a spec demands it): dither once,
`-af "aresample=osf=s16:dither_method=triangular_hp"`.

## Gotchas

- Upload platforms re-encode what they receive; uploading AAC means a lossy file is encoded again (generation loss).
- `-shortest` trims to the shorter stream; if the mix is longer than picture you lose the tail,
  if shorter you lose picture. Make them equal length upstream instead of relying on it.
- An unintended `-ar 44100` in a copied command will resample the master silently.

## Verify

```bash
ffprobe -v error -select_streams a -show_entries stream=codec_name,sample_rate,bits_per_raw_sample,channels -of compact master.mov
ffmpeg -i final_mix_48k24.wav -map 0:a -c:a pcm_s24le -f md5 - ; ffmpeg -i master.mov -map 0:a -c:a pcm_s24le -f md5 -
```

Codec `pcm_s24le`, 48000, and the two audio MD5s match (bit-identical).

## Checked

2026-10-28. Confirmed in the ffmpeg-resampler manual: `resampler=soxr`, soxr-only `precision` (default 20, 28 = Very High Quality), `osf`/`out_sample_fmt`, `dither_method` value `triangular_hp`; `-shortest` in the ffmpeg manual. Removed: `pcm_s24be`/MXF/MP4 container statements, the sibilants-and-cymbals claim.

2026-11-01 run check: the picture + PCM mux with `-shortest` ran and probed `pcm_s24le`, 48000, 24 bits; the two MD5 commands matched only after the first one also got `-c:a pcm_s24le` (without it the MD5 muxer hashed 16-bit audio and the digests differed; fixed above); `aresample=osf=s16:dither_method=triangular_hp` ran and produced `pcm_s16le`; plain `aresample=48000` resampled 44.1 kHz to 48000. The soxr command could not run on this build, so `precision=28` rests on the ffmpeg-resampler manual.

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg-resampler manual for soxr.
