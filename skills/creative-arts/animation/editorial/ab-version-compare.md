---
id: creative-arts.animation.editorial.ab-version-compare
name: ab-version-compare
category: creative-arts
field: animation
product: editorial
tags: [ab-compare, review-approval, cut-review, wipe, side-by-side, version-comparison, openrv, hstack, difference-blend, ffmpeg]
level: practitioner
status: draft
description: "Compare two versions of a shot or cut for review: side-by-side, wipe, and difference views in RV/Resolve or generated with ffmpeg hstack/blend, synced frame-accurately."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#hstack-1
  - https://ffmpeg.org/ffmpeg-filters.html#blend-1
  - https://github.com/AcademySoftwareFoundation/OpenRV
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A/B version comparison

**Goal:** reviewers see precisely what changed between v011 and v012: timing, poses, lighting, so notes
address the change and approvals are confident.

## Views

| View | Shows | Best for |
|---|---|---|
| Side by side | both versions at once | timing and pose changes |
| Wipe | split with a moving divider | lighting, colour, small detail changes |
| Toggle (flip) | alternates on the same frame | subtle differences |
| Difference | absolute pixel difference | what exactly changed (QC) |

## In review tools

- OpenRV: load both sources, Sequence/Stack/Layout views; Wipes via the Stack view; frame-locked playback.
- Resolve: Gallery still or clip compare with split-screen wipe (Colour page), or two-up in the Cut page.
- Review platforms: version stacks with compare mode (side-by-side/overlay).

## Generate with ffmpeg

```bash
# side by side with labels
ffmpeg -i v011.mov -i v012.mov -filter_complex \
 "[0:v]drawtext=fontfile=<FONT>.ttf:text='v011':x=20:y=20:fontsize=36:fontcolor=white[a];\
  [1:v]drawtext=fontfile=<FONT>.ttf:text='v012':x=20:y=20:fontsize=36:fontcolor=white[b];\
  [a][b]hstack=inputs=2,scale=1920:-2" -c:v libx264 -crf 20 -pix_fmt yuv420p ab_sbs.mp4

# difference (black where identical)
ffmpeg -i v011.mov -i v012.mov -filter_complex "[0:v][1:v]blend=all_mode=difference,eq=contrast=4" diff.mp4
```
Both inputs need identical resolution and frame rate; scale/pad first if not.

## Timing changes

When v012 is longer or shorter, side by side at the same start frame misleads after the first change. Align on
the cut's frame numbers (use handles-trimmed versions) and state the frame count difference in the label.

## Gotchas

- Different colour tags or ranges between versions look like changes; normalise both through the same transform.
- Audio: play one version's audio only, or the review becomes unusable.

## Verify

Frame-step both sides together: frame counters match on every frame, and the difference view is black except
where changes were intended.
