---
id: creative-arts.animation.encode-delivery.vmaf-scoring
name: vmaf-scoring
category: creative-arts
field: animation
product: encode-delivery
tags: [vmaf, encode-quality, libvmaf, perceptual-quality, netflix-vmaf, quality-metric, ffmpeg, per-title, json-log]
level: advanced
status: verified
description: "Score encodes against the master with VMAF in ffmpeg: alignment and scaling rules, model choice (HD, 4K, phone), pooled vs per-frame scores and thresholds."
sources:
  - https://github.com/Netflix/vmaf
  - https://github.com/Netflix/vmaf/blob/master/resource/doc/ffmpeg.md
  - https://ffmpeg.org/ffmpeg-filters.html#libvmaf
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VMAF scoring

**Goal:** a number that predicts how viewers will rate an encode relative to its source, used
to pick CRF/bitrate and ladder rungs objectively. VMAF is Netflix's perceptual video quality assessment algorithm (libvmaf);
treat scores as relative and calibrate your own acceptance threshold on your content.

## Command

The distorted file is the first input, the reference second. Both must have identical
resolution, frame rate and frame count, and start on the same frame.

```bash
ffmpeg -i encode_720p.mp4 -i master.mov -lavfi \
 "[0:v]scale=1920:1080:flags=bicubic,setpts=PTS-STARTPTS[d];[1:v]setpts=PTS-STARTPTS[r];[d][r]libvmaf=log_fmt=json:log_path=vmaf.json:n_threads=8" \
 -f null -
```

- Scale lower rungs up to the reference resolution before scoring (the `scale` step in the command above) so both inputs match, and keep the scaler settings the same in every run.
- `setpts=PTS-STARTPTS` aligns start times, as in the manual's libvmaf example; misaligned frames lower the score, and inputs of different resolution make ffmpeg fail (`Invalid argument`) instead of scoring.
- Models: the filter's `model` option defaults to `version=vmaf_v0.6.1`. The libvmaf repository documents the other models and their intended viewing conditions; check it before choosing a non-default model.
- Needs an ffmpeg built with `--enable-libvmaf` (check `ffmpeg -filters | grep vmaf`).

## Reading results

The log is written in the `log_fmt` you chose (xml, json, csv or sub). The `pool` option sets how scores are pooled: `min`, `harmonic_mean` or `mean` (default). In the JSON log (libvmaf in ffmpeg 8.0.1), `pooled_metrics.vmaf` holds `min`, `max`, `mean` and `harmonic_mean` whatever `pool` is set to, and `frames[].metrics.vmaf` holds the per-frame scores.

- The mean can hide bad moments. Look at the per-frame scores in the log and at the `min` pool, and at which frames dip (fast pans, particle FX, film grain).
- Harmonic mean penalises dips more than the arithmetic mean; good for ladder decisions.

## Animation caveats

- VMAF is not a banding detector (the libvmaf README mentions a separate banding metric, CAMBI). Pair it with a visual check
  of gradient shots or a banding metric (`creative-arts.animation.encode-delivery.banding-detection`).
- Holds and on-twos animation score high easily; choose test clips with motion and texture.
- Scores are only comparable with the same model and same reference.

## Verify

Score the master against itself (expect a mean near 100, not exactly 100: a 5 s test clip scored mean 99.8 with max 100, its first frames 97.4, and a synthetic gradient clip scored 97.5) and a deliberately terrible encode (a CRF 51 720p encode scored mean 47.7 against 98.0 for CRF 18 of the same master). If either is off, inputs are misaligned or the wrong input order was used (the first input is the distorted video, the second the reference).

## Checked

2026-10-28. Confirmed in the ffmpeg-filters manual: `libvmaf` options `model` (default `version=vmaf_v0.6.1`), `log_path`, `log_fmt` (xml, json, csv, sub), `pool` (min, harmonic_mean, mean), `n_threads`; first input is the distorted video and the second the reference; `--enable-libvmaf` requirement; the manual's `setpts=PTS-STARTPTS` example. libvmaf README: Netflix algorithm, CAMBI banding metric. Removed: the 93/80/70 score bands, the 0-100 range, the phone and 4K model recommendations (models page not fetched), the JSON key names, the 5th percentile advice, CRF 45 and 50 figures.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: the scaled-distorted-vs-reference command with `log_fmt=json`, `log_path`, `n_threads` and `pool=harmonic_mean` (libvmaf present: `ffmpeg -filters` lists `libvmaf`), JSON keys, self-score, good and bad encode scores, and the resolution-mismatch failure. The harmonic mean was below the arithmetic mean (47.63 against 47.73). Not run: the 4K and phone models.

Method: documentation plus commands run (ffmpeg 8.0.1).
