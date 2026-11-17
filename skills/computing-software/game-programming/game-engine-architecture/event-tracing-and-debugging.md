---
id: computing-software.game-programming.game-engine-architecture.event-tracing-and-debugging
name: event-tracing-and-debugging
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, event-tracing, debugging, event-bus, game-programming]
level: practitioner
status: draft
description: "Trace events through an engine event system: event logs with sender and frame, visual timelines in profilers, filters, and finding feedback loops."
sources: ["https://github.com/wolfpld/tracy", "https://gameprogrammingpatterns.com/event-queue.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event tracing and debugging

**Goal:** decoupled events make "who caused this?" hard; tracing makes it answerable.

## Record every dispatch
In debug/dev builds, wrap the dispatcher:
```cpp
void EventBus::publish(const Event& e, SourceLoc loc = SourceLoc::current()) {
    if (tracing) trace.push({frame, now(), e.typeId, e.sender, loc, depth});
    ++depth; dispatchToListeners(e); --depth;
}
```
Store: frame, timestamp, event type, sender entity, call site (`std::source_location`),
nesting depth (events fired from handlers), listener count and which listener consumed it.

## Viewing
- ImGui window: filterable list by type/sender, colour by depth to show cascades.
- Profiler integration: Tracy `TracyMessage` / zones per dispatch with event name so events appear on
  the frame timeline next to CPU work; Tracy plots for events per frame.
- Dump the trace ring buffer into crash reports.

## Diagnosing common bugs
- **Feedback loops:** A's handler fires B, B's fires A. Detect nesting depth above a threshold (e.g. 16)
  and assert with the chain printed.
- **Event storms:** count events per type per frame; alert when a type spikes (a collision event per
  contact point per frame).
- **Missing listeners:** event published with zero listeners logged at verbose level; often a
  subscription happened too late.
- **Ordering:** queued events processed a frame later; tracing shows publish frame vs handle frame.

## Cost control
Compile-time removable (`#if EVENT_TRACING`), with runtime type filters so hot events can be excluded.

## Verify
- Trigger a known chain (pickup -> inventory -> UI -> sound) and confirm the trace shows it with
  correct nesting.
