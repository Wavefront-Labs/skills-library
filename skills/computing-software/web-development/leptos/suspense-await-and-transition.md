---
id: computing-software.web-development.leptos.suspense-await-and-transition
name: suspense-await-and-transition
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, suspense, transition, await, suspend]
level: practitioner
status: docs-checked
description: "Show loading fallbacks for several Leptos resources with Suspense, use Suspend and Await, and avoid flicker on reload with Transition."
sources: [https://book.leptos.dev/async/11_suspense.html, https://book.leptos.dev/async/12_transition.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: show one loading state for all resources read in a subtree, and choose whether it reappears on reloads.

## Suspense

Instead of matching `(a.get(), b.get())` manually, put the reads under `<Suspense/>`. Reading a resource in its children registers it; the `fallback` shows while any are pending and the children show when all are loaded.

```rust
<Suspense fallback=move || view! { <p>"Loading..."</p> }>
    <h3>"A"</h3>
    {move || a.get().map(|a| view! { <ShowA a/> })}
    <h3>"B"</h3>
    {move || b.get().map(|b| view! { <ShowB b/> })}
</Suspense>
```

Each time a resource reloads, the fallback shows again. Adding or removing resources needs no extra matching.

## Suspend

`Suspend::new` makes a renderable `Future`, so you can `.await` resources directly and avoid null checks:

```rust
{move || Suspend::new(async move {
    let a = a.await;
    let b = b.await;
    view! { <ShowA a/> <ShowB b/> }
})}
```

## Await

For a one-off `Future`: `<Await/>` is a `OnceResource` plus `<Suspense/>` with no fallback. It polls once, ignores reactive changes, renders nothing until resolved, then binds the data (by reference) to your variable:

```rust
<Await future=fetch_monkeys(3) let:data>
    <p>{*data} " little monkeys, jumping on the bed."</p>
</Await>
```

## Transition

`<Transition/>` is the same as `<Suspense/>` but shows the fallback only on the first load; later reloads keep showing the old data until new data arrives, preventing flicker. The page's example passes a `set_pending` prop, the setter of `let (pending, set_pending) = signal(false);`, which is set to `true` whenever the transition is ongoing:

```rust
<Transition fallback=move || view! { <p>"Loading initial data..."</p> } set_pending>
    <p>{move || user_data.read().as_deref().map(ToString::to_string)}</p>
</Transition>
```

Related: `computing-software.web-development.leptos.resources-loading-async-data`.

## Gaps

The page defers server-side rendering effects of Suspense to a later chapter.

## Checked

2026-11-07: Read in full: async/11_suspense.md (Suspense, Suspend, Await with its three-point behaviour, inline sandbox source) and async/12_transition.md (Transition behaviour and the tabbed sandbox source). Confirmed the fallback and children behaviour, 'only polls the Future once', and Transition showing the fallback only on first load. One correction: the skill said set_pending receives a WriteSignal<bool>; the page only shows it passed as the setter of signal(false) and set true while the transition is ongoing, so the text now says that. Live sandboxes not opened.

Method: documentation only; no commands were run.
