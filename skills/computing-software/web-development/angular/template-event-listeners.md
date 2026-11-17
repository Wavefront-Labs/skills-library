---
id: computing-software.web-development.angular.template-event-listeners
name: template-event-listeners
category: computing-software
field: web-development
product: angular
tags: [angular, templates, events, event-binding, key-modifiers, keyboard, prevent-default, global-events]
level: intro
status: docs-checked
description: "Add event listeners in Angular templates: $event, key and code modifiers like keyup.shift.enter, global targets, and preventDefault behavior."
sources:
  - https://angular.dev/guide/templates/event-listeners
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap an event name in parentheses and give a statement that runs each time it fires: `<input type="text" (keyup)="updateField()" />`. Any native event works (`click`, `keydown`, `mouseover`, ...). In every listener the variable `$event` holds the event object:

```ts
template: `<input type="text" (keyup)="updateField($event)" />`
updateField(event: KeyboardEvent): void {
  console.log(`The user pressed: ${event.key}`);
}
```

Key modifiers filter keyboard events with a period: `(keyup.enter)`, and combine them: `(keyup.shift.enter)`. Supported modifiers are `alt`, `control`, `meta` and `shift`. By default the name matches `KeyboardEvent.key` values. Add the built-in `code` suffix to match `KeyboardEvent.code` (the physical or virtual button), e.g. `(keydown.code.alt.shift.shiftleft)`. This helps handle keys consistently across operating systems: with Alt on macOS, `key` reports the modified character (Alt + S gives `'ß'`) while `code` corresponds to the button pressed.

Global targets: prefix an event with `window`, `document` or `body`, for example in a component's `host` metadata:

```ts
host: {
  '(window:click)': 'onWindowClick()',
  '(document:click)': 'onDocumentClick()',
  '(body:click)': 'onBodyClick()',
},
```

Preventing default: call `event.preventDefault()` in the handler. If the handler statement evaluates to `false`, Angular calls `preventDefault()` automatically, like native event handler attributes, but the page says to always prefer calling it explicitly so intent is obvious.

```ts
showOverlay(event: PointerEvent): void {
  event.preventDefault();
}
```
```html
<a href="#overlay" (click)="showOverlay($event)">
```

Custom event syntax is possible through custom event plugins (extend `EventManagerPlugin`, register with the `EVENT_MANAGER_PLUGINS` token).

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/templates/event-listeners (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. Claims match the page. Replaced a cross-reference to a nonexistent skill with what the page says about event plugins, and corrected a garbled phrase about host metadata.
