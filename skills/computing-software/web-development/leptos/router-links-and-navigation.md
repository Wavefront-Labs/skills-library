---
id: computing-software.web-development.leptos.router-links-and-navigation
name: router-links-and-navigation
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, router, links, navigation, accessibility]
level: practitioner
status: docs-checked
description: "Use plain a or the router A component for client-side links with relative paths and aria-current, know when the router bails out, and navigate with use_navigate."
sources: [https://book.leptos.dev/router/19_a.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: link between pages client-side and know the escape hatches.

## Plain `<a>`
The router listens to clicks on every `<a>` and navigates client-side. It does not handle a click when:
- `prevent_default()` was called on the event
- Meta, Alt, Ctrl or Shift was held
- the `<a>` has a `target` or `download` attribute, or `rel="external"`
- the link has a different origin

Opt out for a same-domain page outside your Leptos app with `<a rel="external">`.

## `<A/>` component
`leptos_router::components::A` adds two things:
1. Relative hrefs resolve against the nested route it appears in. With a route `/post/:id`, `<A href="1">` resolves correctly where `<a href="1">` likely will not.
2. It sets `aria-current="page"` on the link to the current page, useful for accessibility and for styling via a CSS attribute selector.

Example from the page: `<A href="conversations">"Conversations"</A>` and `<A href="" exact=true>"Contact Info"</A>` for tabs under a parent route.

## Programmatic navigation
Prefer links and forms (best for accessibility and graceful degradation). When you must navigate from code:

```rust
let navigate = leptos_router::hooks::use_navigate();
navigate("/somewhere", Default::default());
```

The second argument is `NavigateOptions`: resolve relative to the current route, replace the history entry, include navigation state, and keep scroll position.

## Gotchas
- Avoid `<button on:click=move |_| navigate(...)>`; any click handler that navigates should be an `<a>`.
- Related: `computing-software.web-development.leptos.router-form-get-search`.

## Checked

2026-11-07: Read in full: router/19_a.md (bail-out list for plain a clicks, rel=external opt-out, the A component's relative resolution and aria-current, use_navigate and NavigateOptions, the on:click accessibility warning, and the inline sandbox source with A href="" exact=true). Every bullet matches the page; no claims were trimmed. Not opened: docs.rs NavigateOptions.

Method: documentation only; no commands were run.
