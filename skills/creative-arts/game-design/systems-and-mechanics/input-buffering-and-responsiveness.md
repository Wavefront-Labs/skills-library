---
id: creative-arts.game-design.systems-and-mechanics.input-buffering-and-responsiveness
name: input-buffering-and-responsiveness
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, input-buffering, input-latency, responsiveness, game-feel, animation-cancel, action-queue, fighting-games, action-games]
level: advanced
status: draft
description: "Make action games feel responsive: input buffers for queued actions, cancel windows, priority rules, and measuring input-to-photon latency."
sources:
  - https://www.routledge.com/Game-Feel-A-Game-Designers-Guide-to-Virtual-Sensation/Swink/p/book/9780123743282
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input buffering and responsiveness

**Goal:** the game does what the player meant, as soon as possible, even when they
pressed a button slightly early or during another animation.

Swink's *Game Feel* treats response time as fundamental: below roughly 100 ms the
response feels instantaneous; beyond that, players perceive lag and the illusion of
direct control weakens.

## Input buffering
Store a pressed action for a short window and execute it at the first legal frame.
```
on_press(action): buffer = (action, now)
each frame:
  if buffer and now - buffer.time <= BUFFER_WINDOW and can_start(buffer.action):
      start(buffer.action); buffer = None
```
- Typical windows are a handful of frames (tune per action).
- Buffer **the most recent** press (or a small queue for combos).
- Clear buffers on state changes where executing would be surprising (death, cutscene,
  menu).

## Cancel windows
Define per animation which frames can be interrupted by which actions:
| Animation phase | Can cancel into |
|---|---|
| startup | dodge only (or nothing) |
| active | nothing |
| recovery (late frames) | attack, dodge, jump |
Generous recovery cancels feel responsive; none feel "heavy" (sometimes intended, as in
commitment-based combat).

## Priority rules
When several inputs arrive together, decide priority (dodge over attack? jump over
interact?). Write it down; inconsistent priority reads as dropped inputs.

## Measure latency
- Record the screen and controller with a high-speed camera (240 fps phone works) and
  count frames from button press (LED or visible press) to on-screen reaction.
- Contributors: input polling, game logic frame, render pipeline (frames queued),
  display latency. Reduce frames-in-flight, avoid extra smoothing on input.

## Gotchas
- Too-long buffers execute actions the player no longer wants ("I pressed that ages ago").
- Buffering + animation lock can make the game feel like it plays itself; keep windows
  short and test.
- Online play adds network latency; rollback netcode (fighting games) addresses this
  differently from delay-based.

## Verify
- [ ] Buffer windows and cancel tables documented per action.
- [ ] Priority rules written and implemented.
- [ ] Input-to-screen latency measured on target hardware.
- [ ] Playtesters report no "dropped" inputs in core combos.
