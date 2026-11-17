---
id: computing-software.web-development.angular.model-inputs
name: model-inputs
category: computing-software
field: web-development
product: angular
tags: [angular, component, model, two-way-binding, signals, change-event]
level: practitioner
status: docs-checked
description: "Use model() inputs so a component can write values back to its parent with two-way binding, including the implicit Change output."
sources:
  - https://angular.dev/guide/components/inputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A model input is an input the component author can also write to. If it is bound with two-way binding, each new value propagates back to the parent's binding.

```ts
@Component(/* ... */)
export class CustomSlider {
  value = model(0);
  increment() {
    this.value.update((oldValue) => oldValue + 10);
  }
}

@Component({
  template: `<custom-slider [(value)]="volume" />`,
})
export class MediaControls {
  volume = signal(0);
}
```

Notes from the guide:
- With a signal in the parent, the binding passes the signal instance, not its value. This keeps `value` and `volume` in sync.
- A plain property works too: `protected volume = 0;` bound with `[(value)]="volume"`.
- Read a model by calling it, including inside reactive contexts such as `computed` and `effect`; write with `set` or `update`.
- Declaring a model also creates an output named after the model with a "Change" suffix. `checked = model(false)` in a directive yields `checkedChange`, usable as `(checkedChange)="handler()"`. Angular emits it whenever you write a new value with `set` or `update`.
- A model can be required or aliased like a standard input. Model inputs do not support input transforms.
- Use them when a component exists to modify a value from user interaction. Custom form controls such as a date picker or combobox should use a model input for their primary value.
- The guide points to its Two-way binding page for the template-side syntax.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/components/inputs (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page. Replaced an invented skill cross-reference with the page's own pointer to its Two-way binding guide.
