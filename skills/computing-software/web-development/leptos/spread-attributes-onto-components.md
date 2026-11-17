---
id: computing-software.web-development.leptos.spread-attributes-onto-components
name: spread-attributes-onto-components
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, spread, attributes, component, attribute-interceptor, view-macro]
level: practitioner
status: docs-checked
description: "Spread extra attributes, classes, styles and event handlers onto a Leptos component with attr:, the {..} marker and impl Attribute."
sources: [https://book.leptos.dev/view/03_components.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spread attributes onto a component

Goal: let callers add their own `class`, `id`, listeners etc. to a component without declaring a prop for each.

Attributes added to a component are applied to all top-level HTML elements its view returns.

```rust
// build an attribute list: view! with {..} as the tag name
let spread_onto_component = view! {
    <{..} aria-label="a component with attribute spreading"/>
};

view! {
    <ComponentThatTakesSpread
        // plain identifiers are props
        some_prop="foo"
        another_prop=42

        // class:, style:, prop:, on: work as on elements
        class:foo=true
        style:font-weight="bold"
        prop:cool=42
        on:click=move |_| alert("clicked ComponentThatTakesSpread")

        // a plain HTML attribute needs the attr: prefix
        attr:id="foo"

        // or separate props from attributes with {..}
        {..} // everything after this is an HTML attribute
        title="ooh, a title!"

        // add a whole attribute list
        {..spread_onto_component}
    />
}
```

## Reuse via a function

Return `impl Attribute`:

```rust
fn spread_onto_component() -> impl Attribute {
    view!{ <{..} aria-label="a component with attribute spreading"/> }
}

view!{ <SomeComponent {..spread_onto_component()} /> }
```

## Applying to only some elements

Spread hits all top-level elements. To target a subset, pass via a component prop, or use `AttributeInterceptor` (docs.rs leptos attribute_interceptor). See the `spread` example in the Leptos repo.

## Related

- `computing-software.web-development.leptos.component-props`

## Checked

2026-11-07: Read in full: view/03_components.md (spread applies to all top-level elements, attr: prefix, the {..} syntax, impl Attribute, AttributeInterceptor). Every statement matches. No claims were trimmed. Live sandbox not opened.

Method: documentation only; no commands were run.
