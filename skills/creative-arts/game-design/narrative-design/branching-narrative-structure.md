---
id: creative-arts.game-design.narrative-design.branching-narrative-structure
name: branching-narrative-structure
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, interactive-fiction, branching-narrative, branch-and-bottleneck, foldback, hub-and-spoke, choices, consequences, state-tracking, flags, variables, ink, inky, twine, yarn-spinner, articy-draft, dialogue-tree, quest-design, rpg, visual-novel, combinatorial-explosion]
level: practitioner
status: draft
description: "Choose and control a branching story structure (branch-and-bottleneck, hub, open state) so choices feel meaningful without the content cost of a full tree; tools Ink, Twine, Yarn."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Branching narrative structure — meaningful choice at an affordable cost

**Goal:** pick a branching shape that delivers the *feeling* of consequence the game
needs, tracked with state so you write reactions, not whole parallel stories.

## 1. Understand the cost
A pure tree doubles content per binary choice: 10 choices deep = ~1,000 endings.
Nobody ships that. Every practical structure is a way to **merge branches back** while
remembering what happened.

## 2. The standard shapes
| Shape | How it works | Good for | Cost |
|---|---|---|---|
| **Branch and bottleneck** (foldback) | Paths split, then rejoin at key story beats | Linear story games, visual novels | Low–medium |
| **Hub and spoke** | Central place; player picks order of self-contained episodes | RPG towns, investigation games | Medium; order-independence is hard |
| **Gauntlet / parallel paths** | Mostly linear, short side branches that fail or rejoin fast | Action games with light choice | Low |
| **Open state / storylet** | Small content units unlocked by conditions on world state | Sandbox, life sims, emergent story | High up-front tooling, scales well |
| **Multiple endings** | Mostly shared path; state decides which ending plays | Most choice-driven games | Low if endings are short |
Most shipped games mix these: bottleneck at act boundaries, hubs inside acts.

## 3. Track state, then pay it off
- Store choices as **flags and variables** (`spared_guard = true`, `trust_mira += 1`),
  not as separate script branches.
- Pay off state through cheap reactions: a changed line of dialogue, a character
  who remembers, an item present or missing, a different final scene. One acknowledged
  callback many hours later feels more meaningful than a big immediate branch.
- Keep a **state table**: every flag, where it's set, every place it's read. A flag
  set but never read is a broken promise; one read but never set is a bug.

## 4. Writing the choices themselves
- Make the options differ in **values**, not just tone ("protect the town" vs
  "chase the thief", not "polite yes" vs "rude yes"), unless tone is the mechanic.
- Give enough context to choose. A choice the player couldn't reason about feels
  arbitrary when it bites.
- Signal weight when it matters (a pause, a UI cue), and be honest — telegraphing
  "this will be remembered" and then not paying it off erodes trust.
- Label options so players can predict the line they'll say; a surprising
  paraphrase is a common complaint in dialogue wheels.

## 5. Tools
- **Ink / Inky** (inkle): text scripting with knots, diverts, variables; integrates
  with Unity. **Twine**: visual passage graph, good for prototyping and web output.
  **Yarn Spinner**: dialogue scripting popular with Unity indies. **articy:draft**:
  commercial database/flow tool for large teams. Pick one that exports to your engine
  before writing at volume.

## Gotchas
- **Combinatorial bugs:** two flags = four states, ten = 1,024. Test the
  combinations that actually reach payoff scenes; write automated playthrough scripts
  if the tool allows (Ink can be driven from code).
- **Hub order:** if episodes can be done in any order, every reference between
  them must be conditional. Lock order where references matter.
- **Localisation and VO multiply cost** per line; a reaction line in 10 languages with
  voice is not "cheap". Count lines early.
- Structure names vary between writers (e.g. "foldback" vs "branch and bottleneck");
  the shapes are widely described in narrative-design writing, but the table's cost
  ratings are judgement, not measured.

## Verify
- [ ] Structure chosen and drawn as a flowchart, with merge points marked.
- [ ] State table lists every flag with its setter and readers; no orphans.
- [ ] Each major choice has at least one later payoff a player will notice.
- [ ] Choices differ in values or goals, and the player had context to decide.
- [ ] Line count estimated including localisation/voice.
