---
id: computing-software.web-development.angular.template-property-binding
name: template-property-binding
category: computing-software
field: web-development
product: angular
tags: [angular, templates, binding, interpolation, property-binding, attribute-binding, aria]
level: intro
status: docs-checked
description: "Bind dynamic text with interpolation, DOM and component properties with square brackets, attributes with attr., and ARIA attributes in Angular templates."
sources:
  - https://angular.dev/guide/templates/binding
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A binding keeps a template connected to component data.

Text interpolation uses double curly braces anywhere you would write text: `<p>Your color preference is {{ theme() }}.</p>`. Values are converted to strings; `null` and `undefined` render as an empty string; objects and arrays use `toString`. Bindings that change over time should read signals: Angular tracks signals read in the template and updates when they change, while a plain property such as `{{ welcomeMessage }}` does not necessarily update.

Property binding uses square brackets and works on DOM element properties, component inputs and directive inputs:

```html
<button [disabled]="isFormValid()">Save</button>
<my-listbox [value]="mySelection()" />
<img [ngSrc]="profilePhotoUrl()" alt="The current user's profile photo" />
```

Attribute binding uses the `attr.` prefix for attributes with no corresponding DOM property, such as SVG attributes. Angular calls `setAttribute`, and calls `removeAttribute` when the value is `null` or `undefined`:

```html
<ul [attr.role]="listRole()">
```

Interpolation inside a property or attribute value is treated as a property binding:

```html
<img src="profile-photo.jpg" alt="Profile photo of {{ firstName() }}" />
```

ARIA attributes: Angular supports binding string values, writing the string to the attribute and removing it for `null` or `undefined`:

```html
<button type="button" [aria-label]="actionLabel()">{{ actionLabel() }}</button>
```

For ARIA features that expose DOM properties or directive inputs accepting structured values (such as element references), use standard property bindings instead; the accessibility best-practices guide has examples.

The same guide page also covers CSS class and style bindings, which this skill does not summarise.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/templates/binding (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. Claims match the page. Replaced a cross-reference to a nonexistent skill; the page itself covers class and style bindings, which this skill does not summarise.
