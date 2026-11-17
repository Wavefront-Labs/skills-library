---
id: computing-software.cloud-infrastructure-engineering.zot.config-file-basics
name: config-file-basics
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, config-file, hot-reload, zot-verify, json-yaml, dist-spec-version]
level: intro
status: docs-checked
description: "Zot configuration file structure, validating it with zot verify, launching with zot serve, and which settings hot-reload without a restart."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zot is configured by a JSON or YAML file. The initial file looks like this:

```json
{
    "distSpecVersion": "1.0.1",
    "storage": { "rootDirectory": "/tmp/zot" },
    "http": { "address": "127.0.0.1", "port": "8080" },
    "log": { "level": "debug" }
}
```

Other top-level keys include `extensions`, `scheduler` and more.

Workflow:
1. Check syntax: `zot verify <configfile>`
2. Launch: `zot serve <configfile>`

Verification catches operator errors and conflicts caused by release changes.

Hot reloading: Zot watches the file and applies supported changes while running. Replacement of a ConfigMap symlink is detected, so no pod restart is needed. Settings that need a restart log a warning and keep their previous values, so check the logs after every edit.

Restart-only examples from the docs: `http.shutdownTimeout`, `storage.maxRepoBytes` and `storage.gcTimeWindow`.

Note: examples in the docs use different `distSpecVersion` values (1.0.1, 1.1.0, 1.1.1); follow the example matching your release.

## Checked

2026-11-04. Read against the zot admin configuration guide (hot reloading, shutdownTimeout) and storage article (maxRepoBytes, gcTimeWindow restart notes). Every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
