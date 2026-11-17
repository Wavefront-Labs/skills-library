---
id: languages-linguistics.transcription-and-captioning.stenotype.steno-theory-briefs-and-dictionary-maintenance
name: steno-theory-briefs-and-dictionary-maintenance
category: languages-linguistics
field: transcription-and-captioning
product: stenotype
tags: [stenotype, machine-stenography, steno, court-reporting, stenocaptioning, steno-theory, chords, steno-order, stkpwhr, briefs, phrasing, conflicts, untranslates, realtime-dictionary, job-dictionary, cat-software, case-catalyst, eclipse, plover, open-steno, typey-type, speed-building, wpm, 225-wpm, rpr, stenograph-luminex]
level: advanced
status: draft
description: "Machine stenography: steno order and chords, picking a theory, writing briefs and phrases, conflict-free realtime, speed building and dictionary upkeep in CAT software or Plover."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Steno theory, briefs and dictionary maintenance

**Goal:** write English on a stenotype by chording whole syllables or words at once,
building toward realtime speeds (court reporting certifications commonly test up to
225 wpm) with a clean dictionary that translates without conflicts.

> Draft. Steno layout and speed figures are standard; theory details differ between
> theories (e.g. Phoenix, StenEd, Magnum, Plover's theory). Software menu names vary by
> CAT package and version.

## 1. The keyboard and steno order
- Keys (US English): left bank `S T K P W H R`, thumbs `A O` and `E U`, asterisk `*`,
  right bank `F R P B L G T S D Z`, plus the number bar.
- Every chord is written in **steno order**: `STKPWHRAO*EUFRPBLGTSDZ`. A stroke is one
  simultaneous press; all keys pressed must be in that order when written down
  (e.g. `KAT` = "cat").
- Letters missing from the keyboard are **chords**: left `TKPW` = G, `PH` = M, `TPH` = N,
  `SKWR` = J; right `-PB` = N, `-PL` = M, `-BG` = K, `-FP` = ch, `-GS` = -tion (common in many theories). Vowels combine:
  `AOE` = long e, `AEU` = long a, `OEU` = long i (theory-dependent).

## 2. Choose a theory and stick to it
A **theory** is the rule set mapping sounds/spellings to strokes, including how to
resolve **conflicts** (homophones and word-boundary ambiguities). Use the theory your
course teaches; mixing theories creates dictionary conflicts. Free self-study route:
**Plover** (open-source steno engine) with an NKRO keyboard or hobbyist steno machine and
practice sites like Typey Type.

## 3. Briefs and phrases
- **Brief** = a short form for a long or frequent word: e.g. a one-stroke brief for
  "approximately" instead of four strokes.
- **Phrases** = several words in one stroke: "I don't know", "do you", "in the", "ladies
  and gentlemen". Most theories have systematic phrase-building (starter + ender).
- Rules for creating briefs:
  1. Brief what's **frequent in your work** (domain terms, recurring names).
  2. Check the stroke **isn't already used** (search the dictionary) and won't create a
     word-boundary problem with likely neighbouring strokes.
  3. Make it **memorable** (consistent pattern, e.g. first and last sounds).
  4. Drill it 50+ times before using it live.
- Over-briefing early hurts: learn the theory's standard writing first.

## 4. Realtime writing: conflicts and boundaries
For realtime (captions, CART, live court feeds) output must be right **without editing**:
- **Conflict-free:** homophones (their/there/they're, to/too/two) need distinct strokes.
- **Word boundaries:** strokes that can combine into a different word ("in tent" vs
  "intent") need boundary handling — theory rules, or prefix/suffix markers.
- **Untranslates** (strokes with no dictionary entry) show as raw steno — track them.
- Fingerspelling alphabet strokes for unknown names.

## 5. Dictionary maintenance
- **Main dictionary** (your personal one, years of work) + **job dictionaries** (per case,
  client, course) loaded on top.
- After every job: run the CAT software's **untranslate and conflict report**; add
  definitions globally only when they're correct in every context.
- **Prep before jobs:** enter names, terms, acronyms as job entries; test-write them.
- **Back up** dictionaries offsite; export to RTF/CRE (the common exchange format) for
  portability between CAT packages.
- Periodically purge misstroke entries that could fire wrongly.

## 6. Speed building
- Practise at **+10–20 wpm above** your accuracy speed for short bursts, then at
  accuracy speed for clean writing.
- Use graded dictation (literary, jury charge, Q&A testimony) matching your goal.
- Track accuracy: certification tests commonly require ~95% at speed.
- Fix **hesitations**: the stroke you hesitate on every time needs drilling or a brief.

## Gotchas
- Writing "on top of" the theory with ad-hoc briefs that conflict.
- Adding a misstroke globally that later fires in the wrong place.
- Ignoring hand posture and fatigue — injury risk at speed; take breaks.
- No dictionary backup.

## Verify
- [ ] Untranslate rate on a 5-minute dictation is near zero after job prep.
- [ ] Conflict report clean for your common homophones.
- [ ] Each new brief checked for collisions before entry.
- [ ] Dictionary backed up and exported in an exchange format.
