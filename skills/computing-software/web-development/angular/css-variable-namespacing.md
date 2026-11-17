---
id: computing-software.web-development.angular.css-variable-namespacing
name: css-variable-namespacing
category: computing-software
field: web-development
product: angular
tags: [angular, css-variables, custom-properties, namespacing, app-id, styles]
level: advanced
status: docs-checked
description: "Prefix component CSS custom properties per application with provideCssVarNamespacing, opt out with --global--, and use CssVarNamespacer from TypeScript."
sources:
  - https://angular.dev/guide/components/styling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use this when your application shares a page with another application or markup you do not control, so a custom property such as `--primary-color` set on an ancestor could leak in. Angular does not namespace custom properties until asked.

Enable it by adding `provideCssVarNamespacing` to the providers; it uses `APP_ID` as the namespace:

```ts
import {APP_ID, ApplicationConfig} from '@angular/core';
import {provideCssVarNamespacing} from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [{provide: APP_ID, useValue: 'my-app'}, provideCssVarNamespacing()],
};
```

`--primary-color` then becomes `--my-app_primary-color` in declarations, `var()` references, `@property` rules and style bindings such as `[style.--primary-color]` (including those in a component's `host` object). `APP_ID` is `ng` unless set, so give each application on the page its own. To use a different namespace pass it in: `provideCssVarNamespacing('my-app_')` produces `--my-app__primary-color` (Angular appends the underscore itself).

What gets namespaced: component `styles` and `styleUrl`, `<style>` elements in templates, relative `<link rel="stylesheet">` styles, and `ViewEncapsulation.None` styles. Not namespaced: stylesheets the browser loads at runtime (global stylesheets from build config, external styles your build does not inline). Library components are namespaced too, so a library reading a theme property from a global stylesheet silently stops matching (the `var()` fallback or inherited/initial value is used, with no error). Review properties crossing between global and component styles before enabling.

Not rewritten, so namespace these yourself: static `style="--x: red"` attributes (including the `host` object's `style`), object or string style bindings and `ngStyle`, custom property names inside a binding value like `[style.border-color]="'var(--primary-color)'"`, and `Renderer2.setStyle` calls.

Opt out per name with a double-hyphen `--global--` prefix, which Angular strips to `--`:

```css
:host {
  --global--accent-color: navy;
  color: var(--global--brand-color);
}
```

A single hyphen (`--global-brand-color`) does not opt out; avoid names starting `--global-` followed by anything but a second hyphen, as a future major version plans to reject them at build time.

From TypeScript prefer `[style.--primary-color]`; otherwise pass the name you wrote in styles, including `--`, to `CssVarNamespacer`:

```ts
private readonly cssVarNamespacer = inject(CssVarNamespacer);
this.host.style.setProperty(this.cssVarNamespacer.namespace('--primary-color'), color);
```

`namespace` returns the name unchanged when no namespace is configured. Use the plain name for `--global--` properties.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/styling (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
