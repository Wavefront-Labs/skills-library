---
id: creative-arts.animation.encode-delivery.automated-file-qc
name: automated-file-qc
category: creative-arts
field: animation
product: encode-delivery
tags: [automated-qc, delivery-spec, file-qc, mediaconch, ffprobe, ebur128, blackdetect, signalstats, baton, qc-report, python]
level: advanced
status: verified
description: "Automate file QC on masters before delivery: policy checks with MediaConch, ffprobe spec asserts, loudness, black/freeze/silence detection, legal range scans."
sources:
  - https://mediaarea.net/MediaConch
  - https://ffmpeg.org/ffmpeg-filters.html#signalstats-1
  - https://ffmpeg.org/ffmpeg-filters.html#ebur128-1
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Automated file QC

**Goal:** catch every machine-detectable fault before a human watches the file or a client QC
house bills you for a fail. Commercial QC tools do this at scale; the same checks can be scripted with free tools for a smaller studio.

## 1. Container and stream policy

MediaConch is an implementation and policy checker for audiovisual files (see mediaarea.net/MediaConch for its command line). A policy expresses the delivery spec: codec and profile, raster, frame rate, scan type, audio channel count, sample rate and bit depth.

Or assert directly in a script:
```python
import json, subprocess
p = json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json","master.mov"]))
v = next(s for s in p["streams"] if s["codec_type"] == "video")
assert v["codec_name"] == "prores" and v["width"] == 1920 and v["r_frame_rate"] == "24/1", v
assert v.get("color_primaries") == "bt709", "untagged colour"
a = [s for s in p["streams"] if s["codec_type"] == "audio"]
assert all(s["sample_rate"] == "48000" for s in a), "sample rate"
```

## 2. Content checks (one decode pass each, or chain them)

```bash
# loudness and true peak
ffmpeg -nostats -i master.mov -map 0:a:0 -af ebur128=peak=true -f null - 2>&1 | tail -12
# black frames and frozen picture
ffmpeg -i master.mov -vf "blackdetect=d=0.04:pix_th=0.05,freezedetect=n=-60dB:d=1" -an -f null - 2>&1 | grep -E "black_|freeze_"
# silence gaps in the mix
ffmpeg -i master.mov -map 0:a:0 -af "silencedetect=n=-60dB:d=2" -f null - 2>&1 | grep silence_
# out-of-legal-range luma (count frames with YMIN<16 or YMAX>235)
ffmpeg -i master.mov -vf "signalstats,metadata=print:key=lavfi.signalstats.YMAX" -an -f null - 2>&1 | awk -F= '/YMAX/ && $2>235 {n++} END {print n+0, "frames above 235"}'
```

## 3. Report

Collect each result with timecode (convert seconds to TC at the file's rate) into a CSV/HTML
report; classify as fail, warn or info. Expected events (fades to black, intentional silence)
are whitelisted per title from the edit, not ignored globally.

## Gotchas

- Automated QC does not replace a full real-time visual and audio pass: it cannot see a wrong
  shot version, a continuity error or a lip-sync miss.
- Thresholds tuned for live action flag animation holds as "freeze"; set freeze duration
  longer than the longest intentional hold, or review those events by timecode.

## Verify

Seed a test master with known faults (2 s of silence, a black frame, a wrong sample rate) and
confirm each is reported with correct timecode.

## Checked

2026-10-28. Confirmed: ffmpeg `blackdetect` (`pixel_black_th`/`pix_th`, `black_min_duration`/`d`), `freezedetect` (`n` default -60dB, `d`), `silencedetect` (`n`, `d`), `signalstats` metadata keys (`lavfi.signalstats.YMAX`), `ebur128` peak option; ffprobe field names (`codec_type`, `r_frame_rate`, `color_primaries`, `sample_rate`) in the ffprobe XML schema; 8-bit limited range 16-235 (ffmpeg colorspace wiki). Removed: the MediaConch command line and policy field names (the fetched page gives no syntax), the commercial tool list.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: the ffprobe/Python assertion snippet (the untagged ProRes source failed the colour assertion as written, `color_primaries` absent), `ebur128=peak=true`, `blackdetect`, `freezedetect`, `silencedetect` and the `signalstats` YMAX count. A seeded file (3 s white, 0.125 s black, 2 s white, 5.1 s silent mono audio) was reported correctly: black_start 3, black_duration 0.125, freeze events, silence_start 0 for 5.1 s. Not run: MediaConch (not installed; the skill gives no command for it).

Method: documentation plus commands run (ffmpeg 8.0.1).
