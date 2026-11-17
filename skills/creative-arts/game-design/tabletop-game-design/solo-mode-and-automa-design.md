---
id: creative-arts.game-design.tabletop-game-design.solo-mode-and-automa-design
name: solo-mode-and-automa-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, automa, solo-mode, cooperative-board-games, bot-opponent, ai-deck, solitaire-board-games, automa-factory]
level: advanced
status: draft
description: "Design a solo mode for a board game: automa decks that simulate opponents cheaply, upkeep budgets, difficulty levels and score-attack alternatives."
sources:
  - https://stonemaiergames.com/automa-factory/
  - https://www.routledge.com/Building-Blocks-of-Tabletop-Game-Design-An-Encyclopedia-of-Mechanisms/Engelstein-Shalev/p/book/9781138365490
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Solo mode and automa design

**Goal:** a solo mode that keeps the multiplayer game's interesting decisions and
tension with low bookkeeping.

Stonemaier Games' Automa Factory (Morten Monrad Pedersen and team) popularised the
"Automa": an artificial opponent driven by a card deck that simulates the *effect* of an
opponent's actions on the player rather than playing the full game.

## Options
| Approach | Description | Fits |
|---|---|---|
| Score attack | play alone, beat a score table | low interaction games |
| Automa deck | each turn draw a card that tells the bot what to block/take | worker placement, area control |
| Dummy player | full rules played by a flowchart | heavy upkeep; rarely ideal |
| Co-op adaptation | play multiple hands | co-op games |
| Puzzle scenarios | fixed setups with goals | campaign/puzzle-y games |

## Automa design principles (from Automa Factory practice)
1. **Simulate interaction, not the full opponent:** what does an opponent *do to you*?
   Block spaces, take cards, race on tracks, score. The bot only needs to do those.
2. **Cheap upkeep:** target a few seconds per bot turn; one card draw, one or two
   actions.
3. **Decision-free for the player:** the bot's actions should be resolved by rules, not
   player choice (or with clear tie-breaks), so the player doesn't "play both sides".
4. **Difficulty levels:** adjust bot scoring, starting resources or deck composition.
5. **Score comparison:** the bot needs a score or a loss condition.

## Procedure
1. List the interactions players feel from opponents in multiplayer.
2. Design an automa card format that triggers those interactions with minimal fiddliness.
3. Playtest with solo players; time bot turns; count rules lookups.
4. Tune difficulty so a typical player wins about as often as intended at Normal.

## Gotchas
- Flowchart bots with many branches feel like work.
- Bots that ignore the board state can produce absurd moves; use card-driven priorities
  that reference the board simply.
- Solo players are a large audience; a weak solo mode gets reviewed separately.

## Verify
- [ ] Interactions to simulate listed.
- [ ] Bot turn time and rules lookups measured.
- [ ] Difficulty levels tested with win-rate data.
