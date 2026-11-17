---
id: computing-software.web-development.angular.component-selectors
name: component-selectors
category: computing-software
field: web-development
product: angular
tags: [angular, component, selector, attribute-selector, css-selector, prefix]
level: practitioner
status: docs-checked
description: "Which CSS selector forms Angular components support, how to combine them, and how to choose between element and attribute selectors and prefixes."
sources:
  - https://angular.dev/guide/components/selectors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Angular matches component selectors statically at compile time. Changing the DOM at run time, via bindings or DOM APIs, does not affect which components render. An element can match exactly one component selector (several matches is an error), and selectors are case-sensitive.

Supported selector types:
- Type selector: `profile-photo`
- Attribute selector, optionally with an exact value using `=`: `[dropzone]`, `[type="reset"]`. Other attribute operators are not supported.
- Class selector: `.menu-item`
- `:not` pseudo-class appended to another selector: `[dropzone]:not(textarea)`. No other pseudo-classes or pseudo-elements.
- Concatenated selectors: `button[type="reset"]`
- Comma-separated list: `drop-zone, [dropzone]` creates the component for any match.

Not supported: combinators (descendant, child) and namespaces.

Choosing a selector:
- Most components should use a custom element name containing a hyphen. By default Angular reports an error for a custom tag name that matches no component, catching typos.
- Use a short consistent project prefix (the CLI default is `app-`). Never use `ng` as a prefix; Angular uses it for its own APIs.
- Use an attribute selector when building on a native element, such as `button[yt-upload]`, so consumers keep all native APIs like `aria-label`.
- Angular does not report errors for attributes that match no component, so a consumer who forgets to import an attribute-selector component just gets nothing rendered.
- Attribute selectors should be lowercase dash-case, with the same prefix advice.

```ts
@Component({
  selector: 'button[yt-upload]',
  /* ... */
})
export class YouTubeUploadButton {}
```

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/selectors (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
