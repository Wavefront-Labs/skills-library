---
id: creative-arts.comics-and-sequential-art.comic-scripting.balloon-caption-and-sfx-notation-in-scripts
name: balloon-caption-and-sfx-notation-in-scripts
category: creative-arts
field: comics-and-sequential-art
product: comic-scripting
tags: [comic-scripting, full-script, script-balloon-notation, script-sfx-notation, caption-notation, balloon-modifiers, letterer-handoff, emphasis-markup]
level: practitioner
status: draft
description: "Notate dialogue, captions, balloon types, emphasis and SFX in a comic script so the letterer can set them without guessing: speaker tags, modifiers, bold markup, SFX lines."
sources:
  - https://blambot.com/pages/comic-book-grammar-tradition
  - https://kleinletters.com/Blog/
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Writing+Comics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Balloon, caption and SFX notation in scripts

**Goal:** the letterer can letter the page from the script alone; every balloon type,
emphasis and sound effect is marked, not implied.

## Standard tags (common usage; confirm the publisher's style sheet)
| Script tag | Letterer reads it as |
|---|---|
| `MARA:` | normal speech balloon, tail to Mara |
| `MARA (OFF):` | tail to the panel edge toward where she is |
| `MARA (WHISPER):` | dashed balloon, often smaller text |
| `MARA (BURST):` or `(SHOUT)` | spiky burst balloon, bigger/bolder text |
| `MARA (SMALL):` | small text in normal balloon (muttering) |
| `RADIO:` / `PHONE:` / `TV:` | electronic balloon, jagged tail, sometimes italic |
| `MARA (THOUGHT):` | thought balloon or, more commonly now, a caption in her colour |
| `CAPTION:` | narration/neutral caption |
| `CAPTION (MARA):` | first-person caption in Mara's caption style |
| `LOCATOR:` / `CAPTION (LOCATION):` | location/time caption |
| `SFX:` | sound effect, drawn/lettered display type |
| `CONT'D` / `(LINKED)` | same speaker continues; use a connector |

## Emphasis and type styles
- Mark emphasis with **bold** (or `*asterisks*` / underline in plain-text scripts).
  Letterers convert it to bold italic. Keep it to 1-2 words per balloon.
- `<Spanish>` or angle brackets for translated speech, with a note once:
  "Dialogue in <brackets> is spoken in Spanish."
- Electronic/robot voices: state the effect once in a character note, not every line.

## SFX lines
```
  SFX:    KRAKOOM          (huge, behind the ship, artist may draw it)
  SFX:    tik tik tik      (small, from the clock)
```
- Give size and source in parentheses. Say whether the artist or letterer draws it
  if your team has a convention (big integrated SFX are often drawn by the artist).
- Do not tag every sound. A silent panel can be stronger.

## Multiple balloons from one speaker
Number each balloon separately; a new number = a new balloon. Put one thought per
balloon, and keep balloons short (see the word-count skill
`creative-arts.comics-and-sequential-art.comic-scripting.balloon-word-counts-and-panel-text-budget`).

## Gotchas
- `(V.O.)` and `(O.S.)` are screenplay terms; letterers understand them, but `(OFF)` is
  the comics convention. Pick one and be consistent.
- Ellipses at the end of one balloon and start of the next ("I was--" / "--going") are
  a letterer decision under the house grammar; script them consistently.
- Never put art direction inside a balloon line; it gets lettered.

## Verify
- [ ] Every balloon line has a speaker tag and number; modifiers come from one list.
- [ ] Emphasis markup is consistent and sparse.
- [ ] Every SFX has size/source; translated speech convention stated once.
