---
id: computing-software.web-development.angular.let-declarations
name: let-declarations
category: computing-software
field: web-development
product: angular
tags: [angular, templates, let-declaration, template-variables, scope, async-pipe]
level: practitioner
status: docs-checked
description: "Declare local template variables with @let: syntax, one variable per declaration, no reassignment, and view scoping without hoisting."
sources:
  - https://angular.dev/guide/templates/variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`@let` declares a local variable from a template expression and reuses it in the template, like JavaScript `let`. Angular keeps its value up to date with the expression, like a binding.

```html
@let name = user.name;
@let greeting = 'Hello, ' + name;
@let data = data$ | async;
@let pi = 3.14159;
@let coordinates = {x: 50, y: 100};
@let longExpression =
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit ' +
  'sed do eiusmod tempor incididunt ut labore et dolore magna ' +
  'Ut enim ad minim veniam...';
```

Each `@let` declares exactly one variable; commas do not declare several. Reuse it afterward in the same template:

```html
@let user = user$ | async;

@if (user) {
  <h1>Hello, {{ user.name }}</h1>
  <user-avatar [photo]="user.photo" />
  <button (click)="update(user)">Update profile</button>
}
```

Assignability: unlike JavaScript `let`, a `@let` cannot be reassigned. `<button (click)="value = value + 1">` after `@let value = 1;` is invalid.

Scope: `@let` is scoped to the current view and its descendants. Angular creates a new view at component boundaries and wherever dynamic content may appear (control flow blocks, `@defer` blocks, structural directives). Declarations are not hoisted, so parent views and siblings cannot access them:

```html
@let topLevel = value;
<div>
  @let insideDiv = value;
</div>
{{ topLevel }}   <!-- valid -->
{{ insideDiv }}  <!-- valid -->
@if (condition) {
  @let nested = value;
}
{{ nested }}     <!-- error, not hoisted from @if -->
```

Formal syntax: the `@let` keyword, one or more whitespaces (not newlines), a valid JavaScript name, optional whitespace, `=`, optional whitespace, an Angular expression (may be multi-line), terminated by `;`.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/templates/variables (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page. Removed a cross-reference to another skill that the page does not make.
