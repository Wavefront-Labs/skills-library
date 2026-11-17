---
id: computing-software.web-development.angular.class-and-style-binding
name: class-and-style-binding
category: computing-software
field: web-development
product: angular
tags: [angular, templates, class-binding, style-binding, ngclass, css]
level: intro
status: docs-checked
description: "Bind CSS classes and style properties in Angular templates: single class, class with string/array/object, style units, multi-style bindings and === update rule."
sources:
  - https://angular.dev/guide/templates/binding
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Class bindings:
- Single class, toggled by truthiness: `<ul [class.expanded]="isExpanded()">`.
- Whole `class` property accepts a space-separated `string`, a `string[]`, or a `Record<string, any>` whose truthy keys are applied.

```ts
listClasses = 'full-width outlined';
sectionClasses = signal(['expandable', 'elevated']);
buttonClasses = signal({highlighted: true, embiggened: false});
```
```html
<ul [class]="listClasses"> ... </ul>
<section [class]="sectionClasses()"> ... </section>
<button [class]="buttonClasses()"> ... </button>
```

Strings are split on whitespace and empty strings ignored. Static classes, a bound `class` and specific class bindings are combined: `<ul class="list" [class]="listType()" [class.expanded]="isExpanded()">` renders `list box expanded`. Angular does not guarantee a class order. Multiple bindings for the same class are resolved by Angular's style precedence order.

For arrays and objects Angular compares previous and current values with `===`, so you must create a new array or object instance when modifying them. Class bindings do not support space-separated names in a single key or in-place object mutation; use the `ngClass` directive if you need that.

Style bindings:
- Single property: `<section [style.display]="isExpanded() ? 'block' : 'none'">`.
- With units: `<section [style.height.px]="sectionHeightInPixels()">`.
- Multiple values via `[style]`, as a string of declarations or a `Record<string, any>`:

```ts
listStyles = signal('display: flex; padding: 8px');
sectionStyles = signal({border: '1px solid black', 'font-weight': 'bold'});
```
```html
<ul [style]="listStyles()"> ... </ul>
<section [style]="sectionStyles()"> ... </section>
```

When binding `style` to an object, Angular compares with `===`, so create a new object to apply updates. Multiple bindings of the same style property follow style precedence.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/templates/binding (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
Removed the claim that CSS custom properties can be bound with `[style.--my-background]` (not on the cited page).

Method: documentation only; no commands were run.
