---
id: creative-arts.game-design.narrative-design.inform7-parser-fiction
name: inform7-parser-fiction
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, inform7, parser-interactive-fiction, interactive-fiction, text-adventure, natural-language-programming]
level: practitioner
status: draft
description: "Write parser interactive fiction in Inform 7: rooms and things, rulebooks, new actions and Understand lines, scenes, test scripts, and avoiding guess-the-verb."
sources:
  - https://ganelson.github.io/inform-website/
  - https://github.com/ganelson/inform
  - https://ifcomp.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parser interactive fiction in Inform 7

**Goal:** a parser game whose world model responds sensibly to what players type.

## Minimal source
```
"The Lighthouse" by Your Name

The Lamp Room is a room. "Glass on every side, and the great lens dark."
The brass lever is a fixed in place thing in the Lamp Room.
The lens is a device in the Lamp Room. The lens is switched off.

Instead of pulling the brass lever:
    now the lens is switched on;
    say "Gears grind. Light floods out over the sea."

Understand "light [something]" as switching on.
Understand "crank" and "handle" as the brass lever.

Test me with "x lens / pull lever / look".
```

## The rulebook model
Actions run through `Before`, `Instead`, `Check`, `Carry out`, `After`, `Report`.
- `Instead` for one-off exceptions ("Instead of taking the lens: say ...").
- New actions: `Polishing is an action applying to one thing. Understand "polish [something]" as polishing.`
  then write `Check`, `Carry out` and `Report polishing` rules.
- Kinds: room, thing, container, supporter, device, door, person; properties like
  `openable`, `lockable`, `lit`, `scenery`.

## Scenes and pacing
```
Storm is a scene. Storm begins when the lens is switched on.
Every turn during Storm: say "[one of]Rain lashes the glass.[or]Thunder.[at random]".
Storm ends when the ship is rescued.
```

## Avoiding guess-the-verb
1. Every noun mentioned in a description exists as at least scenery with an `x` response.
2. Add synonyms with `Understand` for every object and likely verb; read beta
   transcripts for commands that failed and add them.
3. Clue the required verb in prose ("the lever looks stiff, as if waiting to be pulled").
4. Implement `HINT` or a hint menu; include `ABOUT` and credits.

## Testing
- `Test me with "..."` scripts per puzzle; run `test me` in the IDE after every change.
- Debug commands in IDE builds: `ACTIONS` (trace actions), `RULES` (trace rules), `SHOWME object`, `PURLOIN`, `GONEAR`.
- Release as Glulx (`.gblorb`) for size and features, with a web interpreter bundled
  (`Release along with an interpreter.`).

## Gotchas
- Mentioned-but-unimplemented objects ("You can't see any such thing") are the top complaint in IFComp reviews.
- Disambiguation prompts ("Which do you mean...") on every turn: give objects distinct names.
- Long room descriptions bury interactable items; mention them in a final sentence.

## Verify
- [ ] Every noun in every description responds to `x`.
- [ ] `test me` passes for each puzzle; full walkthrough script reaches the ending.
- [ ] Beta transcripts reviewed and failed commands handled.
