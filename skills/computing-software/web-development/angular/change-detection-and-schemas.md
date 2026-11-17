---
id: computing-software.web-development.angular.change-detection-and-schemas
name: change-detection-and-schemas
category: computing-software
field: web-development
product: angular
tags: [angular, change-detection, onpush, preservewhitespaces, custom-elements-schema, no-errors-schema]
level: practitioner
status: docs-checked
description: "Advanced @Component options: ChangeDetectionStrategy Eager versus OnPush triggers, preserveWhitespaces, CUSTOM_ELEMENTS_SCHEMA and NO_ERRORS_SCHEMA."
sources:
  - https://angular.dev/guide/components/advanced-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `@Component` decorator takes a `changeDetection` option that controls the component's change detection mode.

- `ChangeDetectionStrategy.Eager` (also `Default`): optional mode. Angular checks whether the component's DOM needs an update whenever any activity may have occurred application-wide, including user interaction, network responses and timers.
- `ChangeDetectionStrategy.OnPush`: per the page, the default strategy since v22. It reduces checking. The framework only checks the component's DOM when:
  - a component input changes as a result of a binding in a template, or
  - an event listener in this component runs, or
  - the component is explicitly marked for check via `ChangeDetectorRef.markForCheck` or something that wraps it, like `AsyncPipe`.

When an OnPush component is checked, Angular also checks all of its ancestor components, traversing upward through the application tree.

```ts
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  /* ... */
})
export class Card {}
```

`preserveWhitespaces`: by default Angular removes and collapses superfluous whitespace in templates, mostly newlines and indentation. Set `preserveWhitespaces: true` in a component's metadata to change that.

Custom element schemas: by default Angular throws an error on an unknown HTML element. Include `CUSTOM_ELEMENTS_SCHEMA` in the component's `schemas` to disable that for the component. `NO_ERRORS_SCHEMA` allows any element and any property.

```ts
import {Component, CUSTOM_ELEMENTS_SCHEMA} from '@angular/core';

@Component({
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: '<some-unknown-component />',
})
export class ComponentWithCustomElements {}
```

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/advanced-configuration (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
Removed the closing cross-reference line about projected content (not on the cited page).

Method: documentation only; no commands were run.
