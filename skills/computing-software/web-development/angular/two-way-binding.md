---
id: computing-software.web-development.angular.two-way-binding
name: two-way-binding
category: computing-software
field: web-development
product: angular
tags: [angular, templates, two-way-binding, ngmodel, formsmodule, model, banana-in-a-box]
level: intro
status: docs-checked
description: "Angular [()] two-way binding with ngModel on form controls and between parent and child components using model()."
sources:
  - https://angular.dev/guide/templates/two-way-binding
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two-way binding shorthand binds a value into an element while letting that element propagate changes back. The syntax combines property binding `[]` and event binding `()` as `[()]`, informally called "banana-in-a-box".

Form controls: import `FormsModule` from `@angular/forms`, use `ngModel` with the syntax, and assign the state it should update.

```ts
import {Component} from '@angular/core';
import {FormsModule} from '@angular/forms';

@Component({
  imports: [FormsModule],
  template: `
    <main>
      <h2>Hello {{ firstName }}!</h2>
      <input type="text" [(ngModel)]="firstName" />
    </main>
  `,
})
export class App {
  firstName = 'Ada';
}
```

Between components the child needs a `model` property; the parent wraps the model's name in `[()]` and assigns a property or signal to it.

```ts
// counter.ts
@Component({
  selector: 'app-counter',
  template: `
    <button (click)="updateCount(-1)">-</button>
    <span>{{ count() }}</span>
    <button (click)="updateCount(+1)">+</button>
  `,
})
export class Counter {
  count = model<number>(0);
  updateCount(amount: number): void {
    this.count.update((currentCount) => currentCount + amount);
  }
}

// app.ts
@Component({
  selector: 'app-root',
  imports: [Counter],
  template: `<app-counter [(count)]="initialCount"></app-counter>`,
})
export class App {
  initialCount = 18;
}
```

The parent sets the initial state while the child holds the logic to update and render it.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/templates/two-way-binding (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page. Removed a cross-reference to another skill that the page does not make.
