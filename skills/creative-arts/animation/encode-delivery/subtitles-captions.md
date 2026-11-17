---
id: creative-arts.animation.encode-delivery.subtitles-captions
name: subtitles-captions
category: creative-arts
field: animation
product: encode-delivery
tags: [encode-delivery, subtitles, captions, srt, vtt, ffmpeg, youtube, accessibility, localization, burn-in, sidecar, forced-narrative, multi-language, timing, reading-speed, sdh]
level: advanced
status: draft
description: "Captions and subtitles for YouTube: generate timed SRT/VTT from the shotlist dialogue, style, burn-in vs sidecar, multi-language, forced narratives, upload."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Subtitles and captions for YouTube delivery

**Goal:** ship every episode with accurate, well-timed captions — for accessibility
(deaf/HoH viewers, sound-off autoplay) and as the base for localization — generated
from data you already have, not hand-typed. The pipeline already knows every line's
text (`line_id`) and timing (the VO duration and Rhubarb cues from
`../pipeline/vo-lipsync-pipeline.md`), so captions are **derived data**, not a
transcription job.

This is a delivery step alongside `youtube-master.md` (the -14 LUFS / H.264 master)
and `probe.md` (QC); it runs after the cut is locked.

---

## 1. Captions vs subtitles vs SDH (get the terms right)

- **Captions (CC)** — the dialogue *plus* non-speech info ([door slams], [tense
  music]), for viewers who can't hear the audio. This is the accessibility deliverable.
- **Subtitles** — dialogue only, assuming the viewer hears sound effects; used for
  translation (a hearing viewer who doesn't speak the language).
- **SDH** — subtitles for the deaf/HoH: subtitle styling + the non-speech cues of
  captions. For YouTube, deliver **captions** (dialogue + key non-speech) as the
  primary track.
- **Forced narrative (forced subs)** — the small always-on subset that must show even
  when a viewer has captions off: a foreign line a character speaks, on-screen text
  that matters, a sign. These burn in or ship as a `forced` track (§6).

---

## 2. SRT and VTT — the two formats you ship

Both are plain text, timed cue blocks. Know the differences:

**SRT** (SubRip) — universal, the YouTube upload format:
```
1
00:00:02,120 --> 00:00:04,480
A new viewer! No, better than that.

2
00:00:04,600 --> 00:00:06,900
Welcome to the show, Ivy!
```
- Numbered cues, `HH:MM:SS,mmm` (comma decimal), blank line between cues.

**WebVTT** (`.vtt`) — the web/HTML5 `<track>` format, YouTube also accepts it:
```
WEBVTT

00:00:02.120 --> 00:00:04.480
A new viewer! No, better than that.
```
- `WEBVTT` header required, `HH:MM:SS.mmm` (dot decimal), supports styling/positioning
  (`::cue`, `line:`, `align:`) that SRT can't.

Rule: **author/generate SRT** (simplest, YouTube-native), convert to VTT for web
embeds with ffmpeg (§7). Don't hand-maintain both.

---

## 3. Generate captions from the pipeline (don't type them)

You already have the words and the timing. Build the SRT from the shotlist + the
per-line VO:

- **Text** comes from each shot's `line_id` → the script line (the exact text fed to
  TTS and to Rhubarb — `vo-lipsync-pipeline` §2). Caption text must match the delivered
  VO word-for-word.
- **Timing** comes from each line's **position in the assembled cut** (shot start
  offset) + the VO clip duration. A cue = `[cut_offset_of_shot, cut_offset +
  line_duration]`. The Rhubarb json already carries `start`/`end` within the line;
  offset them by the shot's position in the episode to get absolute cue times.
- **Non-speech cues** ([music], [thud]) are added from the sound-design pass data
  (`../sound-design/sfx-design.md`, `../sound-design/final-mix.md` cue sheet) — a short
  authored list keyed to timecodes, merged into the SRT.

A ~40-line Python generator that walks the shotlist, reads each line's duration, and
writes numbered SRT cues replaces an afternoon of hand-transcription and stays correct
when a line is re-generated (ADR) — regenerate the SRT, don't re-type it.

