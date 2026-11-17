---
id: creative-arts.music.ableton-live.mpe-editing-in-live
name: mpe-editing-in-live
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-midi-editing, mpe, midi-polyphonic-expression, per-note-pitch-bend, slide, pressure, note-expression, push-3, roli-seaboard, linnstrument, mpe-instruments]
level: practitioner
status: draft
description: "Record and edit MPE in Live: enabling MPE on the controller and track, per-note pitch bend, slide and pressure envelopes in the Note Expression tab, and MPE-capable instruments."
sources: ["https://www.ableton.com/en/live-manual/12/editing-midi/ (Editing MPE)", "https://www.ableton.com/en/live-manual/12/midi-and-key-remote-control/ (MPE controllers)", "https://www.midi.org/midi-articles/midi-polyphonic-expression-mpe"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MPE editing in Live

**Goal:** capture and edit per-note expression from MPE controllers (Push 3, ROLI Seaboard,
LinnStrument, Sensel, Osmose).

## 1. What MPE is
- MIDI Polyphonic Expression gives **each note its own MIDI channel**, so pitch bend, pressure and slide (CC74, Y-axis) can vary per note within a chord.
- Three dimensions in Live: **Pitch bend** (per-note glide/vibrato), **Slide** (CC74, usually timbre/filter), **Pressure** (aftertouch).

## 2. Setup
1. Preferences > Link, Tempo & MIDI: for the controller's input, enable **MPE** mode (Live 11+).
2. Use an MPE-capable instrument: Live's **Wavetable, Sampler, Drift, Meld** (Live 12) and MPE third-party plugins (set the plugin to MPE mode; in the plugin device's context menu enable **Enable MPE Mode** for VST/AU).
3. In the instrument, map Slide and Pressure to useful destinations (e.g. filter cutoff, wavetable position) via its MPE section/mod matrix.

## 3. Recording and editing
- Record as usual; expression is stored per note.
- In the piano roll, open the **Note Expression** tab: select a note to see and draw its pitch bend, slide and pressure envelopes; breakpoints can be moved, deleted, scaled.
- Notes keep their expression when moved or copied; transposing a note keeps relative bends.
- Non-MPE instruments receive only the master channel data; per-note expression is lost.

## 4. Tips
- Reduce pitch bend range consistency issues: set the controller's and instrument's bend range the same (48 semitones is the MPE default for per-note channels).
- Use pressure for swells on pads and slide for timbre to make static synth parts expressive.

## Gotchas
- Pitch bend range mismatch causes wildly out-of-tune glides.
- MPE requires 16 channels; routing MPE into a plugin that's not in MPE mode merges channels and breaks voices.
- Exporting MIDI to other DAWs: MPE data survives in a standard MIDI file only if the receiving software supports it.

## Verify
- Play a chord and bend one note: only that note glides on playback.
- Note Expression lanes show per-note curves after recording.
