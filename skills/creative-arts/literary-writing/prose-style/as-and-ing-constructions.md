---
id: creative-arts.literary-writing.prose-style.as-and-ing-constructions
name: as-and-ing-constructions
category: creative-arts
field: literary-writing
product: prose-style
tags: [literary-writing, prose-style, line-level-editing, sentence-level-editing, as-ing-constructions, participial-phrases, simultaneity, dangling-modifier, sophistication, browne-and-king, self-editing]
level: practitioner
status: draft
description: "Fix overused 'as' and '-ing' constructions: impossible simultaneous actions, buried main actions, dangling participles and the monotony they cause."
sources: ["https://en.wikipedia.org/wiki/Participle", "https://en.wikipedia.org/wiki/Dangling_modifier"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# As- and -ing constructions

**Goal:** remove a family of tics that Browne & King (*Self-Editing for Fiction
Writers*, "Sophistication") flag as marks of unpolished prose: sentences built on
"as" clauses and participial ("-ing") phrases.

## The problems
1. **Impossible simultaneity:** *Pulling off her coat, she crossed the room and
   opened the window.* — she can't do all at once. *-ing* phrases imply simultaneity.
2. **Buried action:** the important action goes in the subordinate part: *As the bomb
   exploded, she reached for her coffee.* The explosion deserves a main clause.
3. **Reversed cause and effect:** *She screamed as the knife flashed.* — the stimulus
   should come first (see
   `creative-arts.literary-writing.plot-structure.motivation-reaction-units`).
4. **Dangling participles:** *Walking into the kitchen, the smell of toast was
   overwhelming.* — the smell isn't walking.
5. **Monotony:** many sentences shaped "-ing X, she Y" or "As X, Y" become a drumbeat.

## Fixes
- Split into sequential main clauses: *She pulled off her coat. She crossed the room
  and opened the window.*
- Promote the important action: *The bomb exploded. Her hand was still on the coffee cup.*
- Order stimulus before reaction: *The knife flashed. She screamed.*
- Fix danglers by making the subject the actor: *Walking into the kitchen, she smelled toast.*

## Procedure
- Regex search for sentences starting with an -ing word: `(^|[.!?]\s+)[A-Z][a-z]+ing\b`.
- Search `\bas\b` and check temporal uses ("as she walked").
- Keep the genuinely simultaneous (*Humming, she washed the dishes*) and the occasional
  one for rhythm.

## Verify
- [ ] No impossible simultaneous actions.
- [ ] No dangling participles.
- [ ] Important actions in main clauses.
- [ ] -ing openers appear only occasionally per page.