```python
# ponytail: one cue per line from shotlist order + VO duration; split only if a line > ~7s or > 2 lines of text
def to_srt_time(t):  # seconds -> "HH:MM:SS,mmm"
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s%1)*1000):03}"
```

---

## 4. Timing and readability rules (the craft)

Captions that are accurate but unreadable fail. The conventions:

- **Reading speed** ≤ ~17 characters/second (≈160–180 wpm). If a cue's text can't be
  read in its duration, split it or trim ([laughs] over a verbatim transcription of a
  laugh).
- **Line length** ≤ ~42 characters per line, **≤ 2 lines** per cue. Break at
  grammatical boundaries (after punctuation, before a conjunction), never mid-word or
  splitting an article from its noun.
- **Minimum duration** ≥ ~1 second even for a one-word cue; **maximum** ~7 seconds —
  split a long line into sequential cues.
- **Gaps:** ≥ 2 frames between consecutive cues so they don't visually butt. Don't let
  a cue linger >~1s past the audio.
- **Sync:** cue **on** at the first phoneme (the VO start, which you have exactly), cue
  **off** at or just after the line end. Captions leading or lagging the voice is the
  amateur tell — your pipeline timing prevents it.
- **Speaker ID** when off-screen or ambiguous: `- Ivy:` prefix or color (YouTube
  supports per-speaker color in styled tracks).

---

## 5. Burn-in vs sidecar (choose per purpose)

- **Sidecar (separate SRT/VTT file)** — the default. Viewer toggles it, YouTube indexes
  it for search, it's multi-language, and it's accessible (screen-reader reachable). The
  master video stays clean. **Ship captions as sidecar.**
- **Burn-in (hardsubbed into the pixels)** — permanent, unremovable, no toggle. Use
  **only** for forced narratives (§6) that must always show, or a platform that won't
  carry a sidecar. Burn-in on a cel show must respect the look: match the outline/
  readability (a subtle box or outline so text survives over bright cel fills).

Most episodes: **sidecar captions + burned-in forced-narrative only.**

ffmpeg sidecar mux (soft subs into an MP4 container — still toggle-able):
```
ffmpeg -i master.mp4 -i ep03.srt -c copy -c:s mov_text -metadata:s:s:0 language=eng out.mp4
```
ffmpeg burn-in (re-encodes video — only for forced subs):
```
ffmpeg -i master.mp4 -vf "subtitles=forced.srt:force_style='FontName=<FONT>,FontSize=28,PrimaryColour=&H00FFFFFF&,OutlineColour=&H80000000&,BorderStyle=3,Outline=2,MarginV=40'" -c:a copy out.mp4
```
`BorderStyle=3` = opaque box behind text (survives busy cel frames); `MarginV` lifts it
off the lower edge / YouTube UI.

---

## 6. Forced narratives

The always-on subset. Keep a separate tiny `ep03.forced.srt` containing only the lines
that must show regardless of caption setting (a foreign-language line, a critical sign).
Then either:
- **burn it into the master** (guaranteed visible everywhere), or
- **upload as a `forced` track** on platforms that support the flag.

Keep it separate from the full caption track so the full track isn't duplicated inside
the forced one, and a viewer with full captions on doesn't see doubled text.

---

## 7. Multi-language (localization)

The English caption SRT is the **localization source**. Per target language:

- **One SRT per language**, same cue numbering and **same timings** — translate text
  in place, never re-time. Timings are expensive to get right; reuse them.
- Expect **text expansion** (German/French run ~20–30% longer than English) — a cue
  that fit at 17 cps in English may bust the reading-speed limit translated; split or
  tighten the translation, don't speed-read.
- Name by BCP-47 code: `ep03.en.srt`, `ep03.es.srt`, `ep03.fr.srt`.
- Convert any to VTT for web: `ffmpeg -i ep03.es.srt ep03.es.vtt`.
- **Translate meaning, not words**, and keep character voice consistent across episodes
  (a localization glossary of character names/terms — same consistency discipline as
  the rest of the show).

