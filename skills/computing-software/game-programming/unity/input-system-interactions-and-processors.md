---
id: computing-software.game-programming.unity.input-system-interactions-and-processors
name: input-system-interactions-and-processors
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-input-system, input-interactions, input-processors, hold-interaction, tap-interaction, deadzone, game-programming]
level: practitioner
status: docs-checked
description: "Configure Input System interactions (Press, Hold, Tap, SlowTap, MultiTap) and processors (deadzones, invert, scale, normalize), and write custom ones (package 1.11)."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Interactions.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Processors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input System interactions and processors

**Goal:** express "hold to charge", "tap vs slow tap" and stick shaping in the binding instead of ad-hoc timers in
gameplay code. Package version 1.11 docs.

## Interactions
Phases: Waiting, Started, Performed, Canceled. Not every interaction triggers every phase. Performed normally triggers the
response; Started and Canceled suit UI feedback (a charge bar that fills, then resets on cancel).

| Interaction | Parameters (default) | started | performed | canceled |
|---|---|---|---|---|
| Press | `pressPoint` (`InputSettings.defaultButtonPressPoint`), `behavior` (PressOnly; also ReleaseOnly, PressAndRelease) | magnitude crosses pressPoint | per behavior: crossing up, back below, or both | not used |
| Hold | `duration` (`defaultHoldTime`), `pressPoint` | crosses pressPoint | held above pressPoint for >= duration | back below pressPoint before duration |
| Tap | `duration` (`defaultTapTime`), `pressPoint` | crosses pressPoint | back below pressPoint before duration | held for >= duration (too slow) |
| SlowTap | `duration` (`defaultSlowTapTime`), `pressPoint` | crosses pressPoint | back below pressPoint after duration | back below before duration (too fast) |
| MultiTap | `tapTime` (`defaultTapTime`), `tapDelay` (2 * tapTime), `tapCount` (2), `pressPoint` | crosses pressPoint | tapCount taps completed | gap over tapDelay, or a tap longer than tapTime |

Built-in interactions work on actuation magnitude, so they also work on sticks, not just buttons. With no explicit
interaction, the default interaction applies and behaves per action type (Value, Button, PassThrough; see the page's
callback table).

```csharp
var fireAction = new InputAction("fire");
fireAction.AddBinding("<Gamepad>/buttonSouth").WithInteractions("tap,slowTap"); // Tap fires, slow tap charges
fireAction.started   += ctx => { if (ctx.interaction is SlowTapInteraction) ShowChargingUI(); };
fireAction.performed += ctx => { if (ctx.interaction is SlowTapInteraction) ChargedFire(); else Fire(); };
fireAction.canceled  += _ => HideChargingUI();
fireAction.Enable();
```
(Adapted from the page's example; the page's own Hold snippet writes `action.cancelled`, which is a typo for `canceled`.)

- Multiple interactions on a binding are checked in listed order, and only one drives the action at a time; if a higher
  one cancels, a lower one can take over. Order changes behavior (for example Tap, MultiTap, Hold versus Hold, MultiTap,
  Tap).
- Interactions on an action are appended after each binding's own interactions.
- Code forms: `.WithInteractions("tap(duration=0.8)")` on a binding, `new InputAction(interactions: "tap(duration=0.8)")`.
- `GetTimeoutCompletionPercentage()` on an action returns 0 to 1 for the driving interaction's timeout (for charge bars).
- Custom: implement `IInputInteraction` (`Process(ref InputInteractionContext)`, `Reset()`; they may keep state) and call
  `InputSystem.RegisterInteraction<T>()`; use it as `"MyWiggle(duration=0.5)"`.

## Processors
A processor takes a value and returns a result of the same type. Written as strings like `"scale(factor=2.5)"`; chains run
left to right (`"invert,normalize(min=0,max=10)"`). Binding processors run before action processors. Built-in:
Clamp (`min`, `max`), Invert, InvertVector2 (`invertX`, `invertY`), InvertVector3, Normalize (`min`, `max`, `zero`),
NormalizeVector2/3 (unit length), Scale (`factor`), ScaleVector2 (`x`, `y`), ScaleVector3, AxisDeadzone (`min`, `max`),
StickDeadzone (`min`, `max`; magnitude under min becomes (0,0), over max is normalized to length 1).

- Code forms: `.WithProcessor("invertVector2(invertX=false)")`, `new InputAction(processors: "...")`.
- Controls can carry processors from their layout (gamepad sticks have a Stick Deadzone). `ReadValue` applies them;
  `ReadUnprocessedValue` bypasses them.
- Custom processors derive from `InputProcessor<TValue>` and override `Process(TValue value, InputControl control)`.
  They must be stateless. Register with `InputSystem.RegisterProcessor<T>()` from an `[InitializeOnLoad]` static
  constructor (editor) and a `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]` method; then use
  it by name, for example `"myvalueshift(valueShift=2.3)"`.

## Checked
Date: 2026-11-07.
Read in full: Input System 1.11 "Interactions" and "Processors" pages, including every code block.
Corrected: the draft listed Tap as "released within duration" without pressPoint, Hold `pressPoint` as the only gotcha,
and stated defaults (Hold 0.4 s, Tap 0.2 s, stick deadzone 0.125/0.925); the pages name the defaults only as
`InputSettings.defaultHoldTime` etc., without numbers, so the numbers were dropped. The page says ordering uses commas in
code (`"tap,slowTap"`) though its prose shows `tap;slowTap`; the code form is used here.
Removed as unconfirmed: "Default Hold Time" Project Settings labels, `normalizeVector2` and `scaleVector2` mouse-look
advice, "never deadzone mouse delta", `ApplyParameterOverride` for runtime sensitivity, the `ctx.interaction is
HoldInteraction` wording, the analog-trigger `pressPoint` gotcha, the "deadzone on both binding and action applies twice"
gotcha, and the invented Verify checklist. The draft's custom processor sample used `Mathf.Pow` with an `Init()` stub; the
page's pattern is used instead.
Method: documentation only; no commands were run.
