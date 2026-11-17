---
id: creative-arts.music.ableton-live.slice-to-midi-and-audio-to-midi
name: slice-to-midi-and-audio-to-midi
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, warping, warp-markers, slice-to-midi, audio-to-midi, convert-drums-to-midi, convert-melody-to-midi, convert-harmony-to-midi, drum-rack, sampling]
level: practitioner
status: docs-checked
description: "Use Live's Slice to New MIDI Track and Convert Drums/Harmony/Melody to New MIDI Track: what each creates, slicing options, and how to get accurate conversions."
sources:
  - https://www.ableton.com/en/live-manual/12/converting-audio-to-midi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slice to MIDI and audio-to-MIDI (Live)

**Goal:** turn audio into playable slices or MIDI notes for re-programming, layering or re-voicing.

## 1. Where the commands are
With an audio clip selected, four conversion commands are in the Create menu or the clip's context menu.

## 2. Slice to New MIDI Track
- Splits audio into time-based chunks, each assigned to a MIDI note, without analysing musical content.
- The dialog has a list of slicing divisions and a Slicing Preset chooser. Divisions can be beat resolutions, or based on transients or Warp Markers. You can slice a smaller region of the clip.
- **Preserve warped timing** keeps timing changes from warping in the sliced clip; off, the slices sound like the raw original audio.
- Live limits slicing to 128 slices (the maximum number of chains in a Rack).
- Result: a new MIDI track with a clip holding one note per slice, plus a Drum Rack with one chain per slice; each chain holds a Simpler with its slice.

## 3. Convert commands
| Command | Use for | Result |
|---|---|---|
| **Convert Drums to New MIDI Track** | unpitched, percussive audio; tries to identify kick, snare and hi-hat | new MIDI track with a preloaded Drum Rack |
| **Convert Harmony to New MIDI Track** | polyphonic audio | Instrument Rack playing a piano sound (replaceable) |
| **Convert Melody to New MIDI Track** | monophonic audio | Instrument Rack playing a synth sound; the Synth to Piano macro adjusts timbre |

## 4. Getting accurate results (from the manual)
- Use music with clear attacks; swelling notes may not be detected.
- Use recordings of isolated instruments, since other instruments' notes are detected too.
- Use uncompressed files such as WAV or AIFF; MP3 may give unpredictable results unless high bitrate.
- Adjust transient markers before converting, because Live uses them to place notes.

## Verify
- Play the generated MIDI clip against the original and fix wrong notes by ear.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Converting Audio to MIDI (first 100,000 characters): the four commands and menus, slicing dialog options, Preserve warped timing, 128-slice limit, results of each command, accuracy guidance. Removed: Simpler Slice alternative, "warp first" advice for Convert, cleanup and CPU/RAM advice, uses list (not stated on the page).
Method: documentation only; no commands were run.
