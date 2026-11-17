---
id: computing-software.web-development.dioxus.dioxus-event-handlers-inputs
name: dioxus-event-handlers-inputs
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, onclick, oninput, onsubmit, prevent-default, stop-propagation, controlled-input, downcast]
level: intro
status: docs-checked
description: "Handle Dioxus user input: onclick/oninput/onsubmit handlers, evt.value() and values(), controlled vs uncontrolled inputs, stop_propagation, prevent_default and downcast."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/event_handlers.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/input_controlled.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/event_prevent_default.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Event handlers and form inputs in Dioxus

Goal: wire user input to signals.

Attach a closure as an `on...` attribute; its first argument is an `Event` with typed data (for example `MouseData`):

```rust
button { onclick: move |event| log!("Clicked! Event: {event:#?}"), "click me!" }
```

Families: mouse (`onclick`, `onmouseover`, `onmousedown`, `onmousemove`), keyboard (`onkeydown`, `onkeyup`, `onkeypress`), form (`onsubmit`, `oninput`, `onchange`), focus (`onfocus`, `onblur`), drag and drop (`ondrag`, `ondrop`, `ondragover`), UI (`onscroll`, `onload`, `onresize`).

## Reading values

```rust
input { type: "checkbox", oninput: move |evt| upload_enabled.set(evt.checked()) }
select { oninput: move |evt| option.set(Some(evt.value())), option { label: "Sedan", value: "sedan" } }
input { type: "text", oninput: move |e| first_name.set(e.value()) }
form {
    onsubmit: move |evt| { evt.prevent_default(); values.set(evt.values()); },
    input { type: "text", name: "username" }
}
```

Accessors: `.value()`, `.values()` (form), `.checked()`, `.files()`, `.key()` (a Rust `Key` enum).

## Controlled vs uncontrolled

Uncontrolled is the default: the input owns its state. Controlled drives `value` yourself, which lets you transform, validate or programmatically change input:

```rust
input {
    value: "{name().to_ascii_uppercase()}",
    oninput: move |event| name.set(event.value())
}
```

## Propagation and defaults

Only the bubbling phase is captured, so the inner element's handler runs before its parent's. Call `event.stop_propagation()` to stop it. `evt.prevent_default()` cancels default behavior (link navigation, form submission, file drops, text input) while handlers still run:

```rust
a { href: "https://example.com", onclick: |evt| { evt.prevent_default(); }, "example.com" }
```

## Native events and async

For platform details use `event.downcast::<web_sys::Event>()` (the page example unwraps the result). Handlers may be async and are spawned automatically.

## Gotcha

Dioxus will not cancel earlier tasks from an async handler, so rapid clicks start concurrent fetches; be careful mutating state there without synchronization.

## Checked
Checked 2026-11-07 against the 0.7 Handling User Input page and the input_controlled.rs and event_prevent_default.rs snippet files (all read in full). Confirmed: event families, accessor methods, controlled vs uncontrolled inputs, bubbling-only propagation, stop_propagation, prevent_default, downcast to web_sys, async handlers and the concurrent-task warning. Nothing removed.
Method: documentation only; no commands were run.
