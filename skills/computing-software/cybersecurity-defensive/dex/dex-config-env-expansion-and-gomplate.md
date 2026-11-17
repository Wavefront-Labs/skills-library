---
id: computing-software.cybersecurity-defensive.dex.dex-config-env-expansion-and-gomplate
name: dex-config-env-expansion-and-gomplate
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [configuration, environment, gomplate, secrets]
level: practitioner
status: docs-checked
description: "Inject secrets into the Dex config with $VAR expansion or gomplate templates, and know when the container entrypoint skips templating."
sources:
  - https://dexidp.io/docs/getting-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex supports two ways to pull values from the environment into its config.

1. Built-in expansion: Dex expands `$VAR` and `${VAR}` references in YAML values before parsing the file, for example connector credentials. Set `DEX_EXPAND_ENV=false` to turn this off.

2. Gomplate: the default entrypoint of the distributed container images runs gomplate over configuration files ending in `.tpl`, `.tmpl` or `.yaml` that are passed as arguments. This lets you template any field:

```yaml
secret: "{{ .Env.MY_SECRET_ENV }}"
```

Gotcha: gomplate preprocessing comes from the image entrypoint, not from Dex. If a deployment overrides the container command and runs the binary directly, for example `dex serve /etc/dex/config.yaml`, the entrypoint is skipped and gomplate templates are not rendered.

## Checked

2026-11-08: Read the Dex Getting Started page in full. Confirmed built-in $VAR and ${VAR} expansion, DEX_EXPAND_ENV=false, gomplate preprocessing by the container entrypoint for .tpl, .tmpl and .yaml files, the template example and the entrypoint-override caveat. Removed the literal-text, LDAP bindPW and run-check claims, which that page does not state.
Method: documentation only; no commands were run.
