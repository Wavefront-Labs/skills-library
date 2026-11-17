---
id: creative-arts.animation.editorial.review-burn-ins
name: review-burn-ins
category: creative-arts
field: animation
product: editorial
tags: [burn-ins, review-approval, cut-review, drawtext, timecode-burn-in, shot-name, version-label, ffmpeg, review-copies]
level: practitioner
status: draft
description: "Burn timecode, frame counter, shot name, version and date into review copies with ffmpeg drawtext or NLE data burn-in, laid out to stay readable and out of the action."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#drawtext-1
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Review burn-ins

**Goal:** any still or note from a review copy identifies exactly which version and frame it came from.

## Standard layout (1920x1080)

| Position | Content |
|---|---|
| top left | show / episode / sequence |
| top right | shot or cut version (`sq020_sh010 v012`, `EP104 cut v012`) |
| bottom left | record timecode |
| bottom right | frame counter (shot frames, 1001-based) |
| bottom centre | date and "INTERNAL REVIEW" or recipient name |

Use a letterboxed or padded frame for burn-ins when possible so text never covers picture:
`pad=iw:ih+120:0:60`.

## ffmpeg

```bash
ffmpeg -i sq020_sh010_v012.mov -vf "pad=iw:ih+120:0:60:black,\
drawtext=fontfile=<FONT>.ttf:text='EP104 sq020_sh010 v012':x=20:y=18:fontsize=32:fontcolor=white,\
drawtext=fontfile=<FONT>.ttf:timecode='01\:02\:13\:04':rate=24:x=20:y=h-46:fontsize=32:fontcolor=white,\
drawtext=fontfile=<FONT>.ttf:text='%{frame_num}':start_number=1001:x=w-tw-20:y=h-46:fontsize=32:fontcolor=white,\
drawtext=fontfile=<FONT>.ttf:text='%{localtime\:%Y-%m-%d}':x=(w-tw)/2:y=h-46:fontsize=28:fontcolor=gray" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k sq020_sh010_v012_review.mp4
```
- `timecode=` with `rate=` renders running timecode from a start value (escape colons).
- `%{frame_num}` with `start_number` renders the frame counter.
- Always pass `fontfile` on render nodes; default fonts differ between machines.

## In NLEs

- Resolve: Workspace - Data Burn-In (per project or per clip): record TC, source TC, clip name, custom text.
- Premiere: Timecode effect and Clip Name effect on an adjustment layer.
- Avid: Timecode Burn-In effect.

## Gotchas

- Burn-ins on deliverables: never. Keep burn-in renders in a separate review folder with `_review` in the
  name, and automated QC that flags text in masters.
- Timecode on burn-in must match the edit's record timecode, or notes point at the wrong place.

## Verify

Pause on a random frame: the frame counter equals the shot frame in the tracker's range, the timecode matches
the timeline position in the NLE, and nothing important in the picture is covered.
