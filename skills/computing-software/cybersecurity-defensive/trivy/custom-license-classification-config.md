---
id: computing-software.cybersecurity-defensive.trivy.custom-license-classification-config
name: custom-license-classification-config
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [custom-classification, generate-default-config, trivy-yaml, text-licenses, forbidden, license-regex]
level: advanced
status: docs-checked
description: "Generate the default Trivy config with --generate-default-config and move license IDs between classification lists, including text:// entries and regular expressions."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/license/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can customise the license classification by generating the default config:

```shell
trivy image --generate-default-config
```

This writes `trivy.yaml` containing a `license` section with lists named `forbidden`, `restricted`, `reciprocal`, `notice`, `unencumbered` and `permissive`. By default `forbidden` holds `AGPL-3.0`, `restricted` includes GPL and LGPL variants such as `GPL-2.0` and `LGPL-2.1`, `reciprocal` includes `MPL-2.0` and `EPL-2.0`, `notice` includes `Apache-2.0`, `MIT` and `BSD-3-Clause`, `unencumbered` has `CC0-1.0`, `Unlicense` and `0BSD`, and `permissive` is empty.

The page's example: to forbid only AGPL-3.0, leave it under `forbidden` and move the others to another classification.

```yaml
license:
  forbidden:
    - AGPL-3.0
```

Text licenses: by default Trivy categorises a license as UNKNOWN if it cannot determine the license name from the license text. To classify a text license, add it with the `text://` prefix:

```yaml
license:
  forbidden:
    - "text://Text of Apache Software Foundation License"
```

Since a text license can be large, regular expressions are supported:

```yaml
license:
  forbidden:
    - "text://.* Apache Software .*"
```

A `regex` only applies to text licenses. It cannot be used to configure license IDs.

## Checked

2026-11-03. Read and confirmed against the License Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
