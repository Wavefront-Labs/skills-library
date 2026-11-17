---
id: computing-software.web-development.angular.component-lifecycle-hooks
name: component-lifecycle-hooks
category: computing-software
field: web-development
product: angular
tags: [angular, lifecycle, ngoninit, ngonchanges, ngondestroy, destroyref, ngdocheck]
level: practitioner
status: docs-checked
description: "Angular component lifecycle hooks in order, what each is for, SimpleChanges, DestroyRef cleanup, lifecycle interfaces and ordering rules."
sources:
  - https://angular.dev/guide/components/lifecycle
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Order: `constructor`, then during change detection `ngOnChanges`, `ngOnInit`, `ngDoCheck`, `ngAfterContentInit`, `ngAfterContentChecked`, `ngAfterViewInit`, `ngAfterViewChecked`, then rendering callbacks (`afterNextRender`, `afterEveryRender`), and finally `ngOnDestroy`. On the first pass `ngOnChanges` runs before `ngOnInit`, and `ngDoCheck` runs after `ngOnInit`. Angular visits each component exactly once per traversal, so avoid state changes in the middle of it.

- `ngOnInit`: runs once after inputs are initialized, before the component's template is initialized.
- `ngOnChanges`: runs every time inputs change, before the template is checked. It receives `SimpleChanges` mapping each input name to `previousValue`, `currentValue` and `firstChange`. Aliased inputs still key by the TypeScript property name.
- `ngDoCheck`: runs every time the component is checked; use only to detect state changes outside normal change detection, because it runs very frequently.
- `ngAfterContentInit` / `ngAfterContentChecked`: content initialized / content checked. Good for reading content queries.
- `ngAfterViewInit` / `ngAfterViewChecked`: view initialized / checked. Good for reading view queries.
- `ngOnDestroy`: runs once just before destruction (for example hidden by `@if` or navigating away).

The `*Checked` hooks and `ngDoCheck` run very frequently and can hurt performance; avoid them unless there is no alternative. In the after-content and after-view hooks, avoid changing non-signal state that has already been rendered, which can cause `ExpressionChangedAfterItHasBeenCheckedError` (NG0100).

```ts
ngOnChanges(changes: SimpleChanges<UserProfile>) {
  if (changes.name) {
    console.log(changes.name.previousValue, changes.name.currentValue, changes.name.firstChange);
  }
}
```

Cleanup alternative to `ngOnDestroy`: inject `DestroyRef` and register callbacks, which can be passed to code outside the component:

```ts
constructor() {
  inject(DestroyRef).onDestroy(() => console.log('UserProfile destruction'));
}
```

`DestroyRef.destroyed` tells you whether the instance is already destroyed, helping avoid errors such as NG0911 (view already destroyed) in delayed or asynchronous logic.

Each hook has an interface named without the `ng` prefix (`OnInit` for `ngOnInit`) that you can `implements` to catch typos. When a component and directives share an element, including through `hostDirectives`, the order of a given hook between them is not guaranteed.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/lifecycle (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
