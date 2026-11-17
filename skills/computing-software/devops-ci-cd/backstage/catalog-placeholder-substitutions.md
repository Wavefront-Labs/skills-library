---
id: computing-software.devops-ci-cd.backstage.catalog-placeholder-substitutions
name: catalog-placeholder-substitutions
category: computing-software
field: devops-ci-cd
product: backstage
tags: [placeholders, text-json-yaml, include-files, backstage]
level: practitioner
status: docs-checked
description: "Embed external files into descriptors with the $text, $json and $yaml substitutions."
sources:
  - https://backstage.io/docs/features/software-catalog/descriptor-format
  - https://backstage.io/docs/features/software-catalog/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Descriptor files can pull content from other files using substitution keys. A substitution replaces the object that contains it.

- `$text` reads the referenced file as plain text and embeds the string.
- `$json` reads it as JSON and embeds the parsed value.
- `$yaml` reads it as YAML and embeds the parsed value.

```yaml
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: petstore
spec:
  type: openapi
  lifecycle: production
  owner: petstore@example.com
  definition:
    $text: ./petstore.oas.yaml
```

The reference can be a file path or a URL. To read from targets outside the normal integration points such as github.com you must allow them in the `backend.reading.allow` list, optionally restricted by `paths`:

```yaml
backend:
  reading:
    allow:
      - host: example.com
      - host: '*.examples.org'
      - host: example.net
        paths: ['/api/']
```

Substitutions are not available for `file` location types.

## Checked

2026-11-03. Confirmed on the descriptor format page: substitutions `$text`, `$json` and `$yaml` and their behaviour, the `$text` example with a URL, and the `backend.reading.allow` list requirement. On the catalog configuration page: `file` locations do not support `$text`, `$json` or `$yaml`. Removed: versioning and typo-detection advice, and the claim that a relative path is the reference form, which are not stated.

Method: documentation only; no commands were run.
