---
id: mind-self.learning-how-to-learn.spaced-repetition.designing-a-spaced-review-schedule
name: designing-a-spaced-review-schedule
category: mind-self
field: learning-how-to-learn
product: spaced-repetition
tags: [learning-how-to-learn, spaced-repetition, spacing-effect, forgetting-curve, ebbinghaus, expanding-intervals, leitner-box, leitner-system, srs, anki, supermemo, flashcards, prompt-design, minimum-information-principle, leeches, review-debt, paper-flashcards, retention, long-term-memory, study-habits]
level: practitioner
status: draft
description: "Run spaced review that actually sticks: expanding intervals, atomic prompts, a paper Leitner box or SRS, daily review budget, leech handling and recovering from a backlog."
sources: ["Ebbinghaus, Memory (1885)", "Cepeda et al., Spacing effects in learning, Psychological Science (2008)", "Wozniak, Effective learning: Twenty rules of formulating knowledge (SuperMemo, 1999)", "Leitner, So lernt man lernen (1972)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing a spaced review schedule

**Goal:** remember chosen material for months or years for a few minutes a day, by
reviewing each item just as it is starting to fade instead of cramming it all at once.

## Why it works (in one paragraph)
Forgetting is fast at first, then slows. Each successful, slightly effortful retrieval
makes the memory last longer, so the next review can wait longer. Spacing beats massed
study for the same total time in hundreds of studies; the exact best gap depends on how
long you need to remember, and a rough rule from Cepeda et al. (2008) is that the
optimal first gap is around 10–20% of the retention interval you care about. Treat that
figure as a starting point, not a law.

## 1. Choose what earns a place
Only schedule things you will genuinely need to recall *without looking them up*:
vocabulary, formulas, anatomy, definitions, key facts for an exam. Do not card things
you don't yet understand — understand first (see
`mind-self.learning-how-to-learn.elaboration-and-explanation-technique`), then card the
pieces.

## 2. Write prompts that review cleanly
- **One fact per prompt** (the "minimum information principle"). "Capital of
  Mongolia?" not "Tell me about Mongolia".
- **Unambiguous answer.** If two answers would be right, add context to the prompt.
- **Both directions only when you need both** (word → meaning and meaning → word are two cards).
- **Cloze for lists and sentences**, but break long lists into overlapping small chunks.
- **Add a hook** — an image, example or mnemonic — to anything that keeps failing.

## 3. Pick the scheduler
- **Software (Anki and similar):** the algorithm handles intervals; your job is honest
  grading. Tool specifics live under languages-linguistics skills.
- **Paper Leitner box:** five compartments. New cards go in box 1. Review box 1 daily,
  box 2 every 2–3 days, box 3 weekly, box 4 fortnightly, box 5 monthly. A correct card
  moves up one box; a missed card goes **back to box 1**. Exact gaps are a convention —
  adjust them, but keep them expanding.
- **Plain list or calendar:** for a handful of big items (a speech, a procedure),
  review at roughly 1 day, 3 days, 1 week, 2–3 weeks, 2 months.

## 4. Set a daily budget
Reviews compound: every new card generates future reviews. A sustainable rule is to
cap new cards (often 10–20 a day in SRS software) so that daily review stays within a
fixed time box (15–30 min). Review **every day**, even briefly; skipping days is how
backlogs start.

## 5. Grade honestly
Say or write the answer *before* flipping. "I sort of knew it" is a miss. Inflated
grades push weak items out to long intervals where they die quietly.

## 6. Handle leeches
A leech is a card you keep failing (SRS tools often flag one after ~8 lapses). Don't keep
drilling it. Rewrite it: split it, add context, add a mnemonic, or contrast it with the
item you keep confusing it with. Delete it if you no longer need it.

## 7. Recover from a backlog
After a break you may face hundreds of due cards. Stop adding new cards, then clear the
backlog in daily chunks (oldest-due or most-important first). Don't reset everything —
most items will still be partly remembered.

## Gotchas
- Spaced repetition maintains memory; it does not create understanding.
- Recognising the answer on the back is not recall. Retrieve first.
- Huge decks downloaded from others are often poorly written for *your* needs; your own
  cards usually stick better (commonly reported, evidence modest).
- Interval numbers above are conventions and reasonable defaults, not tested optima for
  every learner — note your own retention rate and tune.

## Verify
- [ ] Every prompt has one clear answer and tests one idea.
- [ ] You retrieve before revealing and grade misses as misses.
- [ ] New-card intake is capped so daily review fits your time box.
- [ ] Intervals expand after success and reset after failure.
- [ ] Leeches are rewritten, not just repeated.
- [ ] Spot-check: of 20 random mature items, you recall roughly 85–90% cold.
