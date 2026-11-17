---
id: computing-software.web-development.leptos.uncontrolled-inputs-noderef
name: uncontrolled-inputs-noderef
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, forms, inputs, uncontrolled, node-ref, submit, web-sys]
level: practitioner
status: docs-checked
description: "Read a form input's value on submit in Leptos using an uncontrolled input, NodeRef and prevent_default."
sources: [https://book.leptos.dev/view/05_forms.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uncontrolled inputs with NodeRef

Goal: let the browser own the input's state and read it only when the form is submitted.

```rust
use leptos::{ev::SubmitEvent, html::Input};

let (name, set_name) = signal("Uncontrolled".to_string());
let input_element: NodeRef<Input> = NodeRef::new();

let on_submit = move |ev: SubmitEvent| {
    // stop the page from reloading!
    ev.prevent_default();
    let value = input_element
        .get()
        .expect("<input> should be mounted")
        .value();
    set_name.set(value);
};

view! {
    <form on:submit=on_submit>
        <input type="text"
            value=name
            node_ref=input_element
        />
        <input type="submit" value="Submit"/>
    </form>
    <p>"Name is: " {name}</p>
}
```

## Points

- Use `value` (attribute) here since you only set the initial value; `prop:value` would also work.
- `node_ref=...` fills the `NodeRef`; older examples use `_ref`, same thing, but `node_ref` has better rust-analyzer support.
- `NodeRef<html::Input>` is a reactive smart pointer to the DOM node, set when the element renders. `.get()` (or calling it as a function) returns `Option<leptos::HtmlElement<html::Input>>`; event handlers fire only after mount, so unwrapping is safe. It derefs to `web_sys::HtmlInputElement`, so `.value()` works.
- The `leptos::html` module has a type for every HTML element.
- The page's submit handler calls `ev.prevent_default()` with the comment "stop the page from reloading!".

## When to choose

Controlled inputs update a signal on every event; uncontrolled only talk to the framework at submit.

## Related

- `computing-software.web-development.leptos.controlled-inputs-bind`

## Checked

2026-11-07: Read in full: view/05_forms.md including the inline sandbox source (controlled inputs, bind:, uncontrolled inputs with NodeRef, node_ref versus _ref, the Option from get, textarea and select). One correction: 'Always call ev.prevent_default()' is now stated as what the page's handler does (comment: stop the page from reloading). The rest matches. Live sandbox not opened.

Method: documentation only; no commands were run.
