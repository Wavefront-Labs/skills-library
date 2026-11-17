---
id: creative-arts.animation.encode-delivery.missing-frame-detection
name: missing-frame-detection
category: creative-arts
field: animation
product: encode-delivery
tags: [missing-frames, image-sequence, duplicate-frames, mpdecimate, freezedetect, render-qc, frame-gaps, ffmpeg, python]
level: practitioner
status: verified
description: "Find missing, zero-byte, black and duplicated frames in render sequences and encoded movies before they ship: gap scan, mpdecimate, blackdetect, freezedetect."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#mpdecimate
  - https://ffmpeg.org/ffmpeg-filters.html#blackdetect
  - https://ffmpeg.org/ffmpeg-filters.html#freezedetect
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Missing and duplicate frame detection

**Goal:** catch the farm's failures before editorial does. Common faults: a frame never
rendered (gap), a frame written as 0 bytes or truncated (node died), a black frame (missing
texture/light link), and repeated frames (a retry wrote the previous frame, or a bad retime).

## 1. Sequence gap and size scan (before encoding)

```python
import re, pathlib, statistics
d = pathlib.Path("renders/shot010")
pat = re.compile(r"\.(\d+)\.(exr|png)$")
frames = {int(m.group(1)): p for p in d.iterdir() if (m := pat.search(p.name))}
first, last = min(frames), max(frames)
missing = [f for f in range(first, last + 1) if f not in frames]
sizes = {f: p.stat().st_size for f, p in frames.items()}
med = statistics.median(sizes.values())
tiny = [f for f, s in sizes.items() if s < 0.2 * med]
print("range", first, last, "missing", missing, "suspiciously small", tiny)
```

Compare `first..last` with the shot's cut range from the shotlist, not just with itself:
a sequence that stops early has no internal gaps.

## 2. Black frames

```bash
ffmpeg -framerate 24 -start_number 1001 -i shot010.%04d.png -vf "blackdetect=d=0:pix_th=0.05" -an -f null - 2>&1 | grep black_start
```

`d=0` reports even single frames. Expected blacks (fade-outs) will show too; check against
the edit.

## 3. Duplicate / frozen frames

```bash
# count frames mpdecimate KEEPS (showinfo prints one line per kept frame); total minus this = near-duplicates
ffmpeg -i shot010.mp4 -vf "mpdecimate=hi=64*4:lo=64*2:frac=0.33,showinfo" -f null - 2>&1 | grep -c "pts_time"
ffmpeg -i ep101.mp4 -vf "freezedetect=n=-60dB:d=0.5" -map 0:v -f null - 2>&1 | grep freeze_
```

Animation on twos and long holds produce legitimate duplicates; what matters is duplicates
where the shot should be moving. Compare against the animation's exposure (a held pose in the
x-sheet is fine; a frozen camera move is not).

## 4. Encoded movie vs expected

```bash
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nk=1:nw=1 ep101.mp4
```

Must equal the sum of shot lengths from the cut.

## Gotchas

- A file can have a valid header and truncated pixel data; size checks catch most, and a full read (for example `oiiotool --stats`, which reports pixel statistics) catches more.
- Renderers that write to a temp name then rename leave `.tmp` files on crashes; exclude them
  from the scan and report them.

## Verify

Run the scan on a known-bad test folder (delete one frame, zero another) and confirm both are
reported.

## Checked

2026-10-28. Confirmed in the ffmpeg-filters manual: `blackdetect` (`pix_th`, `d`), `freezedetect` (`n`, `d`), `mpdecimate`, `showinfo`; oiiotool `--stats`; ffprobe `-count_frames`, `nb_read_frames`, `-select_streams`. The `0.2 * median` size threshold is the author's heuristic and is labelled as such by the 'suspiciously small' output. Reworded: the EXR truncation claim.

2026-11-01 run check: the Python scan, run on a 22-frame folder with frame 1010 absent, a black frame and an 8x8 stub, printed `missing [1010] suspiciously small [1021, 1022]` (the black frame is small as a PNG); `blackdetect=d=0:pix_th=0.05` reported the single black frame (`black_duration:0`); the `mpdecimate` line counted 49 kept frames of 96 (a 2 s moving clip followed by 2 s gray); `freezedetect` reported `freeze_start: 2`; the `-count_frames` query returned 96. `oiiotool` is not installed here, so its `--stats` remark rests on the OpenImageIO documentation only.

Method: commands run with ffmpeg 8.0.1 (Windows build) and Python on synthetic inputs, plus the ffmpeg manual and OpenImageIO documentation.
