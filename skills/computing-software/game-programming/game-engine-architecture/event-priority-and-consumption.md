---
id: computing-software.game-programming.game-engine-architecture.event-priority-and-consumption
name: event-priority-and-consumption
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, event-priority, event-consumption, input-events, game-programming]
level: practitioner
status: draft
description: "Order event handlers by priority and let them consume events: UI over gameplay input, stable ordering, stopping propagation and avoiding priority sprawl."
sources: ["https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html", "https://gameprogrammingpatterns.com/event-queue.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event priority and consumption

**Goal:** the right handler gets an event first and can stop others seeing it (a click on a menu
button doesn't also fire the gun).

## Dispatcher
```cpp
struct Listener { int priority; uint32_t order; std::function<bool(const Event&)> fn; };  // true = consumed
void dispatch(const Event& e) {
    for (auto& l : listeners)          // kept sorted by (priority desc, registration order)
        if (l.fn(e)) break;
}
```
- Sort stably: equal priorities keep registration order, so behaviour is deterministic.
- Insert sorted on subscribe; don't sort per dispatch.

## Input layering example
Godot's input pipeline is a good reference: `_input` -> GUI (`_gui_input`, Controls consume via
`accept_event()`) -> `_shortcut_input` -> `_unhandled_key_input` -> `_unhandled_input`. Gameplay
listens on unhandled input so UI always wins. Model your own as named layers rather than raw numbers:
```text
DebugConsole(1000) > ModalUI(800) > HUD(500) > Gameplay(100) > Analytics(-100, never consumes)
```

## Rules
- Use a handful of named priority constants, never ad hoc numbers like 537.
- Observers that must always see events (logging, analytics, tutorials tracking) subscribe on a
  separate non-consumable channel instead of a low priority that could be starved.
- Consumption only for input-like events; gameplay notifications (enemy died) should not be
  consumable, or one listener silently breaks another feature.

## Pitfalls
- Changing priorities while dispatching; defer list modifications.
- Hidden coupling: a high-priority handler consuming broadly ("consume all keys while menu open")
  blocks system keys like screenshot or push-to-talk; whitelist those.

## Verify
- Unit test dispatch order and consumption with mock listeners; test click on UI over gameplay.
