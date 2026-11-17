---
id: languages-linguistics.transcription-and-captioning.aegisub.timing-and-styling-subtitles-in-aegisub
name: timing-and-styling-subtitles-in-aegisub
category: languages-linguistics
field: transcription-and-captioning
product: aegisub
tags: [aegisub, subtitles, ass, ssa, advanced-substation-alpha, subtitle-timing, audio-spectrum, waveform, keyframes, timing-post-processor, lead-in, lead-out, snap-to-keyframes, styles-manager, override-tags, pos, an8, typesetting, karaoke, fansubbing, srt-export, ffmpeg-burn-in, libass, video-resolution, playresx]
level: practitioner
status: draft
description: "Aegisub workflow: load video/audio and keyframes, time lines on the spectrum, auto-fix lead-in/out and keyframe snapping, build ASS styles, typeset with override tags, export SRT or burn in."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timing and styling subtitles in Aegisub

**Goal:** time a subtitle script accurately to audio and picture in Aegisub, style it with
ASS, place signs/typesetting, and deliver either a styled `.ass` file or a plain `.srt`.

> Draft. Menu names follow Aegisub 3.2.x as commonly documented; forks (e.g. arch1t3cht's
> Aegisub builds) add features and may rename items. Shortcuts are configurable — check
> *View › Options › Hotkeys*.

## 1. Set up the project
1. *File › Open Subtitles* (or *New*), then *Video › Open Video* and *Audio › Open Audio
   from Video*.
2. *Video › Open Keyframes* (or let Aegisub detect them from the video) — shows scene
   cuts as lines on the audio display.
3. *Subtitle › Properties*: set **script resolution (PlayResX/Y)** to match the video
   (e.g. 1920×1080), or use *From video*. Mismatched resolution makes fonts and
   positions scale unexpectedly.
4. Audio display: switch to **spectrum mode** for speech onsets — consonant energy is
   easier to see than in the waveform.

## 2. Timing workflow
- Type or import the text first (one line per subtitle), then time.
- In the audio display: **left-click** sets start, **right-click** sets end of the
  selection; play the selection (default `S` key in many layouts), adjust, **commit**
  (`G` or Enter, per hotkey settings) to move to the next line.
- Start at speech onset (a few frames early is fine); end when the sound ends.
- Use the **video** to check visible speakers and mouth movement.
- **Join/split** lines: *Subtitle › Split line / Join (concatenate)* or the context menu.

## 3. Timing post-processor (do this before final QC)
*Timing › Timing Post-Processor*:
- **Lead-in / lead-out:** adds time before/after each line (e.g. ~100 ms in, ~250 ms
  out — set your guide's values).
- **Make adjacent subtitles continuous:** closes small gaps (threshold e.g. 300–500 ms)
  so lines don't flicker.
- **Snap to keyframes:** pulls starts/ends to scene cuts within a threshold (in ms
  before/after the cut) so subtitles don't bleed a few frames across a shot change.
Apply to selected lines or all; review results.

## 4. Styles
*Subtitle › Styles Manager*: define styles in the script (and save to a catalog for
reuse):
- **Default** (dialogue): font, size, primary colour, outline (2–3 px at 1080p),
  shadow, bold, alignment **2** (bottom centre), margins.
- **Top** (alignment 8) for lines that would cover on-screen text.
- **Italics** or **Signs** style for off-screen voices/on-screen text translations.
Set the style per line in the edit box. Fonts must be installed on the playback machine
or **attached** (*File › Attachments*) — otherwise renderers substitute fonts.

## 5. Override tags (typesetting)
Inline tags in braces change a single line:
- `{\an8}` top-centre alignment; `{\pos(960,540)}` absolute position.
- `{\i1}…{\i0}` italics; `{\b1}` bold; `{\fs60}` font size; `{\c&H00FFFF&}` colour
  (BGR order in hex!).
- `{\fad(200,200)}` fade in/out ms; `{\frz15}` rotation; `{\blur1}` soft edges.
- `{\k20}` karaoke syllable timing (centiseconds).
The *Visual typesetting tools* on the video toolbar let you drag positions and rotation.

## 6. Export
- **ASS:** keep for players/renderers using libass (mpv, VLC, many web players with
  libass) or for burn-in.
- **SRT:** *File › Export Subtitles* → choose `.srt`; enable *Strip tags* / *Clean tags*
  so ASS overrides don't leak as text. Positioning and styles are lost.
- **Burn-in** with ffmpeg: `ffmpeg -i in.mp4 -vf "subtitles=subs.ass" -c:a copy out.mp4`
  (ffmpeg must be built with libass; fonts available).

## Gotchas
- Colours are **&HBBGGRR&**, not RGB — red is `&H0000FF&`.
- Wrong PlayRes → text sizes off after export/burn-in.
- Variable frame-rate video makes timings drift; convert to constant frame rate first or
  load proper timecodes.
- SRT exports with stray `{\an8}` tags if not stripped (some players honour `{\an8}`,
  others show it).

## Verify
- [ ] *Subtitle › Properties* resolution matches the video.
- [ ] Post-processor applied; no line crosses a keyframe by a few frames.
- [ ] Watch-through: every line readable, none covering on-screen text.
- [ ] Exported SRT contains no `{\` tags (search the file).
- [ ] Fonts attached or confirmed on the playback system.
