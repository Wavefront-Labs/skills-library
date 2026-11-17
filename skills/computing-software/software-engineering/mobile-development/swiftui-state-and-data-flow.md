---
id: computing-software.software-engineering.mobile-development.swiftui-state-and-data-flow
name: swiftui-state-and-data-flow
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-ui, ios, swiftui, swiftui-state, observable, data-flow]
level: practitioner
status: draft
description: "Choose the right SwiftUI state tool: @State, @Binding, @Observable models with @Bindable and @Environment, view identity and lifetime, and avoiding redundant view updates."
sources:
  - https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app
  - https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro
  - https://developer.apple.com/documentation/swiftui/state
  - https://developer.apple.com/videos/play/wwdc2021/10022/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SwiftUI state and data flow

**Goal:** a single source of truth per piece of data, views that update exactly when their data changes, and state that is not accidentally reset.

## 1. Which property wrapper
| Need | Use (iOS 17+) | Pre-iOS 17 |
|---|---|---|
| Private, view-owned value | `@State var count = 0` | same |
| Child edits parent's value | `@Binding var isOn: Bool` | same |
| Reference-type model owned by a view | `@State var model = Model()` with `@Observable class Model` | `@StateObject` + `ObservableObject` |
| Model passed in, need bindings to its properties | `@Bindable var model: Model` | `@ObservedObject` |
| App-wide dependency | `.environment(model)` + `@Environment(Model.self)` | `@EnvironmentObject` |
| Persisted small settings | `@AppStorage("key")`, `@SceneStorage` | same |

## 2. @Observable models
```swift
@Observable
final class CartModel {
    var items: [Item] = []
    var promoCode = ""
    var total: Decimal { items.reduce(0) { $0 + $1.price } }
    func add(_ i: Item) { items.append(i) }
}

struct CartView: View {
    @State private var cart = CartModel()          // owner: created once per view identity
    var body: some View {
        List(cart.items) { ItemRow(item: $0) }
        PromoField(cart: cart)
        Text(cart.total, format: .currency(code: "EUR"))
    }
}
struct PromoField: View {
    @Bindable var cart: CartModel
    var body: some View { TextField("Promo", text: $cart.promoCode) }
}
```
With `@Observable`, a view re-renders only when properties **it read in body** change, unlike `ObservableObject` where any `@Published` change invalidates all observers.

## 3. Identity and lifetime
- `@State` storage lives as long as the view's **identity** in the hierarchy. Changing identity (different branch of an `if`, `.id(x)` changing) resets it.
- `ForEach` needs stable identifiers (`Identifiable` with persistent IDs, not array indices or `UUID()` created on the fly).
- Prefer modifiers that keep identity (`.opacity`, ternaries inside a modifier) over `if/else` swapping views when state must persist.

## 4. Async work
```swift
.task(id: query) {                  // cancelled and restarted when query changes, cancelled on disappear
    results = await search(query)
}
```
Mark models that update UI from async code `@MainActor`.

## 5. Avoid
- Initialising `@State` from a parameter (`@State var x: Int` set in init) only uses the first value; later parameter changes are ignored. Derive instead, or use `.onChange`.
- Holding an `@Observable` model in a plain `let` inside a view that creates it each time: it is recreated on every parent update. Owners use `@State`.
- Heavy computation in `body`; it runs often. Cache in the model.

## Gotchas
- `@Observable` requires iOS 17/macOS 14; mixed codebases need both patterns.
- Classes marked `@Observable` should not also use `@Published`.
- Environment values are read-only by default; pass bindings or methods to mutate.
- Debug updates: `let _ = Self._printChanges()` inside `body` logs why a view re-rendered.

## Verify
- `_printChanges()` shows only expected invalidations when editing one field, state survives scrolling items off/on screen, and previews render with mock models.
