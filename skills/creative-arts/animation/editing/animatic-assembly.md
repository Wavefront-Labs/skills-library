---
id: creative-arts.animation.editing.animatic-assembly
name: animatic-assembly
category: creative-arts
field: animation
product: editing
tags: [animatic, editing, boards, ffmpeg, concat, vo, timing, pacing, slate, review, maturation]
level: advanced
status: verified
description: "Assemble a cut by ffmpeg concat of per-shot clips cut to scripted dur_s with VO or silence, slates for gaps; animatic matures to final."
sources: []
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# Animatic Assembly (the cut as concat of per-shot clips)

The review cut — proving story, pacing and voice before expensive work — is built as a
**concatenation of one clip per shot, each cut to its scripted duration**. The exact
same assembly recipe runs at three maturities, which is the whole point: the animatic
(boards cut to VO), the per-shot render, and the final (real FX spliced + mixed) all
concat the same shot list to the same `dur_s` per shot, so **timing locked in the
animatic carries through untouched to delivery.** Verified end-to-end in a production pipeline.

## The maturation ladder (one timeline, three fills)

1. **Animatic** — one PNG board per shot (header, action, dialogue, thumbnail), held for
   its duration, muxed over the assembled VO. No 3D. The pacing dummy.
2. **Per-shot render** (`series/production/build_episode.py`) — Blender renders each
   shot to a PNG sequence; the clip is cut to the **same** `dur_s` with the **same** VO.
   Shots the renderer skips (FX/title, or missing assets) become a **slate** of the
   right length so the timeline never shifts.
3. **Final** (`series/production/final_assembly.py`) — reuse the cached per-shot clips,
   splice the finished FX clips over their slates, concat, then master the soundtrack.
   No Blender re-render.

Because every stage cuts each shot to its `dur_s`, you can swap a board for a render for
an FX plate at any time and the cut length and sync do not move.

## In this pipeline

Input to all stages is `series/scripts/EPnn_shotlist.json` (sequences → shots, each with
`id`, `size`, `dur_s`, optional `line_id`, `fx`). The assembly primitives:

### Per-shot clip, cut to scripted duration (`build_episode.py`)

```python
inp = ["-framerate", str(FPS), "-i", f"{frames_dir}/f_%04d.png"]
if vo_wav and os.path.exists(vo_wav):
    aud  = ["-i", vo_wav];  amap = ["-map","0:v","-map","1:a"]
else:
    aud  = ["-f","lavfi","-i","anullsrc=r=48000:cl=stereo"]; amap = ["-map","0:v","-map","1:a"]
run([FFMPEG,"-y",*inp,*aud,*amap,
     "-t", f"{dur:.3f}", "-c:v","libx264","-pix_fmt","yuv420p",
     "-r",str(FPS),"-c:a","aac","-af","apad", out])
```

The critical lines:
- **`-t dur`** forces the clip to the shot's scripted length. Render too short → the
  last PNG holds; too long → trimmed. Either way the clip equals `dur_s` and the cut
  matches the animatic. `vo = VO/{line_id}.wav` when the shot has a `line_id`; otherwise
  a **silent stereo `anullsrc`** fills the audio track so every clip has identical stream
  layout (concat refuses mismatched streams).
- **`-af apad`** pads the audio to the video length so VO shorter than the shot doesn't
  end the clip early (paired with `-t` trimming the long side).
- `-pix_fmt yuv420p` + fixed `-r 24` + AAC on every clip so the concat demuxer gets
  uniform streams.

### VO sync

VO is per-shot, not one long track: each clip carries **its own line's wav**, so sync is
established at clip-build time and is immutable thereafter. Voice lines with local TTS
(Kokoro) keyed by `line_id` into `workspace/vo/{epl}/`. Cache: skip re-voicing when the
wav already exists. The shotlist `dur_s` is the written beat; set it to
`max(written_beat, vo_len + ~0.6s tail)` upstream so a line never gets clipped by its
shot.

### Slates for missing / FX shots

A shot that can't render (renderer returns non-zero, or it's an `FX`/`TITLE` shot) gets a
black slate of the exact duration so timing holds:

```python
def slate_clip(out, dur, label):
    run([FFMPEG,"-y","-f","lavfi","-i",f"color=c=0x0a0a0c:s=1920x1080:d={dur:.3f}:r={FPS}",
         "-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
         "-vf",f"drawtext=text='{label}':fontcolor=0x888888:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2",
         "-t",f"{dur:.3f}","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest",out])
```
Label it with the shot id + size (e.g. `EP01_SQ03_SH050 [FX]`) so the review cut reads as
a coverage map of what's done vs. pending.

