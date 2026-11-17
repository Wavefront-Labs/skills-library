---
id: computing-software.game-programming.unity.animation-events-and-statemachinebehaviour
name: animation-events-and-statemachinebehaviour
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-animation, unity-animation-events, statemachinebehaviour, animator-callbacks, footsteps, game-programming]
level: practitioner
status: docs-checked
description: "Hook gameplay to animation with Animation Event functions and StateMachineBehaviour callbacks, including active-state order and per-Animator behaviour instances."
sources: ["https://docs.unity3d.com/Manual/script-AnimationWindowEvent.html", "https://docs.unity3d.com/ScriptReference/StateMachineBehaviour.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animation events and StateMachineBehaviour

**Goal:** run gameplay code at a point in a clip, or while a state is active.

## Animation Events (per clip, at a point in time)
- An Animation Event calls a function at a specific point in time. The function can be in any script
  attached to the GameObject, but must only accept a single parameter of type `float`, `int`,
  `string`, an `object` reference, or an `AnimationEvent` object.
```csharp
public void PrintEvent(string s)   // example from the manual page
{
    Debug.Log("PrintEvent called at " + Time.time + " with a value of " + s);
}
```
- Add at the playhead with the Event button, or right-click the Event line at a position and choose
  Add Animation Event. Drag an event to reposition it.
- After adding, the Inspector shows a Function field to pick the method. Methods with more than one
  parameter cannot be selected.
- To pass several values, use an `AnimationEvent` parameter: it holds a float, an int, a string and
  an object reference, and also provides information about the event that calls the function.
- Hover a marker for a tooltip with the function name and parameter value. Shift-click selects
  several markers; a selection box also works. Delete with the Delete key or right-click >
  Delete Event.

## StateMachineBehaviour (per state)
- `StateMachineBehaviour` is a component you add to a state machine state; scripts must derive from
  it. It is an abstract class that inherits from `ScriptableObject`.
- Predefined state methods: `OnStateEnter` (first update frame when the state machine evaluates the
  state), `OnStateExit` (last update frame), `OnStateUpdate` (each update frame except the first and
  last), `OnStateMove` (during the Animator Root Motion pass) and `OnStateIK` (during the Animator IK
  pass). Transition-related: `OnStateMachineEnter` and `OnStateMachineExit`, invoked whenever a
  state machine transition is taken.
- A state machine can have up to three active states at once: current, next and interrupted. Methods
  are invoked for them in this order: current state, then interrupted state, then next state.
- With synchronized layers in the controller, a method can be invoked more than once for the same
  state: once per synchronized layer with the state, in ascending order.
- By default the Animator instantiates a new instance of each behaviour defined in the controller.
  To share instances, use `SharedBetweenAnimatorsAttribute`.
```csharp
// Shape of the reference example (abridged)
public class AttackBehaviour : StateMachineBehaviour
{
    override public void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex) { }
    override public void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex) { }
}
```

## Checked
Date: 2026-11-07

Read in full: "Add an Animation Event" (including its code listing) and the `StateMachineBehaviour`
reference (remarks, method table, the example listing; the long inherited-members list was skimmed).

Corrections: the original said the function can take "none" as parameters and listed `Object`; the
page says a single parameter (`float`, `int`, `string`, object reference or `AnimationEvent`).
Removed because neither page confirms it: Import Settings > Animation > Events advice, "both clips
fire in a blend" and the `animatorClipInfo.weight` filter, the "no receiver" error text, the claim
events can be skipped when a transition interrupts, "OnStateExit runs even when interrupted", the
`GetBehaviour<T>()` lookup, "don't store scene references" advice, the Timeline comparison table, and
the invented Verify list. The "Add Behaviour" button path is not on the cited pages and was dropped.

Method: documentation only; no commands were run.
