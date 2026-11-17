---
id: computing-software.game-programming.game-ai-programming.formation-movement
name: formation-movement
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, steering-behaviours, formation-movement, slot-assignment, group-movement, rts-movement, game-programming]
level: practitioner
status: gated
description: "Move groups in formation: anchor point and slot offsets, slot assignment, pathing the formation as a whole, speed matching, and breaking/reforming around obstacles."
sources: ["https://www.aiforgames.com/", "https://www.gamedeveloper.com/programming/implementing-coordinated-movement", "https://www.red3d.com/cwr/steer/gdc99/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Formation movement

## Structure (Millington, AI for Games)
- A **formation anchor** (virtual leader) with position, orientation and its own path.
- A **pattern**: list of slot offsets in anchor space (line, wedge, column, box, circle).
- Each member is **assigned a slot** and steers (arrive behaviour) to `anchor.TransformPoint(slot)`.

```text
# pseudocode (not runnable as written; Arrive is the steering behaviour from seek-flee-and-arrive-steering)
update(dt):
    anchor.follow_path(path, slowest_member_speed() * 0.9, dt)   # anchor waits for the group
    for m in members:
        target = anchor.position + anchor.rotation * pattern[m.slot]
        m.arrive(target, dt); m.face_towards(anchor.forward)
```

## Slot assignment
- Minimise total distance (or crossing paths) when forming up: greedy nearest-slot assignment is
  simple but not optimal: over 200 random 10-unit cases its total distance averaged 1.20x the optimum (worst 1.70x).
  The Hungarian algorithm gives the minimum (`scipy.optimize.linear_sum_assignment`).
- Role-based: melee slots in front, ranged behind, leader at the centre.
- Re-assign only on formation change or member loss, not every frame (prevents shuffling).

## Moving as a group
- Path the **anchor**, not each unit. Members follow slots with local steering + avoidance.
- Anchor speed = slowest member's speed (minus a margin), so formations don't string out.
- A common fix is to let the anchor drift back toward the members' centre of mass if they lag (gated: unconfirmed, source is paywalled or blocked): prevents the leader running away when members get stuck.
- Turning: rotate the anchor gradually; wide formations turning in place make outer slots sprint.
  Some games pivot around the inner edge or convert to a column for tight turns.

## Obstacles and chokepoints
- When a slot target is inside an obstacle or off the navmesh, project it to the nearest valid point.
- At chokepoints, switch to a column formation (or let members path individually) and reform after (gated: unconfirmed, source is paywalled or blocked). The Game Developer article only describes scaling a formation down to fit gaps and splitting and rejoining around obstacles.
- Large RTS groups: combine formations with flow fields for the bulk movement.

## Gotchas
- Members overshooting slots oscillate: use arrive with a slowing radius, and dead-zone near the slot.
- Formation shape should scale with member count; empty slots look odd.
- Players ordering a move expect the group to arrive in shape at the click point facing the drag direction.

## Verify
- [ ] Group crosses an obstacle field and reforms within a few seconds without collisions.
- [ ] Killing a member re-fills the gap without the whole formation reshuffling.

## Checked (2026-10-22)
- Computed greedy versus Hungarian slot assignment with numpy and scipy (200 random cases of 10 units and 10 slots in a 20x20 area): mean greedy/optimal total distance 1.198, maximum 1.697. The previous 'usually fine for < 20 units' claim was not supported and was replaced.
- The anchor loop is pseudocode (relabelled; the C# used engine types not available here). gamedeveloper.com 'Implementing Coordinated Movement' and the Reynolds page return HTTP 200; the article was read: it confirms predefined per-unit slots and group speed of the slowest unit, but uses a 'commander' rather than an anchor and has no centroid-drift rule or column-at-chokepoint rule, so those two bullets carry the gated marker and the skill is gated.
