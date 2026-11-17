---
id: creative-arts.game-design.tabletop-game-design.tabletop-simulator-prototyping
name: tabletop-simulator-prototyping
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, tabletop-simulator, tts, paper-prototyping, remote-playtest, deck-sheets, steam-workshop, digital-prototype]
level: practitioner
status: draft
description: "Build a board game prototype in Tabletop Simulator: deck sheet images, custom boards and tokens, saving and sharing via Workshop, and running remote playtests."
sources:
  - https://kb.tabletopsimulator.com/
  - https://store.steampowered.com/app/286160/Tabletop_Simulator/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tabletop Simulator prototyping

**Goal:** a playable digital version of a tabletop prototype for remote playtesting and
fast iteration, without programming.

Tabletop Simulator (TTS, Berserk Games, on Steam) is a physics sandbox for tabletop
games; its Knowledge Base documents custom objects.

## Building blocks
| Object | How |
|---|---|
| Cards | Custom Deck: a grid image of card faces (up to 10 columns x 7 rows per sheet; 69 cards plus the hidden slot) + a back image |
| Board | Custom Board: a single image |
| Tokens/tiles | Custom Token (image with alpha) or Custom Tile (square, round, hex) |
| Pieces | built-in chips, cubes, dice, or custom models (OBJ) |
| Bags | infinite bags for resource supplies |
Images can be hosted locally or uploaded to Steam Cloud via TTS's cloud manager; the
Workshop needs hosted images.

## Procedure
1. Export card faces as a deck sheet (nanDeck, spreadsheets + image tools, or online deck
   sheet builders) at the grid size TTS expects; note the card count.
2. In TTS: Objects -> Components -> Custom -> Deck; set face/back URLs, width/height,
   number of cards; import.
3. Add board, tokens, dice; arrange the setup; lock board objects (right-click -> lock).
4. **Save** the game; for sharing, **upload to the Steam Workshop** (unlisted or
   friends-only for confidential prototypes) or share the save file.
5. For updates, replace images and re-import; increment a version name.
6. Run remote playtests with voice chat; record sessions (with consent).

## Gotchas
- Physics makes small pieces fiddly; use snap points and locking.
- Hidden information needs hand zones (built-in for hands; use hidden zones for other
  secrets).
- Cache: TTS caches images by URL; changing an image at the same URL may not refresh
  for others - use new URLs per version.
- Remote testing changes the experience (less table talk, more fiddliness); weight
  feedback accordingly.

## Verify
- [ ] All components import correctly with the right counts.
- [ ] Setup saved; board locked; hand/hidden zones configured.
- [ ] Shared build loads on another machine with current images.
- [ ] At least one full remote playtest completed.
