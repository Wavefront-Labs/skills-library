---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-template-values-decoding
name: external-secrets-operator-template-values-decoding
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [templating, valuesdecodingstrategy, base64, binary]
level: sme
status: docs-checked
description: "Decode templated values safely with templateFrom valuesDecodingStrategy instead of b64dec to preserve binary data."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When provider JSON carries base64 values (for example `{"cert": "LS0t...", "description": ...}` matched by `dataFrom.find`), a literal template such as

```yaml
templateFrom:
- literal: |-
    {{- range $key, $val := . }}
    {{- $json := $val | fromJson }}
    {{ $key }}: {{ $json.cert }}
    {{- end }}
```

stores the base64 text unchanged. Add `valuesDecodingStrategy: Base64` to that `templateFrom` entry and ESO decodes the rendered values and writes the decoded bytes. Only rendered values are decoded, never keys. Options are `None` (values not encoded) and `Base64`, `Base64URL` or `Auto`.

This is safer for binary data than `{{ $json.cert | b64dec }}` inside the template, because `b64dec` injects raw bytes into the intermediate rendered YAML.

## Checked

2026-11-03. Claims were read against guides/templating.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
