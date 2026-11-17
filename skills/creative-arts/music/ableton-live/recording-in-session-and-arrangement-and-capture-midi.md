---
id: creative-arts.music.ableton-live.recording-in-session-and-arrangement-and-capture-midi
name: recording-in-session-and-arrangement-and-capture-midi
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, session-view, arrangement-view, capture-midi, session-recording, arrangement-recording, midi-overdub, count-in, record-quantization, punch-in, loop-recording]
level: practitioner
status: docs-checked
description: "Record in Live: Session and Arrangement record buttons, overdub, punch in/out, count-in, record quantisation, loop recording and the Capture MIDI button."
sources:
  - https://www.ableton.com/en/live-manual/12/recording-new-clips/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recording in Session and Arrangement, and Capture MIDI (Live)

**Goal:** capture ideas and takes quickly in either view.

## 1. Setup
- Click a track's **Arm** button to select it for recording.
- Set a count-in from the pull-down menu next to the **Metronome** switch.
- The **Record Quantization** chooser is in the Edit menu. In the Record, Warp & Launch settings you will find the File Type and Bit Depth choosers for new recordings.

## 2. Session View recording
- Click the **Session Record** button to record into the selected scene on all armed tracks.
- Set the Global Quantization chooser to something other than None if you want correctly cut clips.
- With **MIDI Arrangement Overdub** enabled, new MIDI clips mix the signal already in the track with the new input. For Session clips, press Session Record again to deactivate overdubbing.

## 3. Arrangement recording
- Press the Control Bar's **Arrangement Record** button to start recording.
- **Punch-In** and **Punch-Out** switches limit recording to a region.
- While recording into the Arrangement Loop, Live keeps the audio recorded on each pass.

## 4. Capture MIDI
- Play MIDI into a track, then press the **Capture MIDI** button in the Control Bar to get the notes you just played. On Push 1 and Push 2 hold Record and press New; Push 3 has a dedicated Capture button.

## Gotchas
- Input monitoring in Auto mode is on while the track is armed and inhibited while the track plays clips; In monitors always; Off never.

## Verify
- Recorded clips start where you expect; Capture MIDI returns the phrase you played.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Recording New Clips: Arm button, count-in pull-down by the Metronome switch, Record Quantization chooser in Edit menu, File Type and Bit Depth choosers, Session Record, Global Quantization, MIDI Arrangement Overdub, Arrangement Record, Punch-In/Punch-Out, loop-pass retention, Capture MIDI button and Push variants; monitoring modes from the Routing and I/O chapter. Removed: F9 and Capture shortcuts, Fixed Length, Exclusive Arm, take lanes, Capture MIDI tempo detection, preference menu paths, sample-rate claim (not stated on the page).
Method: documentation only; no commands were run.
