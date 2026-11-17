---
id: computing-software.web-development.angular.component-inheritance
name: component-inheritance
category: computing-software
field: web-development
product: angular
tags: [angular, component, inheritance, extends, inject, lifecycle, host-bindings]
level: practitioner
status: docs-checked
description: "How Angular components and directives inherit inputs, outputs, host bindings and lifecycle methods from base classes, and how to forward dependencies."
sources:
  - https://angular.dev/guide/components/inheritance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Components are TypeScript classes with standard JavaScript inheritance. A component can extend any base class, and a component extending another component or a directive inherits some of the base class's decorator metadata and decorated members: host bindings, inputs, outputs and lifecycle methods. The child's own selector and template override the base's.

```ts
@Component({
  selector: 'base-listbox',
  template: ` ... `,
  host: { '(keydown)': 'handleKey($event)' },
})
export class ListboxBase {
  value = input.required<string>();
  handleKey(event: KeyboardEvent) { /* ... */ }
}

@Component({
  selector: 'custom-listbox',
  template: ` ... `,
  host: { '(click)': 'focusActiveOption()' },
})
export class CustomListbox extends ListboxBase {
  disabled = input(false);
  focusActiveOption() { /* ... */ }
}
```

Here `CustomListbox` ends up with two inputs (`value`, `disabled`) and two event listeners (`keydown`, `click`): children get the union of ancestors' inputs, outputs and host bindings plus their own.

Injected dependencies:
- If the base class uses `inject()` as a property initializer, the child inherits the property automatically; no `super` forwarding is needed (`protected element = inject(ElementRef);`).
- If the base injects through constructor parameters, the child must pass them to `super`:

```ts
export class CustomListbox extends ListboxBase {
  constructor(element: ElementRef) {
    super(element);
  }
}
```

Lifecycle methods: a child that implements `ngOnInit` overrides the base's version. To keep the base behavior, call it explicitly:

```ts
override ngOnInit() {
  super.ngOnInit();
  /* ... */
}
```

For inherited properties that need to be declared as inputs or outputs in a child, see the `inputs` and `outputs` metadata arrays in `computing-software.web-development.angular.decorator-inputs` and `computing-software.web-development.angular.component-outputs`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/inheritance (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
