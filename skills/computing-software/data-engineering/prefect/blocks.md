---
id: computing-software.data-engineering.prefect.blocks
name: blocks
category: computing-software
field: data-engineering
product: prefect
tags: [blocks, save, load, secretstr, block-types]
level: practitioner
status: docs-checked
description: "Prefect blocks: block types, documents and classes, save and load, SecretStr fields, CLI listing and when to use blocks instead of variables."
sources:
  - https://docs.prefect.io/v3/concepts/blocks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store typed, shareable configuration such as credentials.

Structure:
- Block type: a schema registered with the API; its slug is not configurable. Saving a document registers the type automatically.
- Block document: an instance with field values stored server-side.
- Block class: the Python class (subclass of `Block` from `prefect.blocks.core`) whose attributes load from a document. The class is not stored server-side, so import it before calling `load`.

Methods: `instance.save(name)`, `BlockClass.load(name)`, `Block.register_type_and_schema()` (rarely needed). Fields typed `SecretStr` get extra encryption and are hidden in the UI.

```python
class Cube(Block):
    edge_length_inches: float
Cube(edge_length_inches=2.25).save("rubiks-cube")
Cube.load("rubiks-cube")
```

CLI: `prefect block type ls` lists block types; `prefect block register -m prefect.blocks.notifications` registers a module's types.

Built-in slugs include `secret`, `local-file-system`, `remote-file-system`, `slack-webhook`, `ms-teams-webhook`, `custom-webhook`, `sendgrid-email`, `smb`, `twilio-sms`. Integration slugs need the package, for example `prefect-aws` provides `s3-bucket`, `ecs-task`; `prefect-gcp` provides `gcp-credentials`, `gcs-bucket`.

Use blocks for slowly changing shared configuration (credentials can be rotated without redeploying). Use parameters for values that change per run; variables are unstructured JSON.

## Checked

2026-11-08. Block type, document and class layers, SecretStr handling, slug rules, register commands, listed built-in and integration slugs and the blocks-versus-parameters guidance confirmed against the blocks page.

Method: documentation only; no commands were run.
