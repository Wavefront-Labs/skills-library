---
id: creative-arts.animation.blender.audio-scrubbing-lipsync
name: audio-scrubbing-lipsync
category: creative-arts
field: animation
product: blender
tags: [blender, audio-scrubbing-lipsync, dialogue-timing, waveform-display, lip-sync, audio-scrubbing, sequencer]
level: practitioner
status: docs-checked
description: "Time lip sync to dialogue in Blender: Sound strip, waveform display, named phoneme markers and keyed mouth shapes."
sources:
  - https://docs.blender.org/manual/en/latest/editors/timeline.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/sound.html
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/sequencer/display.html
  - https://docs.blender.org/manual/en/latest/animation/markers.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# audio-scrubbing-lipsync

Goal: hand-keyed mouth animation that hits the dialogue precisely, as in traditional lip-sync work.

## Load the audio

In the Video Sequencer use *Add > Sound* and pick the dialogue file. Set the scene frame rate first (`creative-arts.animation.blender.frame-rate-presets`). The Add Sound options include *Cache* (cache the sound in memory) and *Mono* (merge all channels into one). A Sound strip references the original file rather than embedding it, so re-exporting the audio externally and reloading updates the strip. If the file holds several audio streams, one strip per stream is created.

## See the waveform

- Sequencer overlays have a Waveforms setting: On (all strips), Strip (use each strip's *Display Waveform* option) or Off. The per-strip option is only visible when the overlay is set to Strip.
- The waveform *Style* is Full (audio amplitude) or Half (audio level).
- Clipping (over 100% amplitude) is drawn in red in the waveform.
- Keep the Timeline or Dope Sheet beside a Sequencer area so waveform and keys share the same time axis; the Timeline's *Sync Visible Range* option keeps time-based editors panned and scaled together.

## Mark the track

1. Listen through and add markers at key sounds (plosives P/B/M, F/V, wide vowels, accents). Move to the frame and press `M` (Marker > Add Marker); markers always sit on whole frames.
2. Name each marker with the phoneme: select it, press `F2`, type the name, press Return.
3. Key mouth shapes on the markers. Viewers tend to read sync better when the shape is slightly early; judge by playback rather than a fixed offset.
4. Hold closed shapes for M/B/P long enough to read.
5. Markers made in the Timeline, Dope Sheet, Graph Editor, NLA or Sequencer appear in all of them.

## Gotchas

- Audio playback needs an Audio Device other than None in Preferences > System > Sound; with None, audio strips still load and render but do not play live.
- Do not animate to every phoneme; key the shapes that read (open/close rhythm first).
- The Timeline's *Playback* popover holds the audio playback options (scrubbing, sync); read it in the manual's Playback page for your version, it was not checked here.

## Checked

2026-11-09. Confirmed against the Timeline, Sound Strip, Sequencer Display, Markers and Preferences System manual pages: Add > Sound and its Cache and Mono options, external-file reference, one strip per stream, waveform overlay and strip options, red clipping, Full and Half styles, Sync Visible Range, marker add (M), whole-frame markers, rename (F2), shared markers across editors, Audio Device None behaviour. Removed: Scrubbing and Sync to Audio specifics, arrow-key stepping, sample-rate drift advice, Rhubarb and Bake Sound to F-Curves, the fixed 1-2 frame offsets (the Playback page was not read).
Method: documentation only; no commands were run.

## Verify

Playblast (viewport render with audio, `creative-arts.animation.blender.viewport-render-animation`) and watch at full speed: closed shapes land on P/B/M sounds; no visible lag between sound and mouth.
