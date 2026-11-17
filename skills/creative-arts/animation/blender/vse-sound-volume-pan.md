---
id: creative-arts.animation.blender.vse-sound-volume-pan
name: vse-sound-volume-pan
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, sound-strips, audio-mixing, vse-sound-volume, sound-pan, sound-pitch]
level: practitioner
status: docs-checked
description: "Mix sound in the VSE: strip volume and fades, pan with mono strips, pitch and speed, keyframed volume automation, waveform display, scene volume and sync modes."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/sound.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html#sound
  - https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html#audio
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/modifiers/sound_equalizer.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-sound-volume-pan

Goal: a balanced audio mix inside Blender's edit.

## Sound strip (Sidebar > Strip > Sound)

- **Volume**: hover and press I to animate it (fade music in and out, adjust levels). Animated volume is drawn as an overlay on the strip and reflected in the waveform.
- **Fades**: Add > Fades has Fade In and Out, Fade In, Fade Out, From Current Frame, To Current Frame and Clear Fades. On sound strips they animate the volume.
- **Pan**: only mono sources can be panned. If the source is not mono, enable **Mono** to mix the channels together. For stereo output the range is -1 (left) to 1 (right), 0 is centre. For surround outputs the value times 90 degrees is the angle.
- **Preserve Pitch**: keeps the original pitch when the strip speed changes. Off, speed changes also change pitch. (Blender 4.5.14 sound strips have `volume`, `pan`, `sound_offset` and `show_waveform` but no pitch property, and only the Sound Equalizer sound modifier, so Preserve Pitch, Echo and Pitch are 5.x.)
- **Offset**: offset of the sound from the beginning of the strip in seconds.
- **Display Waveform**: only visible when the Waveforms overlay Type is set to Strip. The overlay Type can also force waveforms On or Off for all strips. Audio over 100 percent amplitude is drawn red.
- Source panel **Caching** decodes the sound into RAM.

## Modifiers

Sound strip modifiers: Echo, Pitch (Semitones or Ratio, Preserve Vocal Formants, Quality High, Fast or Consistent) and Sound Equalizer (range 35 Hz to 20 kHz and plus or minus 35 dB).

## Scene audio (Scene Properties > Audio)

- **Volume** for the scene, **Distance Model**, **Doppler Speed** and **Doppler Factor** (the distance and Doppler settings apply to 3D sound sources).
- Timeline playback options also affect audio behaviour; see the Timeline Playback menu in the manual.

## Mixing

- Overlapping sound strips are mixed together. Unlike picture strips, a lower channel does not hide a higher one.
- Sound Crossfade (a transition) animates the volume of two overlapping sound strips.
- Leave headroom and check the exported mix in an audio tool.

## Gotchas

- Clipping: red in the waveform means over 100 percent amplitude.

## Verify

Export an audio mixdown (see audio-mixdown) and check peaks and loudness with an audio tool.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Volume animation overlay, fades menu (Add > Fades), pan rules and range, Mono, Preserve Pitch, Offset, Display Waveform visibility rule and red clipping, Caching, Echo, Pitch and Sound Equalizer modifier options and EQ range, scene Audio panel fields, overlapping sound strips mixing. Removed the dB equivalence, the old Pitch property, the sync-mode details and the keys-move-with-strip claim, which are not documented in these pages.
- Run note, 2026-11-01, Blender 4.5.14 LTS headless: `SoundStrip` has `volume`, `pan`, `sound_offset`, `show_waveform`; `Sound` has `use_mono` and `use_memory_cache`; the fade operator types are IN_OUT, IN, OUT, CURSOR_FROM, CURSOR_TO and `fades_clear` exists; scene audio has volume, distance model (NONE, INVERSE, INVERSE_CLAMPED, LINEAR, LINEAR_CLAMPED, EXPONENT, EXPONENT_CLAMPED), Doppler speed and factor; the waveform overlay is `waveform_display_type`.
Method: documentation checked against the manual and API pages; part of the claims were run headless in Blender 4.5.14 (see the run note), but other claims describe Blender 5.x features that 4.5.14 does not have, so the status stays docs-checked.
