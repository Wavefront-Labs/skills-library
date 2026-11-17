---
id: creative-arts.game-design.narrative-design.tracery-grammar-text-generation
name: tracery-grammar-text-generation
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, tracery, procedural-narrative, generative-text, grammars, procedural-storytelling, kate-compton, twitter-bots, flavour-text]
level: practitioner
status: docs-checked
description: "Generate varied flavour text with Tracery grammars: symbols, rules, modifiers, saved data for consistency, and tests that keep output grammatical and on-tone."
sources:
  - https://github.com/galaxykate/tracery
  - https://tracery.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracery grammar text generation

**Goal:** produce large amounts of varied, on-tone text (item names, NPC descriptions,
rumours, flavour) from a small, maintainable grammar.

Tracery (by GalaxyKate) is a JavaScript text-expansion library that expands grammars
written as JSON-style objects. Other people's ports exist for Ruby, Python, Twine and Node
(listed on tracery.io).

## Grammar basics
```json
{
  "origin": ["#greeting#, traveller. #rumour.capitalize#."],
  "greeting": ["Well met", "Evening", "Hail"],
  "rumour": ["the #place# is haunted", "#name# owes the miller #number# coins"],
  "place": ["old mill", "lighthouse", "chapel"],
  "name": ["Ada", "Bram", "Corin"],
  "number": ["three", "forty", "a hundred"]
}
```
- `#symbol#` expands a rule; modifiers follow a dot: `#animal.capitalize#`, `#animal.a#`,
  `#animal.s#`.
- Each symbol maps to an array of rule strings; a rule can contain further `#symbol#`s.
- **Saved data / actions** keep a choice consistent within one expansion. The README sets
  `hero` once inside an expansion tag, then reuses it:
  `"origin": ["#[hero:#name#][heroPet:#animal#]story#"]` with
  `"story": ["#hero# traveled with her pet #heroPet#."]`.
- Expansion starts from the `origin` symbol by default. In the browser library, a grammar
  comes from `tracery.createGrammar(spellbook)`, `createFlattened()` gives one string.
- For Node.js the README points to a separate library by George Buckenham.

## Design procedure
1. Write 10 hand-made examples of the target text first; extract the pattern.
2. Build rules from the examples; keep lists balanced (a long list next to a short one
   makes the short one repeat visibly).
3. Generate 100+ outputs and read them; fix grammar issues (articles, plurals, gender
   agreement), tone breaks and absurd combinations.
4. Add **constraints** via saved data rather than more rules when consistency matters.
5. Combine with game state by injecting rules at runtime (e.g. set `place` to the
   current region's locations).

## Gotchas
- Combinatorial variety is not perceived variety; distinct structures matter more than
  long word lists.
- Grammar-only generation has no memory of world state beyond what you inject.
- Localisation of grammars is hard (gender, case); plan per language or avoid for
  localised content.

## Checked

2026-11-09. Confirmed against the tracery README on GitHub and tracery.io: JavaScript library,
grammar as key-to-array rules, `#symbol#` expansion, `.capitalize` / `.a` / `.s` modifiers,
saved data with `[key:#rule#]` inside an expansion tag, `origin` default, `createGrammar` and
`createFlattened`, ports list. Removed: the Python code (that port's API is not on the pages
read), the `.ed` modifier, the unconfirmed book claim, and the Kate Compton credit (tracery.io
says GalaxyKate). Design-procedure advice is judgement, not sourced.
Method: documentation only; no commands were run.

## Verify
- [ ] 100+ sample outputs reviewed; error rate acceptable.
- [ ] Saved data used for repeated references.
- [ ] Runtime injection of game state tested.
