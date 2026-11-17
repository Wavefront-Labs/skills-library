---
id: computing-software.ux-hci-design.design-systems.style-dictionary-token-pipeline
name: style-dictionary-token-pipeline
category: computing-software
field: ux-hci-design
product: design-systems
tags: [style-dictionary, token-transforms]
level: practitioner
status: draft
description: "Use Style Dictionary to build CSS variables, iOS and Android outputs from a single token source."
sources:
  - https://styledictionary.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Style Dictionary
- Config lists source files, platforms, transforms (e.g. `name/kebab`, `color/css`), formats (`css/variables`) and destinations.
```js
export default { source:['tokens/**/*.json'],
  platforms:{ css:{ transformGroup:'css', buildPath:'dist/', files:[{destination:'tokens.css',format:'css/variables'}] } } };
```
- Run `npx style-dictionary build`. Check docs for the v4 config format differences (ESM config, `$value` support).
- Version tokens with the package; publish to npm.

## Verify
- [ ] Generated CSS variables used by one component render correctly in light and dark themes.
