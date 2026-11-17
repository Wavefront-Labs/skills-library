---
id: creative-arts.animation.encode-delivery.audio-channel-layout-mapping
name: audio-channel-layout-mapping
category: creative-arts
field: animation
product: encode-delivery
tags: [channel-layout, audio-mux, muxing, 5-1, stereo, pan-filter, amerge, channelmap, smpte-order, discrete-tracks, ffmpeg]
level: advanced
status: verified
description: "Build and verify audio channel layouts in deliverables: 5.1 order L R C LFE Ls Rs, discrete mono tracks, stems on separate tracks, ffmpeg pan/amerge/channelmap."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#pan-1
  - https://ffmpeg.org/ffmpeg-filters.html#amerge-1
  - https://trac.ffmpeg.org/wiki/AudioChannelManipulation
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Audio channel layout and track mapping

**Goal:** every channel in the delivery file is where the spec says, labelled correctly. A
swapped centre and LFE (dialogue in the subwoofer) is a classic rejection.

## Standard orders

- ffmpeg's `5.1` layout order: **FL, FR, FC, LFE, BL, BR** (L, R, C, LFE, Ls, Rs). Confirm the order and labels your delivery spec requires.
- A session that exports in another order (for example L C R Ls Rs LFE) must be remapped.
- Stereo: L, R.

## Common builds

Six mono WAV stems from the mix into one 5.1 track:
```bash
ffmpeg -i L.wav -i R.wav -i C.wav -i LFE.wav -i Ls.wav -i Rs.wav \
  -filter_complex "[0:a][1:a][2:a][3:a][4:a][5:a]join=inputs=6:channel_layout=5.1:map=0.0-FL|1.0-FR|2.0-FC|3.0-LFE|4.0-BL|5.0-BR[a]" \
  -map "[a]" -c:a pcm_s24le mix51.wav
```
(ffmpeg has a `5.1` layout, whose surrounds are `BL`/`BR` as in the ffmpeg wiki join example, and a `5.1(side)` layout; be consistent with the spec's label.)

Film order 6-channel file to SMPTE order:
```bash
ffmpeg -i film_order.wav -af "channelmap=0|2|1|5|3|4:5.1" smpte.wav
```
Each entry is the input channel index placed at output position 0 to 5 of the `5.1` layout (the form the manual's own 5.1 reorder example uses). Write the mapping out per index and check it twice.

Multi-track MOV/MXF with stems on separate tracks (a typical broadcast layout):
```bash
ffmpeg -i picture.mov -i mix51.wav -i mixLR.wav -i me51.wav \
  -map 0:v -map 1:a -map 2:a -map 3:a -c:v copy -c:a pcm_s24le \
  -metadata:s:a:0 handler_name="5.1 Mix" -metadata:s:a:1 handler_name="Stereo Mix" -metadata:s:a:2 handler_name="5.1 M&E" out.mov
```
In MOV the track label is `handler_name`: with ffmpeg 8.0.1 `-metadata:s:a:0 title=...` was silently not written to the .mov (ffprobe showed only `handler_name=SoundHandler`), while Matroska kept `title`.

Stereo fold-down for a web version:
```bash
ffmpeg -i mix51.wav -af "pan=stereo|FL=FL+0.707*FC+0.707*BL|FR=FR+0.707*FC+0.707*BR" lr.wav
```
(This drops the LFE. The `pan` manual says ffmpeg's built-in down-mix, selected with `-ac`, should be preferred unless you have specific needs.) Check loudness after the fold-down.

## Gotchas

- Some specs want 6 discrete mono tracks rather than one 6-channel track. "Track" vs "channel"
  is the most-misread line of a spec.
- Check the layout ffprobe reports for a 6-channel file with no channel mask; do not assume it is 5.1 when it holds six unrelated stems.

## Verify

```bash
ffprobe -v error -show_entries stream=index,codec_name,channels,channel_layout:stream_tags=handler_name -of compact out.mov
```

Then solo each channel (`-af "pan=mono|c0=FC"`) and listen: dialogue only in C, rumble only
in LFE.

## Checked

2026-10-28. Confirmed in the ffmpeg-filters manual and the ffmpeg AudioChannelManipulation wiki: `join` (`inputs`, `channel_layout`, `map=0.0-FL|...`), `channelmap` (index form `1|2|0|5|3|4:5.1`), `pan` syntax (`out=gain*in+...`, `c0` numbered outputs), `5.1(side)` layout name. Fixed: the film-order `channelmap` example used channel names, which refer to the input's assumed layout rather than file order; replaced with the index form. Removed: Pro Tools and LtRt statements, the guess-from-channel-count claim, the 'hotter' fold-down claim.

2026-11-01 run check: `join` built 5.1 and `5.1(side)` files (ffprobe: 6 channels, layouts `5.1` and `5.1(side)`); the three-track MOV probed as pcm_s24le 5.1, stereo, 5.1; the `pan` fold-down gave 2 channels. `channelmap=0|2|1|5|3|4:5.1` was checked with six stems at distinct levels (astats RMS per channel): input index 2 landed in output channel 2 (position 1), input 5 in output channel 3 and so on, exactly as the skill says; `pan=mono|c0=FC` returned the level of the channel labelled FC. Fixed the track-label option (`title` is dropped in MOV).

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manuals for the options above.
