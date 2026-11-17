---
id: computing-software.web-development.angular.control-flow-if-switch
name: control-flow-if-switch
category: computing-software
field: web-development
product: angular
tags: [angular, templates, control-flow, if-block, switch-block, exhaustive-checking, let]
level: intro
status: docs-checked
description: "Angular template @if, @else if, @else with as aliasing, and @switch with @case, @default and exhaustive type checking using @default never."
sources:
  - https://angular.dev/guide/templates/control-flow
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`@if` renders its content when the condition is truthy; add any number of `@else if` blocks and one `@else`:

```html
@if (a > b) {
  {{ a }} is greater than {{ b }}
} @else if (b > a) {
  {{ a }} is less than {{ b }}
} @else {
  {{ a }} is equal to {{ b }}
}
```

Save the condition result in a variable inside the block:

```html
@if (user.profile.settings.startDate; as startDate) {
  {{ startDate }}
}
```

`@switch` resembles a JavaScript switch. The value is compared to each case with `===`, there is no fallthrough (no `break` needed), consecutive `@case` statements share a block, `@default` is optional, and if nothing matches and there is no `@default`, nothing is shown.

```html
@switch (userPermissions) {
  @case ('admin') {
    <app-admin-dashboard />
  }
  @case ('reviewer')
  @case ('editor') {
    <app-editor-dashboard />
  }
  @default {
    <app-viewer-dashboard />
  }
}
```

Exhaustive type checking: `@default never;` declares no remaining cases should exist, so if a union type is extended and a case is not covered, the template type checker reports an error.

```html
@switch (state) {
  @case ('loggedOut') { <button>Login</button> }
  @case ('loggedIn') { <p>Welcome back!</p> }
  @default never;
}
```

Limits and variants from the page:
- Exhaustiveness relies on TypeScript type narrowing, which only works on variables, not function calls or signals such as `@switch (state())`. Workaround: assign it to a `@let` variable, e.g. `@let mySignal = this.mySignal()`.
- When the switched expression is nested in a union, name the expression to check: `@switch (state.mode) { ... @default never(state); }`.

For loops see `computing-software.web-development.angular.control-flow-for`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/templates/control-flow (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
