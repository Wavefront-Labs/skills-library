---
id: computing-software.web-development.angular.using-pipes
name: using-pipes
category: computing-software
field: web-development
product: angular
tags: [angular, pipes, templates, async-pipe, date-pipe, currency-pipe, precedence, pure]
level: intro
status: docs-checked
description: "Use built-in Angular pipes in templates: importing them, chaining, parameters, operator precedence with ternaries, and pure pipe change detection."
sources:
  - https://angular.dev/guide/templates/pipes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pipes transform values declaratively in template expressions with the `|` character. It is a binary operator: left side is the value, right side is the pipe name and arguments. Angular template expressions do not support bitwise operators.

```ts
import {CurrencyPipe, DatePipe, TitleCasePipe} from '@angular/common';

@Component({
  imports: [CurrencyPipe, DatePipe, TitleCasePipe],
  template: `
    <h1>Purchases from {{ company | titlecase }} on {{ purchasedOn | date }}</h1>
    <p>Total: {{ amount | currency }}</p>
  `,
})
export class ShoppingCart {}
```

Import each pipe class into the component's `imports`. Output follows the user's locale.

Built-in pipes in `@angular/common`: `AsyncPipe` (Promise or Observable), `CurrencyPipe`, `DatePipe`, `DecimalPipe`, `I18nPluralPipe`, `I18nSelectPipe`, `JsonPipe` (via `JSON.stringify`, for debugging), `KeyValuePipe`, `LowerCasePipe`, `PercentPipe`, `SlicePipe`, `TitleCasePipe`, `UpperCasePipe`.

Chaining runs left to right: `{{ scheduledOn | date | uppercase }}`. Parameters follow a colon, and more are separated by colons: `{{ scheduledOn | date: 'hh:mm' }}` and `{{ scheduledOn | date: 'hh:mm' : 'UTC' }}`.

Precedence: the pipe operator is lower than `+`, `-`, `*`, `/`, `%`, `&&`, `||` and `??`, so `{{ firstName + lastName | uppercase }}` concatenates first. It is higher than the ternary operator, so `{{ isAdmin ? 'Access granted' : 'Access denied' | uppercase }}` parses as `isAdmin ? 'Access granted' : ('Access denied' | uppercase)`. Use parentheses: `{{ (isAdmin ? 'Access granted' : 'Access denied') | uppercase }}`.

Change detection: all pipes are `pure` by default; they run only when a primitive input value or object reference changes. Mutating object properties or array items is not detected unless the whole reference is replaced (or the pipe is marked impure with `pure: false`; the guide says to avoid impure pipes unless necessary).

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/templates/pipes (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page. Replaced a cross-reference to a nonexistent skill with the page's own statements on impure pipes.
