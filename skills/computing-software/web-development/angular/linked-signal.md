---
id: computing-software.web-development.angular.linked-signal
name: linked-signal
category: computing-software
field: web-development
product: angular
tags: [angular, signals, linkedsignal, dependent-state, equality, writable-computed]
level: practitioner
status: docs-checked
description: "Use linkedSignal for writable state tied to other signals: source and computation with previous, custom equality and a custom set that writes back."
sources:
  - https://angular.dev/guide/signals/linked-signal
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`linkedSignal` holds state intrinsically linked to other state. It works like `signal`, but you pass a computation function like `computed` instead of a default. When the computation's result changes, the `linkedSignal` takes the new result, so it always holds a valid value.

```ts
shippingOptions: Signal<ShippingMethod[]> = getShippingOptions();
selectedOption = linkedSignal(() => this.shippingOptions()[0]);

changeShipping(index: number) {
  this.selectedOption.set(this.shippingOptions()[index]);
}
```

With `shippingOptions = signal(['Ground', 'Air', 'Sea'])`, setting `selectedOption` to `'Sea'` sticks until `shippingOptions` changes, then it resets to the new first option.

Accounting for previous state: pass separate `source` and `computation`. The computation receives the new source value and `previous` (with `previous.source` and `previous.value`). Provide generic type arguments explicitly when using `previous` (first is the source type, second is the output type).

```ts
selectedOption = linkedSignal<ShippingMethod[], ShippingMethod>({
  source: this.shippingOptions,
  computation: (newOptions, previous) => {
    return newOptions.find((opt) => opt.id === previous?.value.id) ?? newOptions[0];
  },
});
```

The `source` can be any signal (a `computed`, a component `input`). The value also updates when any signal read in the computation changes.

Custom equality, used by downstream dependencies:

```ts
const activeUserEditCopy = linkedSignal(() => activeUser(), {
  equal: (a, b) => a.id === b.id,
});
```

Custom `set`: pass `set` to make `set` and `update` write back to the source of truth. It receives the new value and `rawSet`, which updates the linked signal's internal state directly and skips the computation (useful when it is expensive and you know the result).

```ts
const tempC = signal(0);
const tempF = linkedSignal(() => (tempC() * 9) / 5 + 32, {
  set: (valF) => tempC.set(((valF - 32) * 5) / 9),
});
tempF.set(212); // tempC() is 100
```

Nested property in a parent object: `linkedSignal(() => order().shippingMethod, { set: (m) => order.update((o) => ({...o, shippingMethod: m})) })` performs an immutable update of the parent.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/signals/linked-signal (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
