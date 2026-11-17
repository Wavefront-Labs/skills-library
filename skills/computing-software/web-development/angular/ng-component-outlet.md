---
id: computing-software.web-development.angular.ng-component-outlet
name: ng-component-outlet
category: computing-software
field: web-development
product: angular
tags: [angular, ngcomponentoutlet, dynamic-components, lazy-loading, content-projection, injector]
level: practitioner
status: docs-checked
description: "Render components dynamically in a template with NgComponentOutlet: inputs, projected content, custom injector, componentInstance and lazy dynamic import."
sources:
  - https://angular.dev/guide/components/programmatic-rendering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`NgComponentOutlet` is a structural directive from `@angular/common` that renders a component chosen at run time. Add it to `imports`.

```ts
@Component({
  imports: [NgComponentOutlet],
  template: `
    <p>Profile for {{ user().name }}</p>
    <ng-container *ngComponentOutlet="bioComponent()" />
  `,
})
export class CustomDialog {
  user = input.required<User>();
  bioComponent = computed(() => (this.user().isAdmin ? AdminBio : StandardBio));
}
```

Options in the microsyntax:
- Inputs: `*ngComponentOutlet="greetingComponent; inputs: greetingInputs()"` where the object keys are input names; updating the signal keeps the dynamic component in sync.
- Projected content: `*ngComponentOutlet="cardComponent; content: cardContent()"`. The value is an array of projection slots, one per `<ng-content>`, e.g. `[this.vcr.createEmbeddedView(template).rootNodes]`. Hydration does not support projecting DOM nodes created with native DOM APIs (NG0503); use Angular APIs or add `ngSkipHydration`.
- Injector: `*ngComponentOutlet="panelComponent; injector: customInjector"` with `Injector.create({providers: [{provide: THEME_DATA, useValue: 'dark'}]})`.
- Instance: use `exportAs`, `<ng-container [ngComponentOutlet]="counterComponent" #outlet="ngComponentOutlet" />` then `outlet.componentInstance?.increment()`. `componentInstance` is `null` before the component is rendered.

Lazy loading without `@defer`: the guide recommends the built-in `@defer` feature first; if it does not fit, combine the outlet with a standard dynamic import.

```ts
advancedSettings: {new(): AdvancedSettings} | undefined;
async loadAdvanced() {
  const { AdvancedSettings } = await import('path/to/advanced_settings.js');
  this.advancedSettings = AdvancedSettings;
}
```
```html
<ng-container *ngComponentOutlet="advancedSettings" />
```

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/components/programmatic-rendering (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page. Removed a cross-reference to another skill that the page does not make.
