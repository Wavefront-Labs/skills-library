---
id: creative-arts.game-design.narrative-design.vo-script-and-recording-prep
name: vo-script-and-recording-prep
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, vo-script, voice-over, voice-acting, recording-session, game-dialogue, line-ids, direction-notes, pickups]
level: practitioner
status: draft
description: "Prepare game voice-over scripts and sessions: line IDs, context and direction columns, efforts and barks, casting sides, session order, and pickups tracking."
sources:
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
  - https://www.sagaftra.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VO script and recording prep

**Goal:** actors and directors have everything they need to record game lines that fit
in context, and every recorded line maps cleanly back to the game.

Game VO differs from film: lines are often recorded out of order, without scene
partners, and are triggered by systems, so context must be written into the script.

## Recording script format (spreadsheet)
| Column | Purpose |
|---|---|
| Line ID | unique, stable ID used by the engine (e.g. `Q03_MERCHANT_GREET_02`) |
| Character | speaker |
| Context | what just happened; who they're talking to; distance |
| Direction | emotion, intensity (whisper / normal / shout), pace |
| Line | the text |
| Prior line | what the other character said (for conversation flow) |
| Max length | timing constraint (lip-sync, UI, cinematic) |
| Pronunciation | invented names, phonetic spelling |
| Status | to record / recorded / pickup / approved |

## Session prep
1. **Group by character, then by intensity:** record calm lines first, shouting and
   efforts (grunts, death sounds) at the end to protect the voice.
2. **Casting sides:** a few representative lines per character for auditions.
3. **Reference:** character sheet, art, gameplay video if possible.
4. **Pronunciation guide** for every proper noun, agreed before the session.
5. **Alt takes:** ask for variations on key lines.
6. **File naming** matches Line IDs exactly; agree on format with audio before the session.

## After the session
- Log selects (chosen take) per line.
- Track **pickups** (lines changed or missed) for a later session.
- Implement and review in-game; context errors only show up in game.

## Gotchas
- Script changes after recording are expensive; lock narrative for recorded content.
- Union rules and contracts (e.g. SAG-AFTRA agreements in the US) affect session
  lengths, vocal stress work and rates; check current terms.
- Localised VO needs the same context columns for each language.

## Verify
- [ ] Every line has ID, context and direction.
- [ ] Session order protects voices (efforts last).
- [ ] File names match Line IDs; selects logged.
- [ ] Pickup list maintained.
