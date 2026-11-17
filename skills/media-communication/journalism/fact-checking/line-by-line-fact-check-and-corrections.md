---
id: media-communication.journalism.fact-checking.line-by-line-fact-check-and-corrections
name: line-by-line-fact-check-and-corrections
category: media-communication
field: journalism
product: fact-checking
tags: [fact-checking, journalism, verification, pre-publication-check, line-by-line, primary-source, source-tracing, document-verification, image-verification, reverse-image-search, exif, quote-verification, statistics-check, corrections, corrections-policy, errata, editors-note, accuracy, misinformation, osint]
level: practitioner
status: draft
description: "Check a story line by line before publication: mark every checkable claim, trace each to a primary source, verify images and quotes, and run a clean corrections process after."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Line-by-line fact check and corrections

**Goal:** every factual statement in the piece traces to a source you can name and
show, and when something slips through, the correction is fast, visible and honest.

## 1. Mark up the copy
Print or copy the draft and highlight **every checkable unit**: names, titles, ages,
dates, numbers, places, quotes, characterisations ("the largest", "first", "rarely"),
causal claims and anything implied by juxtaposition. A 1,500-word feature typically has
100+ units; that's normal.

Ask the reporter for their **annotated draft** or source list: each claim linked to a
note, recording, document or URL. Missing backup = flag, not assume.

## 2. Source hierarchy — trace to the origin
1. **Primary documents** (court filing, dataset, contract, the actual study) beat
2. **Direct, named witnesses** beat
3. **Reputable secondary reporting** (cite it; inherited errors are still your errors) beat
4. **Anything else** (Wikipedia, aggregators, press releases) — leads only.

Gotchas:
- Press-release statistics often round, cherry-pick a base year, or cite a study that
  says something narrower. Read the study's methods and the exact number.
- "Studies show" in copy → which study, sample size, peer reviewed, preprint?
- Superlatives ("first", "only", "record") are the most-corrected claims. Either find a
  definitive source or soften to "one of the first" with editor agreement.
- Ages and titles change. Check as of publication date.

## 3. Quotes
- Compare against recording or notes, word for word. Fixed grammar is a newsroom-policy
  question; changed meaning is never acceptable.
- Check **context**: the quote shouldn't answer a different question than the copy implies.
- Many checkers call sources to confirm *facts* attributed to them, not to renegotiate
  quotes. Follow your outlet's rule.

## 4. Images, video and documents
- **Reverse image search** (Google Lens, TinEye, Yandex, Bing) to find the earliest copy;
  old photos recirculate as new.
- **Metadata** (EXIF via a viewer or `exiftool`) is a hint only — social platforms strip
  it and it can be edited.
- **Geolocate**: match landmarks, signage, shadows and weather to the claimed place/time.
- **Documents**: check fonts, letterheads, dates, internal consistency; contact the
  purported author/issuer to confirm. Leaked documents get a second independent source
  wherever possible.

## 5. Numbers
Recompute every percentage, change and total yourself. Check the base: "up 50%" from 2 to
3 is not news. Per-capita vs absolute, nominal vs inflation-adjusted, and percent vs
percentage points are the classic slips.

## 6. Log it
Keep a check log: claim → source → status (confirmed / changed / cut / flagged). It is
the record if the story is challenged, and it shows editors what's still open.

## 7. Corrections after publication
- **Fix the copy and say so.** Append a correction stating what was wrong and what is
  right ("An earlier version misstated…"). Don't silently edit — readers and archives
  notice, and it erodes trust more than the error.
- Correct across platforms: social posts, newsletters, syndication partners, push alerts.
- Distinguish **correction** (factual error) from **clarification** (accurate but
  misleading) and **update** (new information) — practice varies by outlet; follow its
  written policy.
- Log root causes; repeated error types point to a process gap.

## Verify
- [ ] Every highlighted unit has a status in the check log.
- [ ] Each statistic was recomputed from the primary source.
- [ ] Every quote matched against recording/notes, in context.
- [ ] Images traced to earliest appearance and location confirmed or caveated.
- [ ] Open flags resolved or explicitly accepted by the editor before publishing.
