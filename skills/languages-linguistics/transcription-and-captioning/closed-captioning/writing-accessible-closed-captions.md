---
id: languages-linguistics.transcription-and-captioning.closed-captioning.writing-accessible-closed-captions
name: writing-accessible-closed-captions
category: languages-linguistics
field: transcription-and-captioning
product: closed-captioning
tags: [closed-captioning, closed-captions, cc, sdh, subtitles-for-the-deaf-and-hard-of-hearing, caption-segmentation, line-breaks, sound-description, music-description, speaker-identification, caption-positioning, cea-608, cea-708, fcc-caption-quality, ofcom, dcmp-captioning-key, wcag, accessibility, srt, webvtt, scc, reading-rate, pop-on-captions, roll-up-captions]
level: practitioner
status: docs-checked
description: "Write closed captions (CC/SDH) for Deaf and hard-of-hearing viewers: segmentation, line breaks, speaker IDs, sound and music descriptions, positioning, rates."
sources:
  - https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide
  - https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing accessible closed captions

**Goal:** captions that give a Deaf or hard-of-hearing viewer the dialogue **and** the
meaningful sound — accurately, in sync, readable and not covering important picture.

> Figures marked Netflix come from its public timed-text guides; check the current
> edition your client cites (DCMP Captioning Key, Ofcom, FCC, house styles).

## 1. Captions vs subtitles
- **Captions (CC / SDH)** assume the viewer **can't hear**: dialogue + speaker IDs +
  sound effects + music + manner of speaking.
- **Subtitles** usually assume the viewer hears but doesn't understand the language
  (see the subtitling skill).
- **Closed** = viewer can toggle; **open** = burned into the picture.

## 2. Accuracy and verbatim
Caption what's said. Edit only when reading rate demands it, and keep meaning, tone and
speaker's register. Don't "correct" dialect or grammar. Include fillers only where they
matter (hesitation that carries meaning).

## 3. Segmentation and line breaks
- **1–2 lines** per caption (pop-on); Netflix English guide: max 42 characters per line,
  2 lines. Other clients set their own limit.
- Break at **natural linguistic boundaries**: after punctuation, before conjunctions
  and prepositions; never split an article from its noun, a name, or a verb from its
  auxiliary.
  - Good: `I told him we'd be late` / `because the train stopped.`
  - Bad: `I told him we'd be late because the` / `train stopped.`
- Prefer a **bottom-heavy** pyramid (shorter top line) when breaks are otherwise equal.
- One sentence per caption where possible; don't run a new sentence's first word on
  the end of a caption.

## 4. Timing
- In-cue at the start of speech; out when speech ends, plus a short linger.
- **Minimum duration:** Netflix 5/6 of a second (20 frames at 24 fps), maximum 7 seconds;
  avoid flashes.
- **Reading rate:** Netflix English guide: up to 20 characters per second for adult
  programs, up to 17 for children's. Verbatim captions on fast speech may exceed the
  limit — the guide decides whether to edit.
- Respect **shot changes**: don't let a caption hang a few frames over a cut.

## 5. Speaker identification
- Use a name or role when the speaker is **off-screen** or ambiguous — follow the house
  style.
- Dash for two speakers in one caption: Netflix uses a hyphen with no space before each
  speaker's line, one speaker per line (`-Ready?` / `-Not yet.`).

## 6. Sounds and music
- Caption sound that **matters for the story**: `[door slams]`, `[phone buzzing]`,
  `[distant siren]`. Skip ambient noise that adds nothing.
- Describe **manner** when it changes meaning: `[whispering]`, `[sarcastically]`.
- Music: describe mood/genre or name it: `[tense music]`, `[upbeat pop music]`; song
  lyrics captioned with ♪ marks: `♪ Lyrics here ♪`.
- Silence that matters: `[no audio]` or `[silence]`.
- Keep descriptions objective and short; present tense.

## 7. Positioning
Move captions to the top (or side) when they'd cover **on-screen text, faces/mouths,
or key action** (lower-thirds, scoreboards, chyrons).

## 8. Formats
Use the format the client's delivery spec names, and validate exports in the target
player.

## Checked
2026-11-01. Confirmed against the Netflix English Timed Text Style Guide (42 characters per line, 2 lines, 20/17 CPS, hyphen for two speakers) and Netflix General Requirements (5/6 s minimum, 7 s maximum, line-break rules). Removed: 32-character 608 limit, 160-180 wpm, 1 s minimum, FCC quality-rule summary (FCC page returned 403), format capability claims and the 708 positioning remark.
Method: documentation only; no commands were run.

## Gotchas
- Captions that cover the speaker's mouth (lip-readers lose information).
- Sound tags for every rustle — noise, not access.
- Losing speaker IDs when a voice is off-camera.
- Auto-captions shipped unedited; they fail accuracy on names and jargon.

## Verify
- [ ] Watch with sound **off**: you can follow who says what and every plot-relevant sound.
- [ ] No caption under ~1 s; reading rate within the guide's limit.
- [ ] Line breaks fall at phrase boundaries; ≤ 2 lines.
- [ ] No caption covers on-screen text.
- [ ] Output validates and displays correctly in the target player.
