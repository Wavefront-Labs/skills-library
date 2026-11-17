---
id: creative-arts.game-design.systems-and-mechanics.game-jam-scoping
name: game-jam-scoping
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, game-jam, ludum-dare, global-game-jam, scoping, rapid-prototyping, game-ideation, time-boxing, mvp]
level: practitioner
status: draft
description: "Scope and run a 48-72 hour game jam entry: theme interpretation, a one-verb core, hour-by-hour time boxes, feature cut list and a playable build by the halfway mark."
sources:
  - https://globalgamejam.org/
  - https://ldjam.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Game jam scoping

**Goal:** ship a complete, playable, small game inside a jam window (Ludum Dare Compo
48 h / Jam 72 h; Global Game Jam ~48 h) instead of an ambitious unfinished one.

## Hour 0-2: concept
1. Brainstorm 10+ interpretations of the theme; discard the first 3 (everyone else has
   them).
2. Pick a concept with **one core verb** that can be playable with grey boxes.
3. Write the **cut list now**, before attachment: core (must), polish (should), dream
   (won't).

## Time boxes (48 h example)
| Hours | Target |
|---|---|
| 0-2 | concept, cut list, roles |
| 2-12 | core verb playable, ugly; one level/round |
| 12-24 | goal, fail state, restart loop: a complete game |
| 24-36 | content (levels/rounds), feedback, sound |
| 36-44 | polish, title screen, how-to-play text |
| 44-48 | build, upload, page, screenshots. Feature freeze. |
Rule: **a complete game (start, play, end, restart) by the halfway point.** Everything
after is improvement.

## Scoping rules
- Divide your estimate by three; jams always run short.
- One mechanic deeply explored beats five shallow ones; jam judges and players play for
  a few minutes.
- Teach in the first 30 seconds; no one reads jam instructions. Put controls on screen.
- Use tools you already know; the jam is not the time to learn a new engine.
- Sound is cheap value: free tools like sfxr/bfxr/jsfxr make placeholder effects fast.
- Web builds get far more plays than downloads.

## Gotchas
- **Uploading in the last hour** fails (site load spikes, build errors). Upload a build
  early and replace it.
- Check the jam's rules (Ludum Dare Compo requires solo work and made-during-jam assets;
  Jam allows teams and pre-made assets with disclosure). Rules change; read current ones.
- Sleep. Bugs introduced at hour 40 without sleep cost more than they fix.

## Verify
- [ ] Complete loop playable by the halfway mark.
- [ ] Cut list exists and was used.
- [ ] Build uploaded with on-screen controls at least 4 hours before deadline.
