---
id: computing-software.web-development.storybook.args-url-and-mapping
name: args-url-and-mapping
category: computing-software
field: web-development
product: storybook
tags: [args-url, arg-mapping, argtypes-mapping, complex-args, url-args]
level: practitioner
status: docs-checked
description: "Set args through the URL query and map simple control values to complex objects like JSX with argTypes mapping."
sources:
  - https://storybook.js.org/docs/writing-stories/args
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Args in the URL and arg mapping

Goal: deep link to an args state and handle non-serializable values.

URL args:
```
?path=/story/avatar--default&args=style:rounded;size:100
```
- Pairs are `key:value` separated by `;`. Values are coerced to the argType.
- Objects and arrays work: `obj.key:val;arr[0]:one;arr[1]:two`.
- `!null` and `!undefined` set special values.
- Dates are `!date(ISO)`; colors are `!hex(value)`, `!rgba(value)`, `!hsla(value)` (no spaces or percent signs).
- Keys and values are limited to alphanumerics, spaces, underscores and dashes (XSS safeguard); other values are removed from the URL.
- URL args extend and override the story args.

Mapping complex values (JSX cannot be serialized to the manager or URL):

```tsx
argTypes: {
  icon: {
    options: ['none', 'star'],
    mapping: { none: null, star: <StarIcon /> },
    control: { type: 'select' },
  },
},
```
`mapping` keys match arg values, not option indexes, and need not be exhaustive: an unmapped value is used as is. Pair with `control.labels` for friendly option labels.

Verify: opening the URL with `args=size:100` shows the control at 100.

## Checked
Date: 2026-11-04. Read the Args page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: URL format, special values, date and color syntax, XSS restriction, mapping behavior, `control.labels`.
Method: documentation only; no commands were run.
