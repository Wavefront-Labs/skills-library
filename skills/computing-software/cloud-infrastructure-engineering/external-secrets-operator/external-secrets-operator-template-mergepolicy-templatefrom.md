---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-template-mergepolicy-templatefrom
name: external-secrets-operator-template-mergepolicy-templatefrom
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [templating, mergepolicy, templatefrom, literal]
level: advanced
status: docs-checked
description: "Keep provider keys alongside templated ones with mergePolicy and load templates from ConfigMaps, Secrets or literals with templateFrom."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default templating keeps only the templated output and drops the keys fetched through `data` and `dataFrom`. `mergePolicy` accepts `Replace` (the default) and `Merge`; with `Merge` the `data` and `dataFrom` keys are also embedded in the templated secret, with lower priority than the template outcome.

`templateFrom` pulls templates from existing `ConfigMap` or `Secret` objects instead of defining them inline. It can also:
- choose where output goes: the Secret's `Data`, `Annotations` or `Labels` (the `target`);
- render as `Values` or `KeysAndValues` through `templateAs`, so one template can produce multiple keys;
- take `literal` blocks, which are rendered as a full `key: value` pair, unlike `template.data` where only the value is templated.

## Checked

2026-11-03. Claims were read against guides/templating.md in the external-secrets docs source. Removed: an unsupported reuse and access-control tip.

Method: documentation only; no commands were run.
