---
id: computing-software.game-programming.gameplay-programming.state-machine-history-logging
name: state-machine-history-logging
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, state-history, state-machine, debugging, game-programming]
level: practitioner
status: draft
description: "Debug gameplay state machines with a ring-buffer transition history, on-screen state overlays and assertions on illegal transitions."
sources: ["https://gameprogrammingpatterns.com/state.html", "https://github.com/ocornut/imgui"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging state machines with history logging

**Goal:** answer "how did the character get into this state?" after the fact, without a debugger.

## Ring buffer of transitions
```cpp
struct Transition { uint32_t frame; float time; StateId from, to; EventId cause; };
template<size_t N> struct History {
    std::array<Transition, N> buf{}; size_t head = 0, count = 0;
    void push(const Transition& t) { buf[head] = t; head = (head + 1) % N; count = std::min(count + 1, N); }
};
// in the FSM's single changeState() funnel:
void FSM::changeState(StateId to, EventId cause) {
    history.push({g_frame, g_time, current, to, cause});
    current->exit(); current = states[to]; current->enter();
}
```
Every transition must go through one funnel function; direct `current = x` assignments bypass logging.
Keep 64-256 entries per entity; it costs a few KB and is always on in development builds.

## What to record
- Frame number (correlates with replays and profiler captures), the triggering event or input,
  and the guard that passed. Store ids, not strings; resolve names when printing.
- Optional: a short context blob (velocity, grounded flag) for the states that misbehave.

## Surfacing it
- Overlay: draw current state name above the selected entity; ImGui window listing the last 20
  transitions with frame deltas.
- Dump history into crash reports and bug-report attachments automatically.
- Flag *thrash*: more than K transitions in M frames (e.g. Fall<->Grounded flicker from a bad ground
  check) and log a warning.

## Illegal transitions
Keep an allowed-transition table and assert in `changeState` when a pair is not in it. Most state
bugs are a transition that was never designed (Dead -> Jump).

## Verify
- Reproduce a bug, open the overlay, and confirm the history explains it without stepping code.
- Unit test: drive a scripted input sequence and compare the recorded transition list to the expected one.
