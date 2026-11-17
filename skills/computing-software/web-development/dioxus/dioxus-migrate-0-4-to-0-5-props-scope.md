---
id: computing-software.web-development.dioxus.dioxus-migrate-0-4-to-0-5-props-scope
name: dioxus-migrate-0-4-to-0-5-props-scope
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, migration, dioxus-0-5, scope, props, readonlysignal, mappedsignal, derive-props]
level: practitioner
status: docs-checked
description: "Migrate Dioxus 0.4 code to 0.5: drop the Scope/cx argument, use owned props, replace borrowed props with ReadOnlySignal or MappedSignal, and derive Clone on manual Props."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_05/index.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_05/props.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/untested_05/migration.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/untested_05/migration_props.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus 0.4 to 0.5: scope and props

## Scope is gone
0.4 components took `cx: Scope` and returned `cx.render(rsx!{..})`. In 0.5 hooks, context and spawn are free functions and the component returns `Element` from `rsx!`:
```rust
fn app() -> Element {
    use_hook(|| { /*...*/ });
    provide_context({ /*...*/ });
    spawn(async move { /*...*/ });
    rsx! { /*...*/ }
}
```

## Owned props
0.4 props were borrowed from the scope. In 0.5 props are always owned and are cloned every render:
```rust
#[component]
fn Comp(name: String) -> Element {
    // name is the type String here
    let owned_name: String = name;
    rsx! { "Hello {owned_name}" }
}
```
Because props are cloned each render, making props Copy is recommended: accept `ReadOnlySignal<T>` instead of `T`.
```rust
#[component]
fn CopyPropsComp(name: ReadOnlySignal<String>) -> Element {
    rsx! {
        button {
            onclick: move |_| { println!("Hello {name}"); async move { println!("Hello {name}"); } },
            "Click me"
        }
    }
}
// parent: CopyPropsComp { name: "World" }
```

## Borrowed props removed
Mapped signals act similarly when props borrow from state:
```rust
fn Parent() -> Element {
    let state = use_signal(|| (1, "World".to_string()));
    rsx! { BorrowedComp { name: state.map(|s| &s.1) } }
}
#[component]
fn BorrowedComp(name: MappedSignal<String>) -> Element { rsx! {"Hello {name}"} }
```

## Manual props
Manual prop structs must now derive `Clone` in addition to `Props` and `PartialEq`, and the function takes the props directly:
```rust
#[derive(Props, Clone, PartialEq)]
struct ManualProps { name: String }
fn ManualPropsComponent(props: ManualProps) -> Element { rsx! {"Hello {props.name}"} }
```

## Checked
Checked 2026-11-07 against the 0.5 migration index and Props pages and the migration.rs and migration_props.rs snippet files (all read in full). Confirmed: free-function hooks and Element return, owned props, ReadOnlySignal copy props, MappedSignal for borrowed props, Clone on manual Props. Nothing removed.
Method: documentation only; no commands were run.
