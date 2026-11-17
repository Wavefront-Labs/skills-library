---
id: computing-software.web-development.leptos.router-form-get-search
name: router-form-get-search
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, router, form, search, resource, query-string]
level: practitioner
status: docs-checked
description: "Build a live search stored in the URL query with the router Form component, a Resource keyed on use_query_map, and oninput requestSubmit."
sources: [https://book.leptos.dev/router/20_form.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a search box whose state lives in the URL, updates without page reload, and works shareably.

## Background
Plain HTML navigates via `<a>` (GET), `<form method="GET">` (inputs in the query string) and `<form method="POST">` (inputs in the body). The router's `<Form/>` (`leptos_router::components::Form`) behaves like `<form>` but navigates client-side for both GET and POST. It also underlies `<ActionForm/>` and `<MultiActionForm/>`.

## Method
```rust
#[component]
pub fn FormExample() -> impl IntoView {
    let query = use_query_map();
    let search = move || query.read().get("q").unwrap_or_default();
    let search_results = Resource::new(search, |_| fetch_results());

    view! {
        <Form method="GET" action="">
            <input type="search" name="q" value=search/>
            <input type="submit"/>
        </Form>
        <Transition fallback=move || ()>
            /* render search results */
        </Transition>
    }
}
```
Submitting navigates to `?q=...` on the client; `search` changes, so the `Resource` reloads, and `<Transition/>` keeps showing old results until new ones arrive. Data flows URL to resource to UI, and the page works when refreshed or shared. The page notes it also works well without loading WASM once server rendering is added.

## Submit on every keystroke
Drop the button and add a plain HTML attribute (not `on:input`):

```rust
<input type="search" name="q" value=search
    oninput="this.form.requestSubmit()"/>
```
`oninput` here is a JavaScript string; `this.form.requestSubmit()` fires the form's submit event, which `<Form/>` catches. The page's other example does the same with `onchange` on a `<select>`.

## Gotchas
- Input `name` becomes the query-string key.

## Checked

2026-11-07: Read in full: router/20_form.md (the three ways HTML navigates, Form with GET and POST, the FormExample search snippet, the oninput requestSubmit variant, and the inline sandbox source showing onchange on a select and input names as query keys). Confirmed that the page says the pattern works without loading WASM once server rendering is introduced. No claims were trimmed. The live sandbox was not opened (source is inline).

Method: documentation only; no commands were run.
