---
id: computing-software.web-development.leptos.controlled-inputs-bind
name: controlled-inputs-bind
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, forms, inputs, controlled, bind, prop-value, textarea, select]
level: practitioner
status: docs-checked
description: "Build controlled form inputs in Leptos with on:input:target and prop:value, the bind: shorthand, and textarea and select handling."
sources: [https://book.leptos.dev/view/05_forms.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlled inputs, bind: and textarea/select

Goal: keep an input's state in a signal.

## Pattern

```rust
let (name, set_name) = signal("Controlled".to_string());

view! {
    <input type="text"
        on:input:target=move |ev| { set_name.set(ev.target().value()); }
        prop:value=name
    />
    <p>"Name is: " {name}</p>
}
```

- `on:input:target` gives a typed `ev.target()`. `input` fires on almost every change; `change` fires roughly on blur. You usually want `input`.
- Use `prop:value`, not `value`. The `value` attribute only sets the initial value (until the user edits); the property keeps updating the input. Same for `prop:checked` on checkboxes.

## bind: shorthand

Equivalent to the above (listener plus dynamic property):

```rust
let (name, set_name) = signal("Controlled".to_string());
let email = RwSignal::new("".to_string());
let spam_me = RwSignal::new(true);
let favorite_color = RwSignal::new("red".to_string());

<input type="text" bind:value=(name, set_name) />
<input type="email" bind:value=email />
<input type="checkbox" bind:checked=spam_me />
<input type="radio" name="color" value="red" bind:group=favorite_color />
```

`bind:value` for text, `bind:checked` for checkboxes, `bind:group` for radio groups. Pass an `RwSignal` or a `(getter, setter)` tuple.

## textarea

No `value` attribute in HTML; the initial value is a text child. To SSR an initial value and keep it reactive, do both:

```rust
<textarea
    prop:value=move || some_value.get()
    on:input:target=move |ev| some_value.set(ev.target().value())
>
    {some_value}
</textarea>
```

## select

Control via `prop:value` on the `<select>` and `on:change:target`:

```rust
let (value, set_value) = signal(0_i32);
<select
    on:change:target=move |ev| { set_value.set(ev.target().value().parse().unwrap()); }
    prop:value=move || value.get().to_string()
>
    <option value="0">"0"</option>
    <option value="1">"1"</option>
</select>
```

## Related

- `computing-software.web-development.leptos.uncontrolled-inputs-noderef`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/05_forms.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
