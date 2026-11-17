---
id: creative-arts.animation.blender.image-sequence-to-video
name: image-sequence-to-video
category: creative-arts
field: animation
product: blender
tags: [blender, output-settings, image-sequence-to-video, sequence-to-video, ffmpeg-encoding, vse]
level: practitioner
status: docs-checked
description: "Turn a rendered image sequence into a video inside Blender's VSE: Add Image/Sequence, frame rate, View Transform on import, Video output settings, plus an ffmpeg CLI alternative."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/image.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
  - https://ffmpeg.org/ffmpeg-formats.html
  - https://ffmpeg.org/ffmpeg-codecs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# image-sequence-to-video

Goal: a playable MP4/MOV from an EXR or PNG sequence, quickly and with correct colour. The manual recommends this route: render image sequences first, then encode, so a failed render can resume and encoding options can be retried in seconds.

## In Blender (new file or a new scene)

1. Video Editing workspace (File > New > Video Editing).
2. Set the scene **Frame Rate** (Output Properties > Format) to the render's rate and the resolution to the sequence's size first.
3. Sequencer: **Add > Image/Sequence**, browse to the folder, press A to select all frames, then Add Image Strip. **Import As**: Auto Detect treats consecutively numbered files as one sequence. **Use Placeholders** keeps the strip length correct when some frames are missing (placeholder frames show pink in the preview).
4. **Set View Transform** (an Add Image Strip option) picks a View Transform from the media's colour space; the manual says Standard is usually right for display-referred media, and a wrong transform gives inaccurate colour. Set Frame End to the strip's end.
5. Output Properties > Output: Media Type **Video**, then the **Encoding** panel: Container (for example MPEG-4), Video Codec (for example H.264), Output Quality, Encoding Speed, and an audio codec if there is sound (default is No Audio). Post Processing > Pipeline > **Sequencer** must be enabled so the strips are rendered.
6. Render > Render Animation (Ctrl F12).

## ffmpeg alternative

```bash
ffmpeg -framerate 24 -start_number 1001 -i sh010.%04d.png -c:v libx264 sh010.mp4
```
`-framerate` (default 25) and `-start_number` are options of ffmpeg's image2 demuxer; the filename pattern uses a printf-style number such as `%04d`. See the libx264 section of the ffmpeg codecs documentation for quality and pixel-format options. EXR input needs a colour transform, so it is easier to go through Blender or render PNGs first.

## Gotchas

- If the sequence's size differs from the render resolution, the sequencer auto-scales it; use the Fit Method option or Crop/Offset on the strip to control that.
- Some codecs do not work with arbitrary dimensions; the manual advises sticking to common dimensions and checking codec limits.
- Not every container and codec pair is compatible; if encoding errors appear, check the pair.

## Verify

Play the result: duration equals frames divided by fps, and colours match the frames viewed in the Image Editor.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): strips/image.rst (Add > Image/Sequence, A selects all, Import As, Use Placeholders, Fit Method, Set View Transform), render/output/properties/output.rst (Media Type Video, Encoding panel, audio default, codec/dimension note, render-images-first tip) and post_processing.rst (Sequencer pipeline). ffmpeg: image2 demuxer options framerate and start_number and the libx264 encoder entry (ffmpeg-formats and ffmpeg-codecs docs). Removed unconfirmable claims: Ctrl Home range shortcut, frame-numbering and missing-frame behaviour, `-crf`/`-pix_fmt` playability advice, even-dimension rule. Method: documentation only; no commands were run.
