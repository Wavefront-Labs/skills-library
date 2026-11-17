---
id: computing-software.game-programming.game-ai-programming.perception-and-memory-systems
name: perception-and-memory-systems
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, perception, line-of-sight, sensing, stimulus, ai-perception, last-known-position, memory-decay, hearing, visibility-cone, raycast-throttling, suspicion-meter, unreal-ai-perception, game-programming, stealth-awareness]
level: practitioner
status: verified
description: "Give NPCs believable senses: throttled line-of-sight and hearing checks, a suspicion ramp instead of binary detection, and time-decayed memory of where the player was."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/ai-perception-system-in-unreal-engine"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Perception and memory systems for NPCs

**Goal:** make an NPC's "can I see/hear the player" feel fair and readable
instead of either omniscient or instantly forgetful — this sits upstream of
decision-making (behaviour tree, utility AI, GOAP): it answers "what do I know
right now," not "what do I do about it."

## Line-of-sight is never just one raycast
A single raycast from NPC-eye to player-center each frame is both expensive at
scale and gives binary, instant detection that feels unfair (spotted the instant
an eyebrow crosses a wall edge). Real implementations layer:
- **Vision cone**: angle + range check first (cheap dot-product/distance test)
  before any raycast — most entities fail this immediately and never need the
  expensive check.
- **Raycast to multiple points** on the target (head, chest, feet), not just
  center, since partial cover shouldn't fully hide or fully reveal.
- **Throttle the raycast itself**: stagger checks across agents and frames (not
  all NPCs raycast on the same frame) and run it at a reduced rate (for example every 6th frame at 60 fps) — use a per-agent frame offset so they don't all
  still land on the same tick: 100 agents staggered over 6 frames cost 16-17 rays per frame instead of 100 on one frame.

## Detection is a ramp, not a bool
A binary "seen/not seen" switch (instant full alert) reads as either psychic or
oblivious. Use an accumulating **awareness/suspicion value** (0..1) that rises
while conditions for detection hold (rate scaled by distance, angle-off-center,
lighting, player's noise level — crouched/walking vs sprinting) and decays when
they don't. Thresholds along that ramp drive visible behavior stages
(Unaware → Suspicious: NPC glances toward last stimulus → Searching → Alert:
full combat), which reads fairly to the player (they see the NPC start to react
before full detection) and gives you distinct states for animation/UI (an
alertness icon) to hook into.

## Memory: last-known-position and decay
On losing sight, an NPC shouldn't either instantly know the player's current
position (omniscient) or instantly forget they existed (goldfish). Store a
**stimulus record** per sensed event: position, timestamp, type (saw, heard),
confidence. On losing direct perception, the AI pathfinds to the
**last-known-position**, not the player's live position, and the record's
confidence decays over a tuned duration — after which the NPC gives up and
returns to a patrol/idle state. Hearing events (footsteps, gunshots) register
as a **lower-confidence, position-only** stimulus (no identity, just
"something happened here") versus a direct sighting's high-confidence,
identified stimulus — this distinction is what makes "I heard something" vs
"I see you" feel different, not the same alert state triggered by two input
types.

## Multi-agent sharing (and why not to always share)
Letting every NPC in a squad instantly know what one NPC perceived
(broadcasting the stimulus to a shared blackboard/perception component) is
realistic for coordinated enemies with radios but breaks believability for
unconnected enemies — an NPC 200m away shouldn't react the instant another one
spots the player with no in-fiction channel for that information. Gate sharing
by actual proximity/comms-group membership, not a convenient global broadcast.

## Verify
- [ ] Expensive LOS checks are throttled and staggered across agents, verified
      in the Profiler with the target agent count, not 2-3 test agents.
- [ ] Detection exposes at least 3 readable stages (unaware/suspicious/alert),
      not a single boolean, and the player gets a visible tell before full alert.
- [ ] Losing sight sends the AI to a last-known-position, with memory confidence
      decaying and eventually clearing — tested by hiding and waiting out the
      decay window, not just immediately re-engaging.
- [ ] Stimulus sharing between NPCs is gated by an in-fiction reason (radio,
      proximity), not a blanket broadcast to every AI in the level.

## Checked (2026-10-22)
- Simulated the awareness ramp (rate 0.5/s while visible, decay 0.3/s): a target seen for 2 s reaches the 0.3 suspicion threshold after 0.58 s, full alert after about 1.8 s, and awareness decays back to 0 within 5 s once unseen, which gives the readable stages the skill asks for; the staggered raycast schedule numbers above are computed.
- The rest (multi-point rays, last-known-position records, hearing as a lower-confidence stimulus, gated sharing) is design guidance, not checkable by running; the unsourced '5-10 Hz is indistinguishable' claim was replaced with the computed stagger cost.
