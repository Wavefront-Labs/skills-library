---
id: computing-software.ux-hci-design.design-systems.design-token-structure-dtcg
name: design-token-structure-dtcg
category: computing-software
field: ux-hci-design
product: design-systems
tags: [design-tokens-format, dtcg-json, ds-tokens]
level: practitioner
status: draft
description: "Define tokens in DTCG JSON with $value, $type and groups, and use aliases for semantic references."
sources:
  - https://www.designtokens.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DTCG token file (draft community spec)
```json
{ "color": {
    "blue": { "500": { "$type": "color", "$value": "#1a56db" } },
    "action": { "primary": { "$type": "color", "$value": "{color.blue.500}" } } } }
```
- `$value`, `$type`, `$description`; groups nest; aliases use `{path.to.token}`.
- Check the current spec version: the format is a community-group draft and details (e.g. colour value shape) have evolved.

## Verify
- [ ] Build tooling (Style Dictionary) resolves aliases without errors.
