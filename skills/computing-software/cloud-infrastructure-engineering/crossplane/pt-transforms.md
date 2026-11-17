---
id: computing-software.cloud-infrastructure-engineering.crossplane.pt-transforms
name: pt-transforms
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function-patch-and-transform, transform, map, match, string]
level: practitioner
status: docs-checked
description: "Modify patch values with convert, map, match, math and string transforms."
sources:
  - https://docs.crossplane.io/latest/guides/function-patch-and-transform/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add `transforms` (each with `type` plus a same-named block) to a patch.

- `map`: exact lookup; an unmatched value is an error.

```yaml
transforms:
- type: map
  map:
    us: us-east-2
    eu: eu-north-1
```

- `match`: `patterns` of `type: literal` (with `literal`) or `regexp`, each with `result`. First match wins. Unmatched: `fallbackTo: Value` with `fallbackValue`, or `fallbackTo: Input`.
- `math`: integers only. `type: multiply` (`multiply: 2`), `clampMin`, `clampMax`.
- `convert`: `toType` is bool, float64, int, int64, string, object or array. Strings `1 t T TRUE True true` convert to true. Add `format: quantity` for float64 suffixes like `Mi`; add `format: json` for object and array.
- `string`: `type` is `Format` (`fmt`, Go formatting), `Convert` (`ToUpper`, `ToLower`, `ToBase64`, `FromBase64`, `ToJson`, `ToSha1`, `ToSha256`, `ToSha512`, `ToAdler32`), `Join` (`join.separator`, arrays only), `Regexp` (optional `group`), `TrimPrefix` or `TrimSuffix` (field `trim`), or `Replace` (`replace.search` and `replace.replace`).

To build a tag key with a custom name, apply a `Format` string transform and then `convert` to `object` with `format: json`.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Function Patch and Transform guide, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the claim that transforms run in listed order.

Method: documentation only; no commands were run.
