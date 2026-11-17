---
id: computing-software.game-programming.game-ai-programming.rule-based-systems-and-dynamic-dialogue
name: rule-based-systems-and-dynamic-dialogue
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, rule-based-system, production-rules, rete, fuzzy-pattern-matching, dynamic-dialogue, response-rules, blackboard, utility-ai, game-programming]
level: practitioner
status: draft
description: "Use rule-based systems in games: facts and production rules, most-specific-match selection (Valve's dynamic dialog), efficient matching, and authoring/debugging large rule sets."
sources: ["https://www.gdcvault.com/play/1015528/AI-driven-Dynamic-Dialog-through", "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rule-based systems and dynamic dialogue

**Goal:** let designers express behaviour as many independent `IF facts THEN response` rules, and
have the system pick the best matching rule at runtime (Millington ch. 5.8; Elan Ruskin's GDC 2012
talk on Left 4 Dead 2's dialogue system).

## Model
- **Facts**: key/value pairs in a query, merged from several sources: the speaker (`Who=Coach`,
  `Health=low`), the world (`Map=swamp`, `TimeSinceCombat=30`), the event (`Concept=SeeZombie`), and
  memory (`SaidZombieLine=1`).
- **Rules**: a list of criteria (`Concept == SeeZombie`, `Health < 30`, `Map == swamp`) + a response
  (a line to say, an action) + side effects (write facts, e.g. remember it was said).
- **Selection**: among rules whose criteria all match, pick the one with the **most criteria**
  (most specific). Ties broken randomly or by weight.

## Why "most specific wins" scales
Designers add a general rule (`Concept=SeeZombie` -> generic line) and then special cases
(`+ Who=Coach + Map=swamp` -> joke) without editing existing rules. Thousands of rules stay
manageable because they never reference each other.

## Efficient matching
- Group rules by a mandatory key (the `Concept`) to cut candidates.
- Sort each rule's criteria by selectivity; reject early.
- Pre-sort candidate rules by criteria count descending: the first full match wins, stop there.
- For large forward-chaining systems, the Rete algorithm caches partial matches; game dialogue
  systems usually do not need it.

## Memory and anti-repetition
Responses write facts back (`LastSaidSeeZombie = now`, `CountSeeZombie += 1`), and rules include
criteria on them (`TimeSinceSaid > 60`), giving cooldowns and "first time" lines purely through
rules. Rules can also fire follow-up concepts with delays to make two characters converse.

## Authoring and debugging
- Rules in spreadsheets or text files (designer friendly), compiled to a binary at build time with
  validation (unknown fact names, unreachable rules shadowed by more specific ones).
- Debug console command to print the query facts and the top N matching rules with scores for the
  last event.
- Same machinery works for barks, animation selection, ambient behaviours and even quest reactions.

## Verify
- [ ] Every concept has a general fallback rule (no silent events).
- [ ] Validator reports rules that can never be selected.
- [ ] Debug dump shows why a specific line was chosen for a recorded event.
