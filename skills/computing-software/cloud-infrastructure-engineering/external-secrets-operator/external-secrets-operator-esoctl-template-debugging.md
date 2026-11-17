---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-esoctl-template-debugging
name: external-secrets-operator-esoctl-template-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [esoctl, templates, debugging, pushsecret]
level: practitioner
status: docs-checked
description: "Render and debug ExternalSecret and PushSecret templates offline with esoctl template, and scaffold new generators with bootstrap generator."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/using-esoctl-tool.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`esoctl` lives under `cmd/esoctl`; run `make build` there to get `bin/esoctl`.

```bash
bin/esoctl template --source-templated-object template-test/push-secret.yaml \
  --source-secret-data-file template-test/secret.yaml
```

Put the PushSecret or ExternalSecret in one file and the Secret data it uses in another. The output shows the rendered Secret (base64 values) so you can decode and check them. Extra flags load templates from a ConfigMap or Secret: `--template-from-config-map` and `--template-from-secret`.

`esoctl bootstrap generator --name GeneratorName --description "..." --package generatorname` scaffolds a new generator for contributors: the CRD type, implementation and test, go.mod, register file, cluster generator types and resolver. `name` must be PascalCase; `package` is optional, snake_case, defaulting to lowercase name.

## Checked

2026-11-03. Claims were read against guides/using-esoctl-tool.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
