---
id: computing-software.web-development.leptos.generic-and-into-props
name: generic-and-into-props
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, props, generics, into, signal, marker, phantom-data, component]
level: practitioner
status: docs-checked
description: "Accept any reactive value as a Leptos prop using #[prop(into)] Signal, generic props, marker props, and Box dyn for optional closures."
sources: [https://book.leptos.dev/view/03_components.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic, into, marker and optional-generic props

Goal: let one prop accept signals, derived signals and closures.

## into + Signal (works on stable)

`#[prop(into)]` calls `.into()` on the passed value. `Signal<T>` is an enum representing any readable reactive signal or a plain value.

```rust
#[component]
fn ProgressBar(
    #[prop(default = 100)] max: u16,
    #[prop(into)] progress: Signal<i32>
) -> impl IntoView {
    view! { <progress max=max value=progress /> <br/> }
}

// ReadSignal converts via .into(); wrap a derived signal with Signal::derive
<ProgressBar progress=count/>
<ProgressBar progress=Signal::derive(double_count)/>
```

## Generic props

On nightly with the `nightly` feature, signals are functions, so you can take `progress: impl Fn() -> i32 + Send + Sync + 'static`. Generics may also use a `where` clause or inline `F: Fn() -> i32 + 'static`.

Specify a generic in the view with type syntax, `<Component<T>/>`, not turbofish `<Component::<T>/>`. Nested generics like `<SizeOf<Vec<T>>/>` are not parseable by the view macro.

## marker props

Props become a struct, so every generic type must appear in a field. `#[prop(optional)] _ty: PhantomData<T>` works but generates docs and a setter; `#[prop(marker)]` removes it from docs and builder:

```rust
#[component]
fn SizeOf<T: Sized>(#[prop(marker)] _ty: PhantomData<T>) -> impl IntoView {
    std::mem::size_of::<T>()
}
// <SizeOf<usize>/>  <SizeOf<String>/>
```

## Optional generic props

An optional prop of generic closure type `Option<F>` cannot compile because the compiler cannot infer `F` and closure types are unnameable. Use a concrete boxed type:

```rust
#[prop(optional)] progress: Option<Box<dyn Fn() -> i32 + Send + Sync>>,
```

`&dyn Fn() -> i32` causes lifetime issues in this case.

## Related

- `computing-software.web-development.leptos.component-props`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/03_components.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
