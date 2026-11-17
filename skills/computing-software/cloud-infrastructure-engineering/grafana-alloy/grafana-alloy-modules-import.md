---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-modules-import
name: grafana-alloy-modules-import
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [modules, importfile, importgit, importhttp, importstring, namespace, shadowing]
level: practitioner
status: docs-checked
description: "Reuse Alloy configuration with modules and the four import blocks, namespaces and shadowing of built-in namespaces, plus security cautions."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/modules.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Modules and import blocks

A module is a unit of configuration with components, custom component definitions and imports. The file you pass to `alloy run` is the main configuration. Modules add no capability; they only organise and reuse config (and suit Fleet Management distribution).

Import with:
- `import.file`: a file on disk.
- `import.git`: a file in a Git repository.
- `import.http`: an HTTP response.
- `import.string`: a string.

An imported module may contain only `declare` and `import` at the top level. The import label is the namespace: `import.file "helpers" { filename = "helpers.alloy" }` exposes `helpers.log_filter`, used as `helpers.log_filter "default" { write_to = [loki.write.default.receiver] }` and referenced as `helpers.log_filter.default.filter_input`.

## Gotchas
- Namespaces must be unique within an importing module.
- A label matching a built-in namespace (`prometheus`, `mimir`) shadows it: after `import.file "mimir"`, `mimir.rules.kubernetes` is no longer available.

## Security
Module content runs with the same privileges as the Alloy process. Protect the main config, secure Git/HTTP sources, review module content, authenticate remote fetches, restrict network access and set file permissions.

## Checked

2026-11-08. Read the Modules page in full. Confirmed: module definition and main configuration, modules adding no capability and the Fleet Management note, the four import blocks, the declare and import only restriction, namespace behaviour and uniqueness, shadowing of built-in namespaces with the mimir example, the helpers.alloy example, and the security practices.

Method: documentation only; no commands were run.
