---
id: computing-software.web-development.htmx.htmx-attribute-inheritance
name: htmx-attribute-inheritance
category: computing-software
field: web-development
product: htmx
tags: [htmx, inheritance, hx-disinherit, hx-inherit, unset, disableinheritance]
level: practitioner
status: docs-checked
description: "How htmx attribute inheritance works: hoisting to parents, unset, hx-disinherit, and explicit hx-inherit with htmx.config.disableInheritance."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-disinherit.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-inherit.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove duplication by putting shared attributes on a parent, and undo it precisely where needed.

Most htmx attributes are inherited: they apply to the element they are on and its children (documented examples: `hx-target`, `hx-confirm`, `hx-boost`). Check an attribute's own reference page for whether it is inherited.

```html
<div hx-confirm="Are you sure?">
  <button hx-delete="/account">Delete My Account</button>
  <button hx-put="/account">Update My Account</button>
  <button hx-confirm="unset" hx-get="/">Cancel</button>   <!-- no confirm -->
</div>
```
`unset` as an attribute value cancels an inherited value for that element (shown in the docs for `hx-confirm`; the `hx-disinherit` page shows `hx-boost="unset"`).

`hx-disinherit` on a parent stops children inheriting:
- `hx-disinherit="*"` - all attribute inheritance for this element is disabled.
- `hx-disinherit="hx-select hx-get hx-target"` - only the listed attributes.
```html
<div hx-boost="true" hx-select="#content" hx-target="#content" hx-disinherit="hx-target">
  <button hx-get="/test"></button> <!-- inherits hx-select, not hx-target -->
</div>
```
Disinheritance applies at the direct parent even if that parent does not itself define the attribute: in the reference example a grandparent's `hx-select` is not inherited through a parent that has `hx-disinherit="hx-select"`.

Opt-in mode: set `htmx.config.disableInheritance` to `true` (the config can be set with the `htmx-config` meta tag) so inheritance is no longer the default, then enable it with `hx-inherit`: `hx-inherit="*"` enables all, or give a space-separated list.
```html
<div hx-target="#tab-container" hx-inherit="hx-target">
  <a hx-boost="true" href="/tab1">Tab 1</a>
</div>
```

## Checked

2026-11-07. Confirmed on docs.md (Attribute Inheritance, hx-confirm `unset` example, `htmx.config.disableInheritance`, `htmx-config` meta tag), hx-disinherit.md (`*`, list form, direct-parent example, `hx-boost="unset"`) and hx-inherit.md.
Removed: the lists of non-inherited attributes and of `hx-ext`/`hx-request` merging, the longer inherited list (swap, select, headers, vals, sync, indicator), `unset` for `hx-select`, the extended-selector gotcha, and the invented Verify step; none appear on the cited pages.
Method: documentation only; no commands were run.
