---
id: languages-linguistics.language-learning.spaced-repetition.anki-deck-design-for-language-study
name: anki-deck-design-for-language-study
category: languages-linguistics
field: language-learning
product: spaced-repetition
tags: [spaced-repetition, anki, ankidroid, ankimobile, srs, flashcards, fsrs, sm-2, note-types, card-templates, cloze, cloze-deletion, desired-retention, learning-steps, leeches, shared-decks, deck-options, add-ons, tts, language-learning, vocabulary, sentence-cards, recognition-cards, production-cards]
level: practitioner
status: draft
description: "Set up Anki for language study: a sentence note type with recognition/production cards, FSRS with sensible desired retention, daily limits, leech handling and shared-deck hygiene."
sources: ["Anki Manual (docs.ankiweb.net) — note types, deck options, FSRS", "open-spaced-repetition/fsrs4anki project documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anki deck design for language study

**Goal:** an Anki setup where reviews stay under ~30–45 minutes a day, cards test what you
actually need (understanding vs saying), and the scheduler is configured rather than left
on defaults you never chose.

*Written against Anki 23.10+ desktop (FSRS built in). Menu names shift between versions and
between AnkiDroid/AnkiMobile — confirm on your build.*

## 1. One note type, several cards
Make a note type (Tools › Manage Note Types › Add › clone "Basic") with fields:
`Sentence`, `Target` (word/chunk), `Reading` (furigana/pinyin/stress), `Meaning`,
`Audio`, `Notes`, `Source`.
Card templates:
- **Recognition**: front `{{Sentence}}` with `{{Target}}` styled bold; back meaning, reading,
  `{{Audio}}`. Every note gets this.
- **Production**: front `{{Meaning}}` (+ sentence with target blanked); back the target.
  Make it conditional so it only generates when you fill a flag field, e.g.
  wrap the front in `{{#MakeProduction}}…{{/MakeProduction}}`. Empty front = no card.
- **Listening** (optional): front `{{Audio}}` only.
Separating *notes* (facts) from *cards* (tests) lets you fix a typo once and every card updates.

Cloze (`{{c1::word}}`) is good for grammar endings and particles; avoid clozing more than
one item per card.

## 2. Scheduler settings (Deck › Options)
- **Turn on FSRS** (Deck options › FSRS). After a few weeks/~1,000 reviews, press
  *Optimize* so parameters fit your own history; re-optimise every month or two.
- **Desired retention**: 0.85–0.90 for most learners. 0.95+ roughly doubles workload
  for a few points of recall; below 0.80 you forget too much to read fluently.
- **Learning steps**: short, e.g. `10m 1d` (with FSRS, steps over a day are discouraged).
- **New cards/day**: 10–20. **Maximum reviews/day**: high (e.g. 9999) — capping reviews
  just hides a backlog.
- **New card order**: by deck/position if the deck is frequency-ordered.
- **Bury siblings**: on, so recognition and production of the same note aren't seen the same day.

## 3. Grading discipline
With FSRS, use **Again** when you didn't know it, **Good** when you did. *Hard* means
"got it, with real effort" — not "wrong but close". Misusing Hard as a soft fail
corrupts the model. Easy sparingly.

## 4. Leeches
Default: tagged `leech` and suspended after 8 lapses. Review the leech list weekly:
rewrite the card (better sentence, mnemonic, image), split it, or delete it. A leech is a
bad card more often than a bad memory.

## 5. Shared decks
Shared decks (ankiweb) are fine for a frequency core, but: check audio licensing and
quality, delete cards for words you already know (suspend them rather than spamming Easy),
and expect errors. Mined cards from your own input stick better than imported ones.

## 6. Sync and backup
Sync before switching devices; on a conflict, choose upload/download deliberately. Anki
keeps automatic backups (File › Switch Profile area / preferences) — know where before
you need one.

## Gotchas
- Adding 50 new cards a day "to catch up" produces a review wall ~1–2 weeks later.
- Missing a few days: do the backlog oldest-overdue first, pause new cards until clear.
- Too much on the back (full conjugation tables) makes grading fuzzy — keep it to what the
  front asks.
- Two-sided "Basic (and reversed)" for everything doubles load; production cards only for
  words you need actively.
- Media files added outside Anki don't sync; use the editor or the media folder correctly
  and run Tools › Check Media.

## Verify
- [ ] FSRS is enabled and optimised on your own review history; desired retention is a chosen number.
- [ ] Your actual true retention (Stats, or the FSRS helper) is within a few points of the target.
- [ ] Daily reviews are stable or falling week on week, not climbing indefinitely.
- [ ] Production cards exist only where flagged; siblings are buried.
- [ ] Leech list reviewed and each leech rewritten, split or deleted.

Related: `languages-linguistics.language-learning.vocabulary-building.frequency-lists-and-sentence-mining`,
`mind-self.learning-how-to-learn.spaced-repetition.designing-a-spaced-review-schedule`.
