---
id: computing-software.game-programming.gameplay-programming.branching-dialogue-systems
name: branching-dialogue-systems
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, dialogue-system, branching-dialogue, dialogue-tree, ink, yarn-spinner, localization, game-programming]
level: practitioner
status: draft
description: "Implement branching dialogue: node graph data, conditions and side-effect commands, runtime runner, choice UI, localisation line ids, and integrating ink or Yarn Spinner."
sources: ["https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md", "https://docs.yarnspinner.dev/", "https://www.gdcvault.com/play/1015528/AI-driven-Dynamic-Dialog-through"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Branching dialogue systems

**Goal:** writers author conversations with choices and conditions; code runs them, shows lines and
choices, and applies consequences, with every line localisable.

## Build or buy
Prefer a proven scripting language before inventing a node editor:
- **ink** (inkle): text-first scripts compiled to JSON; runtime `Story` in C# (Unity integration),
  ports for other engines. Loop: `while (story.canContinue) Show(story.Continue());` then
  `story.currentChoices` -> `story.ChooseChoiceIndex(i)`. Variables via `story.variablesState["gold"]`;
  call game code with `EXTERNAL` functions + `story.BindExternalFunction`. Save with
  `story.state.ToJson()`.
- **Yarn Spinner**: `title:` nodes, `<<if>>`, `<<set>>`, custom `<<commands>>`, `DialogueRunner`
  and line providers for Unity/Godot; built-in line ids (`#line:abc123`) for localisation.
- Custom graphs only when you need tight engine tooling; then copy their model.

## Model (custom or to understand the tools)
```
Node    id, speaker, lineId (localisation key), conditions [expr], commands [cmd], next | choices
Choice  lineId, conditions [expr], target nodeId, once: bool
```
- Conditions read game state through a narrow interface (`HasFlag`, `GetInt`, `HasItem`), never
  arbitrary objects, so scripts stay testable.
- Commands (`give_item`, `set_flag`, `start_quest`, `play_anim`) are registered by name; the runner
  validates at import that every command exists.
- Hide or grey out unavailable choices (decide per design; greyed shows what you missed).

## Runner responsibilities
Advance on input or VO end; skip/fast-forward; block gameplay input while active; camera and
speaker focus via commands; an `OnDialogueEnded` event. Never mutate game state from UI code.

## Localisation and VO
Every line has a stable id independent of its text; strings live in tables keyed by id; VO files
named by id. Changing English text must not change the id (or translations silently orphan).
Plan for 30-40% text expansion (German) in UI boxes.

## Dynamic, rule-based barks
For context-driven one-liners (Valve/Left 4 Dead style), use a rules database instead of trees; see
game-ai-programming `rule-based-systems-and-dynamic-dialogue`.

## Verify
- [ ] Import-time validation: no dangling node targets, unknown commands, or missing line ids.
- [ ] Save mid-conversation (or forbid it explicitly) and reload correctly.
- [ ] Automated walker visits every reachable node with conditions forced true/false.
