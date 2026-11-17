---
id: computing-software.game-programming.unity.animator-controller-state-machines
name: animator-controller-state-machines
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-animation, mecanim, animator-controller, animator-parameters, transitions, has-exit-time, any-state, stringtohash, sub-state-machine, game-programming]
level: practitioner
status: docs-checked
description: "Unity Animator Controllers: controller basics, transition properties (Has Exit Time, Fixed Duration, interruption queue, conditions) and Animator.StringToHash ids."
sources: ["https://docs.unity3d.com/Manual/class-AnimatorController.html", "https://docs.unity3d.com/Manual/class-Transition.html", "https://docs.unity3d.com/ScriptReference/Animator.StringToHash.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animator Controller state machines

**Goal:** understand what an Animator Controller and its transitions actually do, so settings are
chosen on purpose.

## Controller basics
- An Animator Controller arranges a set of Animation Clips and Transitions for a character or animated
  GameObject. It manages them with a state machine, a flow-chart of clips and transitions.
- Even a single clip must be placed in an Animator Controller to be used on a GameObject.
- Unity creates a controller automatically when you start animating a GameObject in the Animation
  window or attach a clip to it. To create one manually: right-click in the Project window > Create >
  Animator Controller.
- View navigation: scroll wheel zooms; select states and press F to focus; press A to fit all states.

## Transition properties (Animator window > select the transition line)
| Property | What the manual says |
|---|---|
| Has Exit Time | Exit Time relies on the state's normalized time, not a parameter. Check it to make the transition happen at the time in Exit Time. |
| Exit Time | Normalized time at which the transition can take effect (0.75 = first frame where 75% has played). For looped animations, exit times below 1 are evaluated every loop; above 1 are evaluated once (3.5 = after three and a half loops). |
| Fixed Duration | Checked: transition time in seconds. Unchecked: a fraction of the source state's normalized time. |
| Transition Duration | Length of the transition, in normalized time or seconds depending on Fixed Duration. |
| Transition Offset | Offset of the time to begin playing in the destination state (0.5 = starts halfway through its own timeline). |
| Interruption Source / Ordered Interruption | Control whether this transition can be interrupted (see below). |
| Conditions | Zero, one or several. With no conditions only the Exit Time is considered. With several, all must be met. |

- With Has Exit Time on and one or more conditions, Unity only checks the conditions after the
  state's exit time, so the transition can only occur in a certain portion of the animation.
- A condition is an event parameter, a conditional predicate if needed (less or greater for floats)
  and a parameter value if needed.
- Only one transition can be active at a time, but settings can let another interrupt the active one.

## Transition interruption
Conceptually, transitions are queued and parsed from the first inserted to the last. AnyState
transitions are always queued first, then others by Interruption Source: None (no more), Current
State, Next State, Current State then Next State, Next State then Current State.
Ordered Interruption checked: parsing ends when a valid transition or the current transition is
found. Unchecked: parsing ends when a valid transition is found. Only an AnyState transition can be
interrupted by itself.

## Parameter ids
`Animator.StringToHash(string)` returns an `int` id (CRC32 of the string). The page says to use the
id to optimize assigning and retrieving parameters, and that an id stays valid as long as the input
string does not change, so it persists between sessions and can be used for networking.
```csharp
// From the reference example: cache the hash once
m_BounceStateHash = Animator.StringToHash("Base Layer.Bounce");
m_Animator.Play(m_BounceStateHash, 0, 0.25f);   // start a quarter of the way through
```

## Checked
Date: 2026-11-07

Read in full: "Introduction to Animator Controllers", "Animation transitions" (properties, interruption,
graph, blend tree preview, conditions) and the `Animator.StringToHash` reference with its example.

Removed because the cited pages do not confirm it: the SetFloat / SetBool / SetTrigger code and the
trigger-reset advice, parameter type list, "0.1-0.25 s typical" durations, advice to turn Has Exit Time
off for gameplay, "Can Transition To Self", Any State / sub-state machine / layer structure advice,
`GetCurrentAnimatorStateInfo` / `IsTag` / `IsInTransition` / `CrossFadeInFixedTime` snippets, the
debugging checklist (including Write Defaults and "first in list wins") and the invented Verify list.

Method: documentation only; no commands were run.
