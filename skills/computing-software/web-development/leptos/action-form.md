---
id: computing-software.web-development.leptos.action-form
name: action-form
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, action-form, forms, server-action, validation]
level: practitioner
status: docs-checked
description: "Wire a Leptos ServerAction to an ActionForm so it submits with or without WASM, validate with on:submit:capture and FromFormData, and post nested structs."
sources: [https://book.leptos.dev/progressive_enhancement/action_form.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ActionForm: server actions from HTML forms

Goal: call a server function from a `<form>` that works with and without JS/WASM.

## Steps

1. Define the server function with `#[server]`.
2. Create `ServerAction::<AddTodo>::new()` (the type of the server function you defined, as in the example).
3. Render `<ActionForm action=...>`.
4. Name form fields exactly like the function arguments.

```rust
#[server]
pub async fn add_todo(title: String) -> Result<(), ServerFnError> { todo!() }

#[component]
fn AddTodo() -> impl IntoView {
    let add_todo = ServerAction::<AddTodo>::new();
    let value = add_todo.value();                    // latest returned value
    let has_error = move || value.with(|val| matches!(val, Some(Err(_))));
    view! {
        <ActionForm action=add_todo>
            <label>"Add a Todo" <input type="text" name="title"/></label>
            <input type="submit" value="Add"/>
        </ActionForm>
    }
}
```

With JS/WASM it submits without reload and exposes `.input()`, `.pending()`, etc. Without JS/WASM it submits with a page reload; a `redirect` call (leptos_axum or leptos_actix) redirects, and by default it returns to the current page.

Only the default URL-encoded POST encoding works with `<ActionForm/>`.

## Client-side validation

`<ActionForm/>` fires a normal `submit` event. Use HTML validation or a handler calling `ev.prevent_default()`; `FromFormData` can parse the data:

```rust
let on_submit = move |ev| {
    let data = AddTodo::from_event(&ev);
    if data.is_err() || data.unwrap().title == "nope!" {
        ev.prevent_default();
    }
}
// <ActionForm on:submit:capture=on_submit /* ... */>
```

Use `on:submit:capture` (capture phase), not `on:submit`, so the handler runs before the component's built-in submit handler (see Leptos issue 3872).

## Nested structs

Use `serde_qs` indexing in field names for struct arguments:

```html
<input type="text" name="hefty_arg[first_name]"/>
<input type="text" name="hefty_arg[settings][display_name]"/>
```

where the server function takes `hefty_arg: HeftyData` and the structs derive `Serialize, Deserialize`.

Related: computing-software.web-development.leptos.server-function-basics, computing-software.web-development.leptos.server-response-and-redirect.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/progressive_enhancement/action_form.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
