---
id: computing-software.web-development.angular.effects
name: effects
category: computing-software
field: web-development
product: angular
tags: [angular, signals, effect, oncleanup, injection-context, manualcleanup, side-effects]
level: practitioner
status: docs-checked
description: "Angular effect(): when to use it, injection context, view versus root effects, destruction, manualCleanup and onCleanup callbacks."
sources:
  - https://angular.dev/guide/signals/effect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An effect runs whenever one or more signals it read change.

```ts
effect(() => {
  console.log(`The current count is: ${count()}`);
});
```

Effects run at least once, track signal reads dynamically (only those read in the most recent run), and always execute asynchronously during change detection.

Use effects last. Prefer `computed()` for derived values and `linkedSignal()` for values both derived and manually set. If you copy data from one signal to another in an effect, move the source of truth higher up. Appropriate uses: logging for analytics or debugging, syncing to storage (`localStorage`, session storage, cookies), custom DOM behavior not expressible in templates, custom rendering to `<canvas>`, charting or third-party UI libraries. Avoid using effects to propagate state changes: this can cause `ExpressionChangedAfterItHasBeenChecked` errors, infinite circular updates or extra change detection cycles.

Injection context: an effect must be created in one (for example a component, directive or service constructor), or pass an injector:

```ts
private injector = inject(Injector);
initializeLogging(): void {
  effect(() => console.log(`The count is: ${this.count()}`), {injector: this.injector});
}
```

Execution:
- A view effect is created in a component instantiation context (including services tied to component injectors) and runs before its component is checked.
- A root effect is created in a root provided service and runs before all components are checked.
- If a dependency changes during the run, the effect re-runs before change detection moves on.

Destruction: a view effect is destroyed with its component, a root effect with the application. Effects return an `EffectRef` whose `destroy` disposes them; combine with the `manualCleanup` option to disable automatic cleanup, and be careful to destroy such effects.

Cleanup: the function may accept `onCleanup` as its first parameter; the callback runs before the next run or on destruction.

```ts
effect((onCleanup) => {
  const user = currentUser();
  const timer = setTimeout(() => console.log(`1 second ago, the user became ${user}`), 1000);
  onCleanup(() => clearTimeout(timer));
});
```

For DOM work after rendering see `computing-software.web-development.angular.after-render-effect`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/signals/effect (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
