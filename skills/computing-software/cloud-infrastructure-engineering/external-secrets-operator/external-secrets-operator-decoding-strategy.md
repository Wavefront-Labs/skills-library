---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-decoding-strategy
name: external-secrets-operator-decoding-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [decodingstrategy, base64, base64url, auto]
level: practitioner
status: docs-checked
description: "Set decodingStrategy None, Base64, Base64URL or Auto on remoteRef, extract or find, and know the Auto limitation."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/decoding-strategy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`decodingStrategy` goes under `spec.data[].remoteRef`, `spec.dataFrom[].extract` or `spec.dataFrom[].find` and applies only to that operation.
- `None` (default): no decoding.
- `Base64` / `Base64URL`: decode with the matching RFC 4648 method; failure is an error.
- `Auto`: try Base64 or Base64URL, and on failure silently fall back to None.

```yaml
dataFrom:
- extract:
    key: my-secret
    decodingStrategy: Auto
```

With `{"name":"Gustavo","surname":"Fring","address":"aGFwcHkgc3RyZWV0"}` only `address` is decoded to `happy street`; the others are stored as-is.

Limitation: there is no reliable way to detect base64, so `Auto` may decode plain values that happen to be valid base64, such as alphanumeric strings of length divisible by four (`1234`, `happy/street`), yielding gibberish. If wrong values appear, switch to `None` to investigate.

## Checked

2026-11-03. Claims were read against guides/decoding-strategy.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
