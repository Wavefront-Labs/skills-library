---
id: computing-software.web-development.angular.host-element-bindings
name: host-element-bindings
category: computing-software
field: web-development
product: angular
tags: [angular, host, host-binding, host-listener, host-attribute-token, css-custom-properties]
level: practitioner
status: docs-checked
description: "Bind properties, classes, styles and events to a component host element with the host metadata, binding collision rules, and HostAttributeToken."
sources:
  - https://angular.dev/guide/components/host-elements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A component's host element is the DOM element matching its selector; its template renders inside it. Bind to the host itself with the `host` property of `@Component`:

```ts
@Component({
  host: {
    'role': 'slider',
    '[attr.aria-valuenow]': 'value',
    '[class.active]': 'isActive()',
    '[style.background]': `hasError() ? 'red' : 'green'`,
    '[tabIndex]': 'disabled ? -1 : 0',
    '(keydown)': 'updateValue($event)',
  },
})
export class CustomSlider { /* ... */ }
```

- Global event targets that can prefix an event name: `document:`, `window:` and `body:`.
- Key names like `(keydown.enter)` match `KeyboardEvent.key`, which depends on keyboard layout and language. To match the physical key use the `code` modifier, e.g. `(keydown.code.Enter)`.
- `@HostBinding('attr.aria-valuenow')` and `@HostListener('keydown', ['$event'])` still work but exist only for backwards compatibility; always prefer the `host` property.

Collisions between a binding in the parent template and a host binding for the same property (for example `role="group"` and `[id]="otherId"` on `<profile-photo>`):
- Both static: the instance (template) binding wins.
- One static, one dynamic: the dynamic value wins.
- Both dynamic: the component's host binding wins.

CSS custom properties can be set on the host with a style binding, such as `'[style.--my-background]': 'color()'` in `host`, updating whenever the signal changes and affecting the component and children that use it. A parent can also set it on a child host: `<my-child [style.--my-background]="color()" />`.

Read static host attributes with `HostAttributeToken` and `inject`:

```ts
variation = inject(new HostAttributeToken('variation'));
```
```html
<app-button variation="primary">Click me</app-button>
```

`HostAttributeToken` throws if the attribute is missing unless the injection is optional.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/host-elements (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
