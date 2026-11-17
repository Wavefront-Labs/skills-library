---
id: creative-arts.game-design.narrative-design.audio-logs-and-lore-collectibles
name: audio-logs-and-lore-collectibles
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, audio-logs, lore-collectibles, environmental-storytelling, codex, found-documents]
level: practitioner
status: draft
description: "Write and place audio logs, notes and lore collectibles: length limits, play-while-moving, placement near what they explain, collection UI and avoiding exposition dumps."
sources:
  - https://www.gdcvault.com/
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Audio logs and lore collectibles

**Goal:** optional found content that deepens the world for players who want it and stays
out of the way of players who do not.

## Format choices
| Format | Strength | Cost |
|---|---|---|
| Audio log | plays while the player keeps moving (BioShock, System Shock) | VO casting and recording |
| Note / document | cheap, skimmable, localises easily | reading stops play |
| Terminal / email | fits sci-fi, can carry puzzles (codes) | UI work |
| Item description lore | zero placement cost (Dark Souls) | must be tiny |
| Codex entry | unlocked by encounters, reference not drama | can become a wiki dump |

## Writing rules
1. **Under 60 seconds or ~120 words.** One log, one idea, one voice.
2. **Character first, exposition second:** a person wanting something, in a moment, and
   the lore leaks through. "The pressure doors won't hold" beats a history lesson.
3. **Each log answers a question the space raised** (why is this room barricaded?).
4. **Name the speaker and date** in the UI so logs can be found out of order.
5. **Codes and passwords** in logs must be repeated in the log viewer for re-reading.

## Placement
- Put the log next to the thing it explains so the environment illustrates it.
- Place before a revelation so the player arrives primed, or right after for payoff.
- Avoid placing in combat spaces; the player cannot listen while fighting.
- Use a consistent visual and audio tell (glow, hum) so players learn what to look for.

## Collection UI
- Logs play from the pause menu or a log list; allow replay and subtitles.
- Track collected / total per area for completionists; never gate the main story behind 100%.

## Gotchas
- Logs that carry critical plot make the story incoherent for players who skip them.
- Stacking many logs in one room turns exploration into a listening session.
- Audio logs over loud ambience: duck music and SFX while a log plays.

## Verify
- [ ] Main story understandable with zero logs found.
- [ ] Every log under the length budget and placed beside its subject.
- [ ] Logs replayable from a menu, with subtitles.
