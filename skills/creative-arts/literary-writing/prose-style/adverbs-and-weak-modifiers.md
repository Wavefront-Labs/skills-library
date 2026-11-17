---
id: creative-arts.literary-writing.prose-style.adverbs-and-weak-modifiers
name: adverbs-and-weak-modifiers
category: creative-arts
field: literary-writing
product: prose-style
tags: [literary-writing, prose-style, line-level-editing, sentence-level-editing, adverbs, weak-modifiers, ly-adverbs, intensifiers, qualifiers, adjectives, said-adverb, self-editing]
level: practitioner
status: draft
description: "Prune adverbs and weak modifiers: replace verb-plus-adverb with a precise verb, cut intensifiers and qualifiers, fix adverbs in dialogue tags."
sources: ["https://en.wikipedia.org/wiki/Adverb", "https://en.wikipedia.org/wiki/Intensifier", "https://en.wikipedia.org/wiki/On_Writing:_A_Memoir_of_the_Craft"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adverbs and weak modifiers

**Goal:** prose carried by strong nouns and verbs, with modifiers only where they add
information. Stephen King (*On Writing*) and Browne & King both single out adverbs —
especially in dialogue tags — as a sign of telling.

## Targets
1. **Verb + adverb that a better verb replaces:** *walked slowly* -> *ambled / trudged*;
   *said loudly* -> *shouted*; *ate quickly* -> *wolfed*.
2. **Redundant adverbs:** *shouted loudly*, *whispered quietly*, *completely full*.
3. **Adverbs in dialogue tags:** *"Get out," she said angrily.* If the line doesn't
   show anger, fix the line; if it does, the adverb is redundant.
4. **Intensifiers:** *very, really, extremely, so, totally, incredibly* — usually cut or
   replace the phrase (*very tired* -> *exhausted*).
5. **Qualifiers / hedges:** *somewhat, rather, a little, kind of, quite, slightly,
   almost, seemed to* — they sap conviction in narration (fine in a hesitant voice).
6. **Stacked adjectives:** *the tall, dark, brooding, handsome stranger* — one precise adjective or a detail.

## Procedure
1. Search `ly\b` (regex) to find -ly adverbs; also search the intensifier/qualifier list.
2. For each: keep, cut, or replace with a stronger verb.
3. Keep adverbs that add information the verb can't: *she smiled sadly* conveys a
   mixed state; *he answered immediately* matters if timing matters.

## Gotchas
- Thesaurus verbs that are showy or wrong in connotation (*he cachinnated*).
- Removing all adverbs mechanically; the target is redundancy and telling, not a word class.
- Non-ly adverbs (*fast, hard, soon, well*) also need the same check.

## Verify
- [ ] -ly search run; each hit kept only for a reason.
- [ ] Dialogue tags carry no adverbs of manner unless essential.
- [ ] Intensifiers reduced to deliberate uses.
