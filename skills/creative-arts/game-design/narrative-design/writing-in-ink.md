---
id: creative-arts.game-design.narrative-design.writing-in-ink
name: writing-in-ink
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, ink-script, inkle, interactive-fiction, branching-dialogue, inky, narrative-scripting]
level: practitioner
status: docs-checked
description: "Write branching narrative in inkle's Ink: knots, stitches, sticky vs once-only choices, gathers, variables, tunnels, tags and the runtime loop a game calls."
sources:
  - https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md
  - https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md
  - https://www.inklestudios.com/ink/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing in Ink

**Goal:** a branching script that writers can play-test in Inky and engineers can drive
from the game without hand-coding every branch.

## Core syntax
| Construct | Syntax | Notes |
|---|---|---|
| Knot (scene) | `=== harbour ===` | divert to it with `-> harbour` |
| Stitch (sub-scene) | `= dockside` | address as `harbour.dockside` |
| Once-only choice | `* [Ask about the ship]` | disappears after being picked |
| Sticky choice | `+ [Wait]` | stays available; use for hubs and loops |
| Suppressed text | `* "Hello[."]," you say.` | text in `[]` shows on the button only, text after only in output |
| Gather | `- ` | rejoins the branches above it; the main tool against branch explosion |
| Conditional choice | `* {has_key} [Unlock it]` | |
| Fallback choice | `* -> leave` | no choice text; never shown, chosen by the game when no other options exist |
| Variables | `VAR trust = 0` then `~ trust += 1` | global; `temp` for local |
| Visit counts | `{harbour > 1: "Back again?"}` | a knot or stitch name is an integer: the number of times it has been seen |
| Alternatives | `{Hi\|Hello again\|You.}` sequence, `{&a\|b}` cycle, `{~a\|b}` shuffle, `{!a\|b}` once | |
| Tunnel | `-> flashback ->` and `->->` to return | reusable scenes that come back to the caller |
| Thread | `<- ambient_options` | merges another knot's choices into this one |
| Tags | `# speaker: Mara # mood: angry` | hashtag metadata the game reads per line from `currentTags` |
| End | `-> END` (story over) / `-> DONE` (this flow over) | |

## Working pattern
1. Write the critical path as knots with `-> END` stubs; play it in Inky end to end.
2. Add choices, then close every fork with a gather unless the split is meant to persist.
3. Track persistent consequences in a few named variables or a `LIST` of states, not in
   dozens of booleans.
4. Put presentation data (speaker, portrait, camera, VO id) in tags, never in the prose.
5. Split files by chapter with `INCLUDE chapter2.ink`; keep one root file.

## Runtime loop (C# integration)
```
var story = new Story(inkJson.text);
while (story.canContinue) { Show(story.Continue(), story.currentTags); }
foreach (var c in story.currentChoices) { AddButton(c.text, c.index); }
// on click: story.ChooseChoiceIndex(i); then loop again
string save = story.state.ToJson();       // save game
story.ObserveVariable("trust", (n, v) => UpdateUI(v));
```
`EXTERNAL play_sound(id)` binds Ink calls to game functions via `story.BindExternalFunction`.

## Gotchas
- A flow that ends with no divert hits an "ran out of content" runtime error and wants a
  `-> DONE` or `-> END`. Fix every warning.
- A loop built only from once-only `*` choices runs out of options and hits that error unless
  it has a fallback choice or sticky `+` choices.
- A knot name used as a test is true if any stitch inside that knot has been seen.

## Checked

2026-11-09. Confirmed against inkle's WritingWithInk.md and RunningYourInk.md (read in part, by
section): knots, diverts, once-only and sticky choices, fallback choices, gathers, visit-count
tests, alternatives (`&`, `~`, `!`), tunnels and `->->`, threads, `-> DONE`, `INCLUDE`, tags,
`LIST`, and the C# calls `Continue`, `canContinue`, `currentChoices`, `ChooseChoiceIndex`,
`state.ToJson`, `ObserveVariable`, `BindExternalFunction`. Removed the unsourced notes on tunnel
visit counts and renaming knots against saves.
Method: documentation only; no commands were run.

## Verify
- [ ] Inky shows zero errors and zero warnings.
- [ ] Every path reaches `-> END` or `-> DONE` (play each choice at least once).
- [ ] Save, reload, continue works mid-scene.
- [ ] Tags parsed by the game for every line that needs speaker/VO data.
