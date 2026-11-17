---
id: computing-software.ux-hci-design.design-systems.component-api-design
name: component-api-design
category: computing-software
field: ux-hci-design
product: design-systems
tags: [component-api, variant-props, ds-components]
level: advanced
status: draft
description: "Design small, consistent component APIs with variants, sizes, composition slots and sensible defaults."
sources:
  - https://www.w3.org/WAI/ARIA/apg/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Component API
- Prefer composition (slots/children) over many boolean props.
- Standardise prop names across components (`size`, `variant`, `disabled`, `onChange`).
- Variants over one-off styles; enumerate states: default, hover, focus, active, disabled, loading, error.
- Spread native attributes to the root element; forward refs.
- Accessible by default (roles, focus management) and documented keyboard behaviour.

## Verify
- [ ] Two teams can build different layouts from the same components without forking them.
