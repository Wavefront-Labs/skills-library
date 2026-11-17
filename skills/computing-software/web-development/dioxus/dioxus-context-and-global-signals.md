---
id: computing-software.web-development.dioxus.dioxus-context-and-global-signals
name: dioxus-context-and-global-signals
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, use-context-provider, use-context, provide-context, consume-context, globalsignal, globalmemo, context]
level: practitioner
status: docs-checked
description: "Share state in Dioxus without prop drilling: use_context_provider and use_context with newtypes, signal bundles, dynamic consume_context, GlobalSignal and GlobalMemo."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/context.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/guide_state.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Context and global signals in Dioxus

Goal: let descendants reach shared state directly instead of threading it through props.

## Provide and consume

```rust
fn app() -> Element {
    use_context_provider(|| "Hello world!".to_string());
    rsx! { Child {} }
}

fn Child() -> Element {
    let title = use_context::<String>();
    rsx! { "{title}" }
}
```

Context is indexed by `TypeId`, so type aliases share a key. Wrap data in a newtype (`#[derive(Clone)] struct Title(String);`) so several `String` values can coexist; usually one struct for a set of data is enough. Each context entry must implement `Clone`.

## Provider components

```rust
#[component]
fn ThemeProvider(children: Element, color: ThemeColor) -> Element {
    use_context_provider(|| ThemeState::new(color));
    children
}
```

Use it several times with different parameters to scope context to a subtree.

## Dynamic context

`provide_context` and `consume_context` work at runtime without hooks, including inside event handlers and async tasks: `onclick: move |_| consume_context::<ThemeProvider>().set_theme(ThemeColor::Red)`. Dynamically providing replaces the current component's entry, and replacing context is not reactive.

## Reactive context: provide signals

```rust
#[derive(Clone, Copy)]
struct HeaderContext {
    title: Signal<String>,
    subtitle: Signal<String>
}

#[component]
fn HeaderProvider(children: Element) -> Element {
    let title = use_signal(|| "Title".to_string());
    let subtitle = use_signal(|| "Subtitle".to_string());
    use_context_provider(|| HeaderContext { title, subtitle });
    children
}
```

Add methods (reset, fetch, uppercase_title) to the struct and call them from handlers after `use_context::<HeaderContext>()`.

## Global signals

```rust
static SONG: GlobalSignal<String> = Signal::global(|| "Drift Away".to_string());
// read: rsx! { h3 { "Now playing {SONG}" } }
// write: onclick: move |_| *SONG.write() = "Vienna".to_string()

static COUNT: GlobalSignal<i32> = Signal::global(|| 0);
static DOUBLE_COUNT: GlobalMemo<i32> = Memo::global(|| COUNT.cloned() * 2);
```

No `use_context_provider` is needed. Global signals are global to one app, not the program: with server-side rendering or multi-window desktop each app gets its own independent value. `GlobalSignal` and `GlobalMemo` are `Global<Signal<T>>` and `Global<Memo<T>>`.

## Checked
Checked 2026-11-07 against the 0.7 Global Context page and the guide_state.rs snippet file (both read in full). Confirmed: use_context_provider and use_context, TypeId and newtypes, provider components, dynamic context and non-reactive replacement, signal bundles, GlobalSignal and GlobalMemo and per-app scope. Nothing removed.
Method: documentation only; no commands were run.
