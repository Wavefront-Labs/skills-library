---
id: computing-software.game-programming.gameplay-programming.input-context-priority-stacks
name: input-context-priority-stacks
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, input-system, input-context-stack, input-consumption, modal-input, game-programming]
level: practitioner
status: draft
description: "Route input through a stack of contexts (gameplay, vehicle, menu, dialogue, text entry) with priorities and consumption so modal states never leak or eat input wrongly."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/ActionAssets.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input context priority stacks

**Goal:** opening a menu, entering a vehicle or typing in chat changes what buttons do, and closing
it restores the previous mapping — without flags scattered everywhere.

## Model
- An **input context** = a set of action bindings + a priority + "consumes unhandled?" flag.
  Examples: Gameplay (0), OnFoot (1) or Vehicle (1), Dialogue (5), Menu (10), TextEntry (100, consumes
  everything).
- Contexts are pushed/popped by the systems that own the mode. Input dispatch goes from highest
  priority down; an action handled at a level stops (if that context consumes it).

```csharp
class InputRouter {
    readonly List<InputContext> stack = new();       // sorted by priority desc
    public IDisposable Push(InputContext c) { stack.Add(c); stack.Sort(byPriorityDesc); return new Popper(this, c); }
    public void Dispatch(InputEvent e) {
        foreach (var c in stack) {
            if (c.TryHandle(e)) return;               // handled and consumed
            if (c.BlocksLowerContexts) return;        // modal: nothing below gets input
        }
    }
}
using var _ = router.Push(menuContext);               // pop guaranteed when the menu closes
```

## Engine equivalents
- Unreal Enhanced Input: Input Mapping Contexts with priorities; actions' `bConsumeInput`; CommonUI
  activatable widget input configs.
- Unity Input System: action maps enabled/disabled per mode (`playerInput.SwitchCurrentActionMap`), plus
  your own stack to restore previous maps.
- Godot: `_input` -> GUI -> `_unhandled_input` order plus `set_input_as_handled()`; implement mode stack
  in an autoload.

## Rules
- The owner pushes and pops its context (RAII/handles), so closing paths (death, level change) can't
  forget to restore.
- Held keys across context changes: when a context is pushed, send "released" for actions it hides (or
  reset axes) — otherwise the character keeps running while the menu is open.
- Text entry must consume everything, including keys bound to gameplay (WASD typing).

## Debugging
On-screen overlay listing the current stack top-down with the last handled action per context.

## Gotchas
- Two systems pushing the same context twice; use ref-counted or idempotent push.
- Pausing via time scale doesn't block input; contexts do.

## Verify
- [ ] Open menu while holding forward: character stops, and resumes only after re-press.
- [ ] Typing "w" in chat doesn't move the player.
