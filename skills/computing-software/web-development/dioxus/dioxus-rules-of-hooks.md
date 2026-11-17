---
id: computing-software.web-development.dioxus.dioxus-rules-of-hooks
name: dioxus-rules-of-hooks
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, hooks, use-hook, rules-of-hooks, use-signal, hook-list, early-return]
level: intro
status: docs-checked
description: "Dioxus hook rules: hooks use call order via use_hook, so never call them in conditionals, closures or loops; early returns and the use_ prefix convention."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rules of hooks in Dioxus

Goal: call hooks so the internal hook list stays consistent between renders.

`use_hook` is the primitive all hooks sit on. It takes an initializer and returns a clone of the stored value:

```rust
fn Simple() -> Element {
    let count = use_hook(|| 123);
    rsx! { "{count}" }
}
```

On the first call the initializer runs and a new slot is created; otherwise `use_hook` returns a clone of the current value in the slot. The hook index is incremented by 1 on every `use_hook` call and reset to 0 before the component re-renders. Hooks use their call order to track which state belongs to which hook, so call them in the same order every time, only at the top level of a component or another hook. Breaking the rules can make the hook list walk fail and the app panic.

## What not to do

- No hooks in conditionals: the hook list may skip an entry on re-render, so the next hook retrieves the wrong value.
- No hooks in closures: closures can call hooks in an inconsistent order between renders. Call the hook outside and only use its result inside the closure.
- No hooks in loops: this too leads to inconsistent retrieval of hook values between renders.

## Early returns

Unlike React, Dioxus lets you return early between hook calls, because error boundaries and suspense boundaries use the question-mark syntax. The docs still discourage it, since it can cause consistency issues like conditionals. Return early after all hooks have run:

```rust
let name = use_signal(|| "bob".to_string());
let age = use_signal(|| 123);
if name() == "jack" {
    return Err("wrong name".into())
}
rsx! { "{name}, {age}" }
```

## Convention

Name hook functions with the `use_` prefix; it signals that the function internally walks the component's hook list and must follow these rules.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Dioxus 0.7 "Hooks" docsite page. Removed: the code snippets for conditionals, closures and loops, because the page pulls them from an include file that was not readable; the rules are kept as prose.
