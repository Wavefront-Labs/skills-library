---
id: computing-software.web-development.angular.signal-queries
name: signal-queries
category: computing-software
field: web-development
product: angular
tags: [angular, queries, viewchild, viewchildren, contentchild, contentchildren, signals]
level: practitioner
status: docs-checked
description: "Signal-based view and content queries (viewChild, viewChildren, contentChild, contentChildren): required queries, locators, read option, descendants."
sources:
  - https://angular.dev/guide/components/queries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Queries find child elements and read values from their injectors. All query functions return signals with up-to-date results, readable in `computed` and `effect`.

- View queries search the component's own template: `viewChild(CustomCardHeader)` and `viewChildren(CustomCardAction)` (signal of an Array).
- Content queries search content nested inside the component where it is used: `contentChild(CustomToggle)` and `contentChildren(CustomMenuItem)`.
- Queries never pierce component boundaries; content queries only see the same template as the component itself.
- Without a match, `viewChild`/`contentChild` are `undefined` (for instance when hidden by `@if`), so the type includes `undefined`.

```ts
header = viewChild(CustomCardHeader);
headerText = computed(() => this.header()?.text);
actions = viewChildren(CustomCardAction);
```

Required queries: `viewChild.required(CustomCardHeader)` and `contentChild.required(CustomCardBody)` report an error when nothing matches, and then `undefined` is not in the type.

Locators: usually a component or directive, or a string naming a template reference variable (`viewChild<ElementRef<HTMLButtonElement>>('save')` for `<button #save>`; the first match wins). CSS selectors are not supported. Any `ProviderToken`, such as an `InjectionToken`, can locate elements by the providers they declare.

Options (second parameter):
- `read`: retrieve a different value from the matched element, most often `ElementRef` or `TemplateRef`, or `Injector`: `contentChild(ExpandoContent, {read: TemplateRef})`, `viewChild('inner', {read: Injector})`. The Injector can be passed to `ngTemplateOutletInjector`.
- `descendants`: `contentChildren` finds only direct children by default, while `contentChild` traverses descendants by default. Set `descendants: true` to traverse all descendants in the same template. View queries always traverse descendants and have no such option.

Pitfalls the guide lists: keep a single source of truth for state shared between components; do not write state directly to child components, or to parent or ancestor components, since this is brittle and prone to NG0100 `ExpressionChangedAfterItHasBeenChecked` errors.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/components/queries (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
