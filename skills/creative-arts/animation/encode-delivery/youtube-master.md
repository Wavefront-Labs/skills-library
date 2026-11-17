---
id: creative-arts.animation.encode-delivery.youtube-master
name: youtube-master
category: creative-arts
field: animation
product: encode-delivery
tags: [encode-delivery, ffmpeg, youtube, h264, aac, export, bitrate, faststart, thumbnail, delivery, master, loudnorm]
level: advanced
status: draft
description: "Final YouTube delivery master with ffmpeg: H.264 High/yuv420p at the right 1080p24 bitrate, faststart, AAC 384k/48k, -14 LUFS loudness, thumbnail and captions."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# youtube-master — the upload-ready delivery encode

**Goal:** turn the assembled picture (shot clips concatenated) plus the mastered
audio into one file that looks and sounds correct the moment it finishes
processing on YouTube — right codec, right bitrate, right loudness, streamable
container — and the thumbnail and captions that ship with it. This is the last
stage; nothing downstream can fix what you get wrong here without a re-render.

## In this pipeline

The audio half is grounded in `series/production/build_audio.py`, which masters a
cut to the YouTube target and muxes it in one ffmpeg call. Its final flags are the
ones that matter for delivery:

- `loudnorm=I=-14:TP=-1.5:LRA=11` — integrated **-14 LUFS**, true peak **-1.5 dBTP**,
  loudness range 11. -14 LUFS is YouTube's normalisation target: master quieter and
  YouTube leaves you quiet; master louder and it turns you *down* (so mastering hot
  only loses dynamics, never gains loudness). -1.5 dBTP leaves headroom so the lossy
  AAC encode can't produce inter-sample clipping.
- `-c:a aac -b:a 384k -ar 48000` — AAC, 384 kbit/s, **48 kHz** (the broadcast/video
  sample rate; never deliver 44.1 k for video).
- `-c:v copy` — in that script the video is passed through untouched while only the
  audio is (re)built, so the picture is never double-encoded during the mix.
- `-movflags +faststart` — moves the MP4 `moov` atom to the front so the file
  streams/plays before it's fully downloaded. Non-negotiable for web delivery.

So the loudness/audio spec is already verified in-pipeline; this skill adds the
picture encode and packaging around it.

## The encode (ffmpeg)

When the picture still needs encoding (or re-muxing with the master), feed the
best picture source available and the -14 LUFS master:

```bash
ffmpeg -y -i picture.mp4 -i master.wav \
  -map 0:v -map 1:a \
  -c:v libx264 -preset slow -profile:v high -level:v 4.2 -pix_fmt yuv420p \
  -b:v 12M -maxrate 16M -bufsize 24M \
  -g 12 -keyint_min 12 -r 24 \
  -c:a aac -b:a 384k -ar 48000 \
  -movflags +faststart \
  EP01_master.mp4
```

Flag by flag:

- **`-c:v libx264 -profile:v high -pix_fmt yuv420p`** — H.264 High profile, 8-bit
  4:2:0. `yuv420p` is mandatory for broad playback; leaving libx264 in `yuv444`/`yuvj`
  (which it may pick from PNG/RGB input) breaks QuickTime, many TVs and some phones.
- **`-preset slow`** — spend encode time for a smaller/cleaner file; this is a
  one-shot delivery render, not a realtime job.
- **Bitrate `-b:v 8–12M` at 1080p24.** Cel art is flat, large areas of a single
  colour — it compresses extremely well, so 8–12M is ample and matches YouTube's own
  1080p recommendation. Push to **16M only if banding shows** in gradients/glow
  (skies, the glow bloom). 4K would be ~35–45M. `-maxrate/-bufsize` cap the VBV so a
  busy glitch frame can't spike past what players expect.
- **`-g 12 -keyint_min 12 -r 24`** — a keyframe every 12 frames = every 0.5s at 24fps,
  which helps YouTube's transcoder and seeking. **CFR is required**: the render is
  constant-frame-rate already; forcing `-r 24` guards against any VFR creeping in
  from concat.
- **Audio** — the -14 LUFS/-1.5 dBTP master from `build_audio.py`; re-stated here as
  AAC 384k / 48k so a standalone encode matches.

