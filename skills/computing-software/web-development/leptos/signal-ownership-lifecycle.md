---
id: computing-software.web-development.leptos.signal-ownership-lifecycle
name: signal-ownership-lifecycle
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, ownership, lifecycle, signals, on-cleanup, arc-signals]
level: practitioner
status: docs-checked
description: "Explain Leptos ownership for component lifecycle, on_cleanup, disposed-signal panics, signal leaks in collections, and ArcRwSignal reference-counted alternatives."
sources: [https://book.leptos.dev/appendix_life_cycle.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signal lifecycle, ownership and disposal in Leptos

Goal: answer "how do I run code on mount/unmount?", "why does accessing a signal panic?", and "why are signals Copy?".

## Key ideas

- Components do not exist at runtime; they are function calls. What matters is the decision tree (each reactive closure or signal the renderer wraps in an effect), which becomes an ownership tree.
- The owner is the effect or memo currently running. It owns effects and signals created inside it. When it re-runs it first cleans up its children: child effects are cancelled and signals are disposed.
- Signals are arena-allocated: a signal is a cheap Copy index into storage elsewhere, which is why it can move into closures without `.clone()`. Disposal is determined by the owner, not reference counts or lifetimes.

## Component life cycle equivalents

- Before mount: code in the component body.
- On mount: an effect runs a tick after the rest of the component, so use `Effect::new` for work needing the view in the DOM (the page names `create_effect`).
- On unmount: `on_cleanup`, which runs when the current owner cleans up; anything that can unmount is under an effect created by the renderer.

## Problem 1: use after dispose

If you store a signal higher in the tree than where it was created, it may be disposed while you hold its index. Updating a disposed signal only warns; accessing it panics. The `try_` variants of `.get()` and `.with()` return `None` instead. Fix: create the signal in the parent and pass it down.

## Problem 2: leaks

Signals created at a high level and stored in collections (for example `RwSignal<Vec<RwSignal<Todo>>>`) are not disposed when removed from the list; dispose them manually or they live as long as the owner (see the TodoMVC example).

## Reference-counted alternative (0.7)

Every arena primitive has an Arc version: `ArcRwSignal`, `ArcReadSignal`, `ArcWriteSignal`, `ArcMemo`, and so on. Memory is managed by reference counting, so they are safe where arena signals would leak or be used after disposal. Typical pattern: create `ArcRwSignal` values in the collection and convert each to `RwSignal` in the row (see the `counters` example).

Related: computing-software.web-development.leptos.reactive-graph-propagation.

## Checked

2026-11-07: Read in full: appendix_life_cycle.md (component versus decision tree, ownership, the Copy arena, use-after-dispose, leaks, 0.7 Arc signals, Connecting the Dots). Confirmed that updating a disposed signal only warns while accessing it panics, that try_ variants of .get() and .with() return None, the Arc primitive list, and the on mount/on_cleanup guidance (the page names create_effect, which the skill notes). No claims were trimmed. The linked TodoMVC and counters examples were not opened.

Method: documentation only; no commands were run.
