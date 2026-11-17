---
id: computing-software.web-development.angular.decorator-inputs
name: decorator-inputs
category: computing-software
field: web-development
product: angular
tags: [angular, component, input-decorator, getter-setter, inputs-array, legacy]
level: practitioner
status: docs-checked
description: "Decorator-based @Input: required, transform and alias options, getter/setter inputs, and the inputs array in @Component for inherited properties."
sources:
  - https://angular.dev/guide/components/inputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Angular team recommends the signal-based `input` function for new projects, but the original `@Input` decorator remains fully supported. Binding syntax in templates is identical: `<custom-slider [value]="50" />`.

```ts
@Component(/* ... */)
export class CustomSlider {
  @Input() value = 0;
  @Input({required: true}) mustSet = 0;               // build-time error if unbound
  @Input({transform: trimString}) label = '';          // same as signal transforms
  @Input({alias: 'sliderValue'}) aliased = 0;          // [sliderValue]="50"
}
function trimString(value: string | undefined) {
  return value?.trim() ?? '';
}
```

The decorator also accepts the alias as its first parameter in place of a config object.

Getters and setters can be inputs, including write-only inputs with just a public setter:

```ts
export class CustomSlider {
  @Input()
  get value(): number { return this.internalValue; }
  set value(newValue: number) { this.internalValue = newValue; }
  private internalValue = 0;
}
```

Prefer input transforms over getters and setters. Avoid complex or costly setters: Angular may invoke an input's setter multiple times, so costly work such as DOM manipulation can hurt performance.

Declare inputs without the decorator via the `inputs` array in `@Component`, useful when a component inherits a property from a base class. An alias goes after a colon:

```ts
@Component({
  ...,
  inputs: ['disabled: sliderDisabled'],
})
export class CustomSlider extends BaseSlider {}
```

Inputs are inherited by child classes, and input names are case-sensitive. See `computing-software.web-development.angular.component-inputs` for the signal API.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/inputs (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
