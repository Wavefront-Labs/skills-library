---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-datafrom-find
name: external-secrets-operator-datafrom-find
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [datafrom, find, getallsecrets, tags]
level: practitioner
status: docs-checked
description: "Pull many provider secrets into one Kubernetes Secret with dataFrom.find by name regexp, metadata tags or path."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/getallsecrets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When you cannot bundle everything into one provider secret, or do not know the names, use `dataFrom.find`. Each matched provider secret becomes one key in the Kubernetes Secret, holding its whole content.

- By name pattern: `find.name.regexp`. Secrets `/path/key1`, `key2/path` and `path/to/keyring` become keys `_path_key1`, `key2_path` and `path_to_keyring`.
- By tags: `find.tags` matches secrets that contain all the given metadata labels; at least one tag is required.
- By path: some providers support `find.path` to restrict the search to a sub-path instead of the root.

Not every provider implements find. A `decodingStrategy` can be applied only at the secret level; a JSON secret containing base64 values is not decoded inside.

Key-name conflicts: Kubernetes keys allow limited characters, so forbidden ones become `_` and `a_c` collides with `a/c`. Use a `rewrite` block, or set `dataFrom.find.conversionStrategy: Unicode`, which replaces invalid characters with `_UXXXX_` (giving `a_c` and `a_U2215_c`).

## Checked

2026-11-03. Claims were read against guides/getallsecrets.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
