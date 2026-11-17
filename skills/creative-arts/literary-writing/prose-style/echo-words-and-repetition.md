---
id: creative-arts.literary-writing.prose-style.echo-words-and-repetition
name: echo-words-and-repetition
category: creative-arts
field: literary-writing
product: prose-style
tags: [literary-writing, prose-style, line-level-editing, sentence-level-editing, echo-words, word-repetition, crutch-words, word-frequency, once-is-usually-enough, browne-and-king, self-editing]
level: practitioner
status: draft
description: "Find and fix unintended repetition: echo words close together, personal crutch words found by word-frequency analysis, repeated beats and gestures."
sources: ["https://en.wikipedia.org/wiki/Repetition_(rhetorical_device)", "https://en.wikipedia.org/wiki/Word_lists_by_frequency"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Echo words and repetition

**Goal:** remove repetition the reader notices but you didn't intend. Browne & King's
chapter "Once Is Usually Enough" covers repeated words, repeated information and
repeated beats.

## Kinds of unintended repetition
1. **Echo words:** the same distinctive word within a few lines ("the *ancient* door...
   her *ancient* aunt"). Common words (said, the, was) don't echo; distinctive ones do.
2. **Crutch words:** your personal habits across the book — *just, really, very, that,
   suddenly, actually, somehow, slightly, began to, turned, nodded, smiled, sighed, shrugged*.
3. **Repeated gestures and beats:** characters nodding, grinning, looking every page.
4. **Repeated information:** telling the reader something already shown or already told
   in an earlier chapter ("As we know, he hated his father").
5. **Repeated sentence structures** (see `sentence-variety-and-length`).

## Finding them
- **Word frequency:** paste the manuscript into a word-frequency tool, or in Python:
  `collections.Counter(re.findall(r"[a-z']+", text.lower())).most_common(300)`.
  Ignore function words; investigate content words high on the list.
- Search each crutch word and check every hit.
- Read aloud (echoes are easy to hear; see `read-aloud-revision`).

## Fixing
- Cut first (most crutch words add nothing).
- Replace with a more precise word only if the replacement is better, not just different
  ("elegant variation" — calling a lemon "the yellow fruit" — is worse than repetition).
- Replace stock gestures with specific actions or nothing.
- Cut the second telling of any information.

## Keep deliberate repetition
- Rhetorical repetition (anaphora), motifs, refrains, characters' verbal tics, and
  repetition for clarity in technical passages.

## Verify
- [ ] Frequency list reviewed; crutch words reduced.
- [ ] No distinctive word repeats within a paragraph unintentionally.
- [ ] Gesture count (nods, smiles, sighs) checked across the book.
