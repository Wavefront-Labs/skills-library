---
id: computing-software.cybersecurity-defensive.falco.rules-file-versioning
name: rules-file-versioning
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [required-engine-version, engine-version, rules-versioning, plugin-versions, falco-engine]
level: intro
status: docs-checked
description: "Declare required_engine_version and required_plugin_versions in a rules file and know what happens on a mismatch."
sources:
  - https://falco.org/docs/concepts/rules/versioning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two optional top-level elements in a rules file track compatibility:
- `required_engine_version`: compatibility with the Falco engine version.
- `required_plugin_versions`: compatibility with plugin versions.

The `falco` executable and the `falco_engine` C++ object report a version number. The initial version is 2, meaning earlier versions were 1. It is incremented on incompatible changes to the rules file format or when new fields, events or syntax elements are added.

```yaml
# This rules file requires a falco with falco engine version 7.
- required_engine_version: 7
```

The value is the minimum engine version needed to read the file. If omitted, no version check is performed. If the value is greater than the Falco engine version, the rules file is loaded and an error is returned.

`required_plugin_versions` tracks compatibility with plugin versions; its entry syntax is described on the plugins documentation, not on the versioning page. The engine version your installation supports is shown by `falco --version`.

The official rules distributed by the Falco organization are versioned and have a changelog on the falcosecurity/rules releases page.

Gotcha: a too-new rules file is still loaded when its required version exceeds the engine version, and an error is returned, so check the error output after upgrading rules without upgrading Falco.

## Checked

2026-11-08. Read the cited versioning page in full. Moved the required_plugin_versions syntax claim out, since that syntax is documented on the plugins usage page, not this one.

Method: documentation only; no commands were run.
