---
id: computing-software.web-development.dioxus.dioxus-state-signals-context
name: dioxus-state-signals-context
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, use-signal, use-hook, signal, context, use-context-provider, globalsignal, event-handler]
level: practitioner
status: docs-checked
description: "Manage Dioxus state: onclick handlers, use_hook, use_signal, Context via use_context_provider/use_context, and GlobalSignal via Signal::global."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/state.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# State: events, signals, context, global signals

Goal: add interactivity and share state in a Dioxus app.

## Event handlers
Attributes starting with `on` take closures; the listener receives an Event object.
```rust
let skip = move |evt| {};
rsx! { button { onclick: skip, id: "skip", "skip" } }
```

## use_hook and use_signal
`use_hook` stores a value in a bare function component and returns a `.clone()` of it:
```rust
let img_src = use_hook(|| "https://images.dog.ceo/breeds/pitbull/dog-3981540_1280.jpg");
```
`Signal` wraps any Rust value and tracks reads and writes; prefer the `use_signal` hook. Creating one manually with `Signal::new()` requires calling `.manually_drop()`, whereas `use_signal` cleans up automatically. When a signal changes, its reactive scope is marked dirty and re-run; components are reactive scopes, so they re-render.

## Context
`use_context_provider()` takes a value that implements `Clone`; children call `use_context()`.
```rust
#[derive(Clone)]
struct TitleState(String);

fn App() -> Element {
    use_context_provider(|| TitleState("HotDog".to_string()));
    rsx! { Title {} }
}
fn Title() -> Element {
    let title = use_context::<TitleState>();
    rsx! { h1 { "{title.0}" } }
}
```
Combine with a signal for reactive shared state:
```rust
#[derive(Clone, Copy)]
struct MusicPlayer { song: Signal<String> }

fn use_music_player_provider() {
    let song = use_signal(|| "Drift Away".to_string());
    use_context_provider(|| MusicPlayer { song });
}
// elsewhere:
onclick: move |_| consume_context::<MusicPlayer>().song.set("Vienna".to_string()),
```
Components reading the signal re-render when it changes.

## GlobalSignal
Combines Context and Signals with no extra setup:
```rust
static SONG: GlobalSignal<String> = Signal::global(|| "Drift Away".to_string());

rsx! {
    h3 { "Now playing {SONG}" }
    button { onclick: move |_| *SONG.write() = "Vienna".to_string(), "Shuffle" }
}
```

## Gotchas
- Hooks follow rules (see the hooks page in the essentials guide).
- GlobalSignals are global to one app, not the whole program: on the server every app gets its own.

## Checked

2026-11-09. Confirmed against the Dioxus 0.7 tutorial page state.md and its guide_state.rs examples: on-prefixed attributes taking closures, use_hook returning a clone, Signal and the manually_drop note, reactive scopes, use_context_provider and use_context, the signal-in-context pattern with consume_context, Signal::global and the one-app scope of GlobalSignal. Nothing removed.

Method: documentation only; no commands were run.