**Avoid double compression.** Prefer feeding the **PNG frames** or a near-lossless
**CRF 16–18 intermediate** into this final encode rather than re-encoding an
already-lossy concat. If the picture is already a good H.264 and only the audio
changed, mux with `-c:v copy` (as `build_audio.py` does) and skip the video encode
entirely — re-encoding identical video only adds generation loss.

## Concat the picture (CFR-safe)

Assemble per-shot clips with the **concat demuxer**, not the `concat` filter, so no
re-encode and no frame-rate reinterpretation happens at the joins:

```bash
# shots.txt: one line per clip, in order ->  file 'sh010.mp4'
ffmpeg -y -f concat -safe 0 -i shots.txt -c copy picture.mp4
```

Every clip must share codec/resolution/fps/pixfmt or the concat stream copy will
glitch at a boundary — probe them first (see
`creative-arts.animation.encode-delivery.probe`). If the shots were rendered at
different settings, encode each to a matching CRF-18 intermediate before concat
rather than fixing it in the final pass. Because all shots are CFR 24, the joined
`picture.mp4` is CFR 24, and the delivery encode's `-r 24` just guards it.

## Two-pass (only when you must hit an exact size)

The single-pass VBV above (`-b:v` + `-maxrate`/`-bufsize`) is right for almost every
upload. Use two-pass (`-pass 1`/`-pass 2` with the same `-b:v`) only when a hard
file-size ceiling matters; it doesn't improve YouTube quality over a good CRF/VBV
pass and doubles encode time.

## Container & packaging

- MP4 with `+faststart`. Stereo AAC. One video + one audio stream, both mapped
  explicitly (`-map 0:v -map 1:a`) so no stray streams ride along.
- Confirm A/V sync is intact end-to-end: muxing a master that is a few frames
  longer/shorter than the picture drifts lip-sync by the end.

## Thumbnail

Pull a strong hero frame or render a bespoke key pose:

```bash
ffmpeg -ss 00:01:23 -i EP01_master.mp4 -frames:v 1 -q:v 2 thumb_src.png
```

Add the title via `creative-arts.animation.motion-graphics.title-cards`, export
**1280x720**, on-brand, keep it **under 2 MB** (YouTube's thumbnail ceiling). JPG
is fine at this size; PNG if there's flat text/graphics that would JPEG-ring.

## Captions / subtitles

Deliver a sidecar `.srt`/`.vtt` and upload it alongside — do **not** burn captions
into the master (burned-in can't be toggled and fails accessibility). Timecodes
must match the final cut's frame rate (24fps). Auto-generated YouTube captions are
a fallback, not a delivery; an authored SRT is the on-brand option for scripted
dialogue.

## Upload specs (what to hand YouTube)

- 1920x1080, 24fps CFR, H.264 High, yuv420p, `+faststart`.
- AAC-LC stereo, 384 kbit/s, 48 kHz, integrated -14 LUFS / -1.5 dBTP.
- Sidecar SRT captions; 1280x720 thumbnail < 2 MB.

## Verify

- [ ] `ffprobe` the master: **1920x1080, 24fps CFR, yuv420p, H.264 High**; AAC 48k
      stereo; `moov` at front (faststart). (See
      `creative-arts.animation.encode-delivery.probe`.)
- [ ] Measured loudness ~ -14 LUFS, true peak ≤ -1.5 dBTP (ebur128 pass).
- [ ] Container duration == episode runtime; A/V in sync at the *end*, not just the
      start.
- [ ] No banding in glow/gradients at the chosen bitrate (bump to 16M if there is).
- [ ] Picture not double-encoded (fed from frames/CRF-18 intermediate, or muxed with
      `-c:v copy`).
- [ ] Thumbnail 1280x720, on-brand, < 2 MB; SRT timed to 24fps.

status draft: audio/loudness spec is verified (running in `build_audio.py`); the
video encode settings are standard/correct but not yet run end-to-end on a finished
A full episode. See `creative-arts.animation.encode-delivery.probe`,
`creative-arts.animation.motion-graphics.title-cards`.
