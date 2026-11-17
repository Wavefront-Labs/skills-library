---
id: creative-arts.animation.blender.vse-import-media
name: vse-import-media
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-import-media, add-movie-strip, image-strip, sound-strips]
level: practitioner
status: docs-checked
description: "Import media into the VSE correctly: movie strips with sound, frame rate matching, image sequences, still images, sound caching, relative paths and drag-and-drop."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/movie.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/image.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/sound.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# vse-import-media

Goal: media comes in at the right frame rate, in sync, with paths that survive moving the project.

## Add > Movie

Options in the operator panel:
- **Sound**: also import the movie's audio streams as Sound strips (one strip per audio stream).
- **Set Scene Frame Rate**: sets the scene frame rate to the movie's. Use it with the first clip so the edit runs at the footage's rate.
- **Adjust Playback Rate**: plays the video at its original speed regardless of the scene frame rate.
- **Fit Method** (Scale to Fit, Scale to Fill, Stretch to Fill), **Relative Path**, **Replace Selection**, **Start Frame**, **Channel**, **Move Strips**.
- **Set View Transform**: sets a View Transform that suits the imported media's colour space (usually Standard).
- A movie with several video or audio streams gets one strip per stream, synchronised to the timing stored in the file.

## Add > Image/Sequence

- Select the frames by range (click and drag in the file browser), by Shift-click batch, or press A to select all files.
- A single still image makes a strip 25 frames long by default (change the length when adding).
- **Use Placeholders** (image sequences): fills gaps between the first and last frame number with placeholder frames drawn in pink until the files exist. Refresh the sequencer afterwards.

## Add > Sound

- **Cache**: decode the sound into memory.
- **Mono**: merge all channels into one (needed to pan a sound strip).

## Drag and drop

The manual's video editing setup recommends dragging media (movies, images, sounds) into the Sequencer area.

## Gotchas

- The Source panel shows the movie's FPS. If it does not match the scene frame rate, the perceived speed is wrong unless the speed is changed to compensate.
- Enable **Relative Path** when adding media so the strips keep working when the project folder moves.

## Verify

Check that picture and sound strips have the same length, play a clap or lip-sync moment to check sync, and that the scene frame rate matches the footage.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Add Movie options (Sound, Set Scene Frame Rate, Adjust Playback Rate, Fit Method, Relative Path, Set View Transform), one strip per stream, image add options (selection methods, 25 frame default, Use Placeholders), sound Cache and Mono, drag and drop, FPS mismatch note. Replaced the old option name Use Movie Framerate; removed the variable-frame-rate and Make Paths Relative claims, which these pages do not cover.
- Method: documentation only; no commands were run.