### Concat

Build a concat-demuxer list of absolute paths, then stitch:
```python
with open(lst,"w") as f:
    for c in concat: f.write(f"file '{os.path.abspath(c)}'\n")
run([FFMPEG,"-y","-f","concat","-safe","0","-i",lst,
     "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac", out])
```
`-safe 0` allows absolute paths. Re-encode on concat (not `-c copy`) because the clips,
though uniform in format, may differ in GOP boundaries — copy-concat can glitch at joins;
re-encode is reliable and cheap at this resolution.

### Final splice + master (`final_assembly.py`)

Reuse the cached `_clips/{idx:03d}_{sid}.mp4`. Where a real FX plate exists in
`workspace/fx/{sid}.mp4`, normalize it to match the shot clips exactly before concat:
```python
run([FF,"-y","-i",src,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
     "-map","0:v","-map","1:a","-t",f"{dur:.3f}",
     "-vf",f"scale=1920:1080,fps={FPS}","-c:v","libx264","-pix_fmt","yuv420p",
     "-r",str(FPS),"-c:a","aac","-ar","48000","-ac","2","-shortest",dst])
```
Same `-t dur`, same 1080p24, same silent stereo — a normalized FX clip is drop-in
interchangeable with the render clip it replaces. Concat the mix of cached + FX clips,
then call `build_audio.py` for the ducked, mastered soundtrack (see
`creative-arts.animation.sound-design.dialogue-mix-master`).

## ffmpeg 8 gotchas (hard-won)

- `-vsync` was **removed** — it errors. Don't use it.
- `-fps_mode vfr` combined with `-r`/`-fpsmax` → "contradictory" error.
- **CFR output**: plain `-r 24`, no `-fps_mode` at all. This is the working form (and
  what all the clip builders above use).
- Streams must match for concat: same codec, pix_fmt, sample rate, channel layout. The
  silent `anullsrc` on every no-VO clip exists precisely for this.

## Idempotency / coverage

- **Generalize the builder**: `sys.argv[1]` = EPID, derive every path from it. Do NOT
  hardcode `ep01` in output names — Ep2 would silently overwrite Ep1. `build_episode.py`
  takes `<EPID> [SEQ]`; the optional `SEQ` renders just one sequence (e.g. `SQ04`) for a
  fast proof.
- **Coverage pass** (`generate_coverage.py`) expands a shotlist to hit target length:
  back up to `EPnn_shotlist.base.json` **first**, always expand FROM base (idempotent —
  no double-expansion on re-run). Interleave listener-reaction shots after dialogue
  beats + per-location atmosphere inserts + round-robin holds until ≥ target seconds.
- Already-dense episodes can overshoot — check the estimate, restore from base if over,
  skip expansion for that one (Ep1 hit 10m09 → restored to 6m21).

## Calibration

~8–11 shots/min; 6–8 min ≈ 55–87 shots. Dialogue VO is the floor; coverage (reaction /
atmosphere / inserts) is the dial.

## Verify

- [ ] Final runtime == Σ `dur_s` across all shots (timing carried from the animatic).
- [ ] Every shot clip is exactly `dur_s` long (`ffprobe` each in `_clips`).
- [ ] Every clip has a video + an audio stream (silent where no VO) so concat succeeds.
- [ ] Slates present for all `FX`/`TITLE`/missing shots, labelled with id+size.
- [ ] Swapping an animatic board / render / FX plate does not change the cut length.
- [ ] No `-vsync`; CFR via plain `-r 24`.

status draft (content verified in-pipeline): the concat/slate/VO recipe is implemented
and was run end-to-end to build a production review cut (`build_episode.py` +
`final_assembly.py`); marked draft pending the deepened write-up's own review. Scripts:
`series/production/build_episode.py <EPID> [SEQ]`, `series/production/final_assembly.py
[EPID]`, `series/production/generate_coverage.py <EPID> <target_s>`. See
`creative-arts.animation.pipeline.shot-episode-structure` and dialogue-mix-master.

## Verified gotcha: normalise every clip's audio before a concat
The ffmpeg concat demuxer assumes every clip shares the first clip's stream parameters.
A cut whose clips mix mono TTS-rate VO with 48 kHz stereo silence decodes garbage mid-
stream ("Error submitting packet to decoder: Invalid data found") and the conversion
fails. Fix: pre-pass every clip with `-c:v copy -af aresample=48000 -ac 2 -c:a aac`
(video untouched, audio uniform), then concat with `-c copy` - lossless and instant.
