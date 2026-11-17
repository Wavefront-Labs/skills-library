---
id: computing-software.web-development.angular.component-inputs
name: component-inputs
category: computing-software
field: web-development
product: angular
tags: [angular, component, input, signals, input-required, transform, alias]
level: practitioner
status: docs-checked
description: "Declare signal-based inputs with input() and input.required(), read them, and configure transforms, built-in transforms and aliases."
sources:
  - https://angular.dev/guide/components/inputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inputs let a component accept data. Declare one with the `input` function in a property initializer (the only place you may call it, in components and directives).

```ts
import {Component, input, computed} from '@angular/core';

@Component(/* ... */)
export class CustomSlider {
  value = input(0);                       // InputSignal<number>, type inferred
  maybe = input<number>();                // InputSignal<number | undefined>
  required = input.required<number>();    // must be bound; build-time error otherwise
  label = computed(() => `The slider's value is ${this.value()}`);
}
```

```html
<custom-slider [value]="50" />
```

Facts:
- Inputs are recorded statically at compile time; they cannot be added or removed at run time.
- The returned `InputSignal` is read-only; read it by calling it.
- Required inputs do not automatically include `undefined` in the signal's type.
- Child classes inherit inputs. Input names are case-sensitive.
- Avoid names that collide with DOM element properties, and avoid prefixes (an element hosts only one component).

Config object (second argument):
- `transform`: changes the value when Angular sets it. The transform's parameter type determines what a template may bind. It must be statically analyzable (no conditional or expression-built transforms) and a pure function.
- `alias`: renames the input in templates only, not in TypeScript: `input(0, {alias: 'sliderValue'})` is bound as `[sliderValue]="50"`.

```ts
widthPx = input('', {transform: appendPx});   // accepts number, exposes string
function appendPx(value: number): string { return `${value}px`; }
```

Built-in transforms: `booleanAttribute` (attribute presence means true, but the literal string "false" is false) and `numberAttribute` (NaN if parsing fails).

```ts
disabled = input(false, {transform: booleanAttribute});
value = input(0, {transform: numberAttribute});
```

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/inputs (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
