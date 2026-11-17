---
id: computing-software.web-development.angular.component-outputs
name: component-outputs
category: computing-software
field: web-development
product: angular
tags: [angular, component, output, events, event-emitter, output-ref]
level: practitioner
status: docs-checked
description: "Define custom component events with output(), emit data, alias, subscribe programmatically, and the legacy @Output EventEmitter and outputs array."
sources:
  - https://angular.dev/guide/components/outputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Define a custom event by assigning a property to the `output` function (only callable in component and directive property initializers):

```ts
@Component({/*...*/})
export class ExpandablePanel {
  panelClosed = output<void>();
}
```
```html
<expandable-panel (panelClosed)="savePanelState()" />
```

Emit with `this.panelClosed.emit()`; pass data with `emit(7)` or an object. In the template the data is `$event`: `(valueChanged)="logValue($event)"`.

Facts: Angular custom events do not bubble up the DOM. Output names are case-sensitive and are inherited by child classes.

Alias: `changed = output({alias: 'valueChanged'})` is used as `(valueChanged)="saveVolume()"`; the alias does not change TypeScript usage.

Subscribe programmatically to dynamically created components via `OutputRef.subscribe`. Angular automatically cleans up subscriptions when it destroys the component; you can also call `unsubscribe()` on the returned `OutputRefSubscription`.

```ts
const ref: ComponentRef<SomeComponent> = viewContainerRef.createComponent(/*...*/);
const sub = ref.instance.someEventProperty.subscribe((eventData) => console.log(eventData));
sub.unsubscribe();
```

Naming: avoid names that collide with DOM element events, do not add prefixes, use camelCase, and avoid prefixing with "on".

Legacy decorator form (still supported; `output` is recommended for new projects):

```ts
@Output() panelClosed = new EventEmitter<void>();
@Output('valueChanged') changed = new EventEmitter<number>();   // alias
```

The `outputs` array in `@Component` covers inherited properties, with an alias after a colon: `outputs: ['valueChanged: volumeChanged']`.

RxJS interop is covered in the separate RxJS interop output guide.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/outputs (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
