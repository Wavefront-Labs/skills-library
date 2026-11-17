---
id: creative-arts.animation.blender.vse-effects-transitions
name: vse-effects-transitions
category: creative-arts
field: animation
product: blender
tags: [blender, vse-effects, transitions, sound-strips, text-strip, audio-mixing, sequencer, cross, wipe, gamma-cross, adjustment-layer, color-strip, glow, transform, subtitles, titles]
level: practitioner
status: docs-checked
description: "Blender VSE effect strips and transitions: Cross/Gamma Cross/Wipe, blends, Adjustment Layer grading, Text strips for titles and subtitles, Glow/Blur/Speed, sound mixing, keyframed strip properties."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/effects/index.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/transitions/index.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/transitions/wipe.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/text.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/sound.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-effects-transitions

Goal: dissolves, wipes, titles, subtitles, grades and audio mixes directly on the strip timeline.

## Effect strips (Add > Effect Strip, Add > Transition)

Effect strips generate or modify output from other strips. The available types depend on how many strips are selected: none gives generators, one gives single-input effects, two gives dual-input effects.

- **Transitions** (Add > Transition, two strips): **Cross** (crossfade), **Gamma Cross** (uses colour correction for a smoother result than Cross), **Wipe**, and **Sound Crossfade**. The transition uses the overlap of the two strips as its duration. If the strips do not overlap, the last frame of each strip is used.
  - Cross, Gamma Cross and Wipe have **Default Fade** (an automatic linear fade) or **Effect Fader** (keyframe a custom fade, with easings).
  - **Wipe** options: **Transition** (Single, Double, Iris, Clock), **Direction** (In or Out), **Blur Width**, **Angle** (Single and Double). Its duration is the intersection of the two source strips and cannot be adjusted directly; change the strips' bounds instead.
  - **Sound Crossfade** animates the Volume of two overlapping sound strips; it does not create a strip.
- **Dual-input blends**: Add, Subtract, Multiply, Alpha Over and Alpha Under (selection order matters), Color Mix (see vse-color-mix-blend). Every strip also has its own Blend mode and Opacity in the Sidebar.
- **Single-input effects**: Glow, Gaussian Blur (see vse-glow-blur-effects), Speed Control (see vse-speed-control), Multicam Selector (see vse-multicam).
- **Generators**: Color and Text strips, plus the Adjustment Layer strip, which treats all strips below it as its input.
- Effect strips depend on their source strips for position and duration, so move the sources. Exchange the wrong effect type with Strip > Effect Strip > Change Effect Type (same number of inputs); `R` reassigns inputs and `Alt S` swaps the first two inputs.

## Text strips

See vse-text-styling for every field. Text strips support presets (Subtitle, Main Title, Title Corner), multi-line UTF-8 text, Wrap Width, outline, shadow, box and layout controls. Edit text directly in the Preview with `Tab`. All Text strips can be exported as a SubRip file.

- Lower third: a Text strip with its Box enabled, optionally grouped with other strips in a Meta strip (`Ctrl G`).

## Keyframing strip properties

Hover a value and press `I` (the manual uses this for sound properties and opacity). Animated opacity and volume are drawn on the strips and can be hidden with the Animation Curves overlay. Fades are in Add > Fades.

## Sound strips

- Sidebar > Strip > Sound: **Volume**, **Pan** (mono sources only), **Preserve Pitch**, **Display Waveform**; Source panel **Caching**.
- Overlapping sound strips are mixed together; a lower channel never hides a higher one for audio.
- Sound strip modifiers: Echo, Pitch, Sound Equalizer (35 Hz to 20 kHz, plus or minus 35 dB).
- Scene > Audio panel: Volume, Distance Model, Doppler Speed and Factor.

## Modifiers versus effect strips

Strip modifiers (Brightness/Contrast, Color Balance, Curves, Hue Correct, White Balance, Tone Map, Mask, Compositor, camera lens and creative groups) apply per strip, can be stacked and copied with **Copy to Selected**, and most have a Mask Input (a Mask data-block or another strip). Put a shared look on an Adjustment Layer strip. See vse-strip-modifiers.

## Gotchas

- Transitions need two strips; if the strips do not overlap the transition uses each strip's end frame, so overlap them for the intended duration.
- The Wipe effect has no effect when created from a single strip.
- Adjustment Layer strips act on strips below them, not above.
- Cross with a gap between the strips extends the last and first frames, which can cause a pause when a strip is an image sequence.

## Verify

- Gamma Cross between two clips shows a smoother midpoint than Cross.
- Text strip at final resolution is crisp and inside the safe areas (Overlays > Safe Areas).
- An Adjustment Layer with a Color Balance modifier affects every strip below it for its duration.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Effect strip types and how availability depends on the selection, transitions (Cross, Gamma Cross, Wipe, Sound Crossfade) with Default Fade and Effect Fader, Wipe options and fixed duration, no-overlap behaviour, Alpha Over and Under order rule, Adjustment Layer input, Change Effect Type, Reassign Inputs and Swap Inputs shortcuts, text strip options, sound strip options and modifiers, scene audio fields. Removed Over Drop and the Transform effect (not in the 5.2 effect list), the Convert to Float and mixing-level advice, the SRT importer remark and the dBFS figures, which the manual does not state.
- Method: documentation only; no commands were run.
