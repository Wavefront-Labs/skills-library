---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-configuration-extension
name: woodpecker-configuration-extension
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [config-extension, pipeline-generation, http-endpoint]
level: sme
status: docs-checked
description: "Modify or generate Woodpecker pipeline configs at runtime with a configuration extension."
sources:
  - https://woodpecker-ci.org/docs/usage/extensions/configuration-extension
  - https://woodpecker-ci.org/docs/administration/configuration/server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker configuration extension

A configuration extension is an HTTP endpoint that modifies or generates pipeline configuration. Set it per repository (settings, extensions tab) or globally:

```ini
WOODPECKER_CONFIG_EXTENSION_ENDPOINT=https://example.com/ciconfig
```

Uses: Go templating, converting custom attributes, adding default steps, converting from other formats (GitLab CI, Starlark, Jsonnet) and centralizing configuration for many repositories.

Flow: when a pipeline triggers, Woodpecker fetches the repository config, then POSTs JSON containing `repo`, `pipeline`, optional `netrc`, `restart` and the `configuration` list (file `name` and `data`). The extension responds with:

```json
{ "configs": [ { "name": "central-override", "data": "steps:\n ..." } ] }
```

Respond `204 No Content` to keep the existing files.

Options:

- The global endpoint is called before the repository one, unless the repository enabled the exclusive setting.
- Exclusive mode (`WOODPECKER_CONFIG_EXTENSION_EXCLUSIVE`, default false) skips the forge entirely, and requests carry no configuration files.
- `netrc` is sent only if `WOODPECKER_CONFIG_EXTENSION_NETRC` is true (default false) or the repository checks "Send netrc credentials".

Secure the endpoint; Woodpecker signs requests (see the extension security skill).

## Checked

2026-11-08. Read the Woodpecker Configuration extension page in full and the `CONFIG_EXTENSION_*` entries of the server configuration page. All claims were confirmed; nothing was removed.

Method: documentation only; no commands were run.