---

## 8. Upload to YouTube

- Upload the **sidecar SRT per language** in YouTube Studio > Subtitles (or via the
  Data API `captions.insert`), selecting the correct language per file. YouTube stores
  them as toggle-able CC and indexes the text for search/SEO.
- **Do not rely on YouTube auto-captions** — they mis-hear names (Ivy → "ivy",
  "Hollow Creek" mangled) and have no non-speech cues. Always upload your authored track;
  auto-caption is a fallback, not a deliverable.
- Set the **default/primary** caption language; mark the forced track if used.
- Keep the master itself caption-clean (sidecar), with forced-narrative burn-in already
  baked if you chose that route.

---

## 9. QC the caption track before publish

A caption bug ships as badly as a render bug. Before upload, check:

- **Parse + overlap.** `ffmpeg -i ep03.srt -f null -` reports no errors; no cue's start
  precedes the previous cue's end (overlaps double-stack on screen).
- **Coverage.** Every `line_id` in the shotlist has a cue — a generator that walks the
  shotlist can diff "lines with VO" vs "cues emitted" and flag any missing.
- **Drift at the tail.** Captions drift late over a long episode if cue times were
  accumulated with rounding error — check the *last* line's cue against the actual VO
  position, not just the first. Build absolute times from the shot's cut offset, not by
  summing durations (which compounds error).
- **Over-frame burn-in.** If forced subs are burned in, spot-check them over the
  brightest cel frames and the busiest action — the box/outline must keep them legible.
- **Encoding.** SRT/VTT saved as UTF-8 (so accented localization text and em-dashes
  survive); BOM stripped for strict parsers.

## 10. Common failures (and the fix)

| Symptom | Cause | Fix |
|---------|-------|-----|
| Captions lag more as episode runs | cue times summed with rounding | build absolute times from cut offset (§3, §9) |
| Text cut off / unreadable speed | cue busts 42 char / 17 cps limit | split the cue (§4) |
| Accents show as mojibake | wrong file encoding | save UTF-8 (§9) |
| Doubled forced + full text | forced lines also in full track | keep forced track separate (§6) |
| Translated cue too fast | text expansion ignored | tighten translation / split (§7) |
| YouTube shows wrong words | relied on auto-caption | upload authored track (§8) |
| Burn-in invisible over bright fill | no box/outline | `BorderStyle=3` + outline (§5) |

The through-line: captions are **derived from pipeline data**, so most errors are
generation bugs (timing math, coverage, encoding) caught by QC — not transcription
mistakes. Get the generator right and the track is right every episode.

---

## Verify

1. **Format validity.** The SRT parses (numbered cues, `HH:MM:SS,mmm`, blank-line
   separated); the VTT starts with `WEBVTT` and uses dot decimals. `ffmpeg -i ep.srt`
   reports no cue errors.
2. **Text accuracy.** Each cue's words match the delivered VO exactly (same source text
   as TTS/Rhubarb); re-generating a line (ADR) and re-building the SRT updates the cue.
3. **Timing.** Load the sidecar over the master and scrub: every caption appears on the
   first word and clears near the line end — no lead/lag; non-speech cues land on their
   effects.
4. **Readability.** No cue exceeds ~42 chars/line, 2 lines, or ~17 cps; every cue is on
   screen ≥1s; line breaks fall at grammatical boundaries.
5. **Burn-in vs sidecar.** Full captions ride as a toggle-able sidecar (master pixels
   clean); only forced narratives are burned in, legible over bright cel frames.
6. **Multi-language.** Each language SRT shares the English timings/numbering, uses a
   BCP-47 filename, and no translated cue busts the reading-speed limit.
7. **Upload.** The authored track (not auto-caption) is live on YouTube per language
   with the correct default set.

See `youtube-master.md` (the master this captions), `probe.md` (QC the muxed output),
`../pipeline/vo-lipsync-pipeline.md` (the line text + timing source),
`../sound-design/final-mix.md` (cue sheet for non-speech captions).
