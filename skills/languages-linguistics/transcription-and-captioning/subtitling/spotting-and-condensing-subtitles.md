---
id: languages-linguistics.transcription-and-captioning.subtitling.spotting-and-condensing-subtitles
name: spotting-and-condensing-subtitles
category: languages-linguistics
field: transcription-and-captioning
product: subtitling
tags: [subtitling, subtitles, spotting, timing, cueing, in-time, out-time, reading-speed, cps, characters-per-second, line-length, cpl, minimum-gap, frame-gap, shot-changes, condensation, reduction, line-breaks, interlingual-subtitles, template-file, netflix-timed-text-style-guide, subtitle-edit, ooona, ease, srt, ttml]
level: practitioner
status: docs-checked
description: "Spot and write subtitles that read comfortably: in/out times, shot-change snapping, min gaps, CPS/CPL limits, condensing dialogue without losing meaning, and line breaks."
sources:
  - https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide
  - https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spotting and condensing subtitles

**Goal:** time and write subtitles that viewers can read in the time available,
synchronised to speech and cuts, saying what the dialogue means even when it can't say
every word.

> Figures marked Netflix come from its public timed-text guides; every client's guide
> differs — always load its exact numbers into your tool's settings.

## 1. Settings first
Put the client's limits into your subtitle editor (Subtitle Edit, Ooona, EZTitles,
Aegisub etc.) so violations are flagged as you work:
- **Max characters per line (CPL):** Netflix English guide: 42. Other languages and
  clients differ; use the client's number.
- **Max lines:** 2 (Netflix).
- **Reading speed (CPS):** Netflix English guide: up to 20 CPS adult programs, up to 17
  CPS children's programs. Check how your tool counts spaces.
- **Min duration:** Netflix: 5/6 of a second (20 frames at 24 fps); **max** 7 seconds.
- **Min gap** between subtitles and shot-change margins: take them from the client's
  guide (not stated in the pages checked).
- **Frame rate** matching the video exactly (23.976 vs 24 vs 25 matters).

## 2. Spotting (timing)
1. **In-time** on the first frame of speech (some guides allow a few frames early).
2. **Out-time** at end of speech, extended for reading time where the next subtitle
   allows.
3. **Shot changes:** don't cross a cut by a few frames. Either snap the in/out **to** the
   cut or keep **clear of it** by the guide's margin. If speech
   genuinely runs over a cut, crossing it is acceptable; tiny overlaps are not.
4. **Chaining:** when subtitles follow closely, close small gaps to the guide's minimum
   gap so subtitles don't blink off and on.
5. Use the waveform/spectrogram to find speech onsets; check by playing at normal speed.
6. Template files (master English timings) are common in multilingual work: keep the
   template's timing unless the guide allows re-spotting.

## 3. Condensing (when the CPS is too high)
Viewers read slower than people speak, so fast dialogue usually needs reduction.
Cut in this order:
1. **Repetitions, false starts, fillers** (well, you know, I mean).
2. **Vocatives and greetings** already obvious on screen (names when the person is
   visible and addressed).
3. **Redundant information** shown in the picture.
4. **Simplify syntax:** "I'm going to have to leave now" → "I have to go."
5. **Shorter synonyms** and active voice.
Never cut: plot information, jokes' punchlines, names needed later, negation, tone
markers (sarcasm), or anything that makes a later line unintelligible.

## 4. Writing and line breaks
- One idea per subtitle; end subtitles at sentence/clause boundaries where possible.
- Break lines at syntactic boundaries (see closed-captioning skill): Netflix breaks after
  punctuation and before conjunctions and prepositions, and keeps noun with article or
  adjective, first with last name, and verb with subject pronoun, auxiliary, reflexive
  or negation together.
- Two speakers in one subtitle: Netflix uses a hyphen with no space before each speaker's
  line, one speaker per line (`-Ready?` / `-No.`).
- **Ellipses** for trailing off (Netflix: the single ellipsis character for a pause of 2
  seconds or more or trailing dialogue; not when a sentence splits across subtitles with
  a shorter pause).
- Italics: Netflix uses them for narration, unspoken thoughts, sung lyrics, dialogue via
  electronic media when the speaker is not in the scene, and unfamiliar foreign words;
  off-screen speakers are not italicised.
- Don't subtitle what's already readable on screen unless it's a translation (forced
  narratives/inserts follow separate rules).

## 5. Translation subtitles
- Translate meaning and register, not words; cultural references may need
  domestication or explanation within limits.
- Keep consistent names and terminology across episodes; maintain a glossary.

## Gotchas
- Wrong frame rate → subtitles drift progressively out of sync.
- Snapping out-times to the next in-time with **zero** gap — some players merge or
  flicker.
- Condensing so hard that characters sound alike or rude.
- Line breaks splitting names or "the / house".
- Trusting CPS from one tool when the client counts differently.

## Checked
2026-11-01. Confirmed against the Netflix English Timed Text Style Guide (42 CPL, 2 lines, 20/17 CPS, italics, dash, ellipsis rules) and the Netflix General Requirements page (5/6 s minimum, 7 s maximum, line-break rules). Removed: 2-frame minimum gap, 12-frame shot-change margin, CJK 16-character limit, 0.5-1 s linger, 20-40% reduction figure, 13 CPS children figure (page says 17) and the unsourced 37-39 CPL range; min gap and shot-change margins now defer to the client guide.
Method: documentation only; no commands were run.

## Verify
- [ ] Tool's QC check: zero CPS, CPL, duration, gap and shot-change violations (or each
      justified).
- [ ] Full watch-through at normal speed: every subtitle readable before it disappears.
- [ ] Nothing plot-relevant lost in condensed lines (compare against the script).
- [ ] Export matches the delivery format and frame rate.
