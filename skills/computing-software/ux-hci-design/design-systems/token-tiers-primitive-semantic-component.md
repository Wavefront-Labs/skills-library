---
id: computing-software.ux-hci-design.design-systems.token-tiers-primitive-semantic-component
name: token-tiers-primitive-semantic-component
category: computing-software
field: ux-hci-design
product: design-systems
tags: [token-tiers, semantic-tokens]
level: practitioner
status: draft
description: "Separate raw values, role-based semantic tokens and component tokens so themes can remap semantics."
sources:
  - https://www.designtokens.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Token tiers
1. **Primitive/reference**: raw palette and scale (`blue-500`, `space-4`).
2. **Semantic/system**: purpose (`color-action-primary`, `color-text-muted`) pointing to primitives; themes remap here.
3. **Component**: scoped (`button-primary-bg`) pointing to semantic tokens.
- Name by role, not appearance (`danger` not `red`).
- Consumers should use semantic or component tokens, never primitives.

## Verify
- [ ] Switching theme changes only semantic mappings; components untouched.
