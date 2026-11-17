---
id: computing-software.web-development.angular.template-reference-variables
name: template-reference-variables
category: computing-software
field: web-development
product: angular
tags: [angular, templates, template-reference-variable, exportas, queries, scope]
level: intro
status: docs-checked
description: "Template reference variables with #name: what they point to, exportAs directive references, use with queries, and nested template scope."
sources:
  - https://angular.dev/guide/templates/variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A template reference variable references a DOM element (including custom elements), an Angular component or directive, or a `TemplateRef` from an `ng-template`, so another part of the same template can read from it. Declare with `#` plus a name: `<input #taskInput placeholder="Enter task name" />`.

What it refers to:
- On an Angular component: the component instance (`<my-datepicker #startDate />`).
- On an `<ng-template>`: a `TemplateRef` (`<ng-template #myFragment>...</ng-template>`).
- On any other displayed element: the `HTMLElement` instance.
- On a directive via `exportAs`: set `exportAs` in the directive and assign it explicitly. You cannot refer to a directive that has no `exportAs` name.

```ts
@Directive({
  selector: '[dropZone]',
  exportAs: 'dropZone',
})
export class DropZone { /* ... */ }
```
```html
<section dropZone #firstZone="dropZone">...</section>
```

Queries: mark an element with a variable and query for it by name.

```ts
@Component({
  template: `<input #description value="Original description">`,
})
export class AppComponent {
  @ViewChild('description') input: ElementRef | undefined;
}
```

Scope: variables are scoped to the template that declares them. Control flow blocks (`@if`, `@for`), structural directives and `<ng-template>` create nested scopes. An inner template can read variables from the outer one, but the outer template cannot read a variable declared in a nested one. Define a variable only once so the runtime value stays predictable.

```html
<input #ref1 type="text" [(ngModel)]="firstExample" />
@if (true) {
  <span>Value: {{ ref1.value }}</span>  <!-- works -->
}

@if (true) {
  <input #ref2 type="text" [(ngModel)]="secondExample" />
}
<span>Value: {{ ref2?.value }}</span>   <!-- does not work: ref2 is in the child scope -->
```

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/templates/variables (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page. Removed a cross-reference to another skill that the page does not make.
