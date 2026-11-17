---
id: computing-software.web-development.dioxus.dioxus-migrate-0-4-to-0-5-state-hooks
name: dioxus-migrate-0-4-to-0-5-state-hooks
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, migration, dioxus-0-5, use-signal, use-resource, peek, global-signal, fermi]
level: practitioner
status: docs-checked
description: "Migrate Dioxus 0.4 state to 0.5: use_state/use_ref/use_shared_state become use_signal, use_future becomes use_resource, write_silent becomes peek, fermi atoms become GlobalSignal."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_05/index.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_05/state.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_05/hooks.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_05/fermi.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/untested_05/migration.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/untested_05/migration_state.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/untested_05/migration_hooks.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/untested_05/migration_fermi.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus 0.4 to 0.5: state, hooks, fermi

## State hooks
`use_state`, `use_ref` and `use_shared_state` are replaced by `use_signal`. A scope only subscribes to a signal if it reads it, so a parent that merely passes the signal down no longer re-renders when it changes.
```rust
let mut copy_state = use_signal(|| 0);
let mut clone_shared_state = use_context_provider(|| Signal::new(String::from("Hello")));
let mut clone_local_state = use_signal(|| String::from("Hello"));

let copy_state_value = copy_state();                // call to clone the value
let clone_local_state_value = clone_local_state.read(); // or borrow with read()

copy_state.set(1);
clone_shared_state.set("World".to_string());
```
Shared state: use `use_context_provider(|| Signal::new(0))` and `use_context::<Signal<i32>>()` instead of the shared-state hooks.

## write_silent is gone: use peek
`write_silent` (updating without notifying subscribers) was removed. Instead `state.peek()` reads without subscribing, so you opt out of subscribing rather than opting all subscribers out of updates.

## Async hooks and dependencies
`use_future` becomes `use_resource`. `use_effect` and `use_resource` take a single closure and automatically subscribe to signals read inside it, not a tuple of dependencies.
```rust
let state = use_signal(|| 0);
let my_resource = use_resource(move || async move { println!("{state}"); });
let state_plus_one = use_memo(move || state() + 1);
```
Dependencies must be signal-like (Signal, ReadOnlySignal, GlobalSignal, another Resource). For non-reactive values wrap with the `use_reactive!` macro:
```rust
use_resource(use_reactive!(|(non_reactive_state,)| async move {
    non_reactive_state + 1
}));
```

## Fermi atoms become global signals
No `use_init_atom_root`, `use_set` or `use_atom_ref`:
```rust
static NAME: GlobalSignal<String> = Signal::global(|| "world".to_string());
static NAMES: GlobalSignal<Vec<String>> = Signal::global(|| vec!["world".to_string()]);
// onclick: move |_| *NAME.write() = "dioxus".to_string(),
// for name in NAMES.read().iter() { li { "hello: {name}" } }
```
Global memos: `static MEMO: GlobalMemo<u32> = Signal::global_memo(|| COUNT() + 1);`, used like signals. Signals can be used directly in spawned futures without cloning.

## Checked
Checked 2026-11-07 against the 0.5 migration index, State, Hooks and Fermi pages and the migration.rs, migration_state.rs, migration_hooks.rs and migration_fermi.rs snippet files (all read in full). Confirmed: use_signal replacements, context signals, write_silent to peek, use_future to use_resource, single-closure dependencies, signal-like dependency list and use_reactive!, GlobalSignal and GlobalMemo. Nothing removed.
Method: documentation only; no commands were run.
