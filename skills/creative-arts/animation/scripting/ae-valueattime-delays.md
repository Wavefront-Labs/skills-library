---
id: creative-arts.animation.scripting.ae-valueattime-delays
name: ae-valueattime-delays
category: creative-arts
field: animation
product: scripting
tags: [value-at-time, ae-expressions, expressions, after-effects, valueattime, delay, follow-through, cascade, echo, offset-animation, index]
level: advanced
status: docs-checked
description: "Build delays and follow-the-leader animation with valueAtTime in After Effects expressions: read another property at an offset time."
sources:
  - https://raw.githubusercontent.com/docsforadobe/after-effects-expression-reference/master/docs/objects/property.md
  - https://raw.githubusercontent.com/docsforadobe/after-effects-expression-reference/master/docs/objects/comp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# valueAtTime delays

**Goal:** many layers follow one animated leader with a delay, so you animate once and offset everywhere.

## The method

`property.valueAtTime(t)` returns the value of a property at time `t`, in seconds (number or array). The reference's own example picks a random value per frame from four keyframes at 0, 1, 2 and 3 seconds with `valueAtTime(random(4))`.

`thisComp.layer(indexOrName)` returns the Layer object with the specified index or name; the index refers to layer order in the Timeline panel.

## Leader-follower

On a follower's Position, read the leader at a time offset:

```javascript
delay = 0.08;                                   // seconds
thisComp.layer("Leader").transform.position.valueAtTime(time - delay)
```

Give each follower a larger delay (or drive the delay from a slider on a control layer) to cascade. Retiming the delay value retimes every follower, because all read the same leader.

## Further reading

The reference points to Dan Ebberts' MotionScript article on follow-the-leader techniques for more examples.

## Verify

Scrub and check that a follower repeats the leader's motion, shifted by the delay, at a key moment.

## Checked

Method: 2026-11-09 read valueAtTime in the property object page and layer(index) in the comp object page of the After Effects expression reference. Removed the index-chain, tail-rig decay, Echo comparison, performance and reordering claims, which those pages do not state.
