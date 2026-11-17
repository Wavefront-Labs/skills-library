---
id: computing-software.rpa-and-low-code.uipath.uipath-credential-stores
name: uipath-credential-stores
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-credential-stores]
level: advanced
status: draft
description: "Keep secrets out of Orchestrator where policy requires."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use external credential stores
**Goal:** Keep secrets out of Orchestrator where policy requires.

- Orchestrator supports credential stores such as CyberArk, Azure Key Vault and HashiCorp Vault plugins (confirm the list in docs).
- Robots retrieve credentials at runtime; rotate in the vault.
- Restrict who can view asset values.

## Gotchas
- Granting Assets View to developers exposes secrets of the folder.

## Self-check
Rotated secret works on the next run without a code change.
