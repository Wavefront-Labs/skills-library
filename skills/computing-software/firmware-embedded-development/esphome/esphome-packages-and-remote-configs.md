---
id: computing-software.firmware-embedded-development.esphome.esphome-packages-and-remote-configs
name: esphome-packages-and-remote-configs
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, packages, include, git-packages, merge, github, modular-config, substitutions]
level: advanced
status: docs-checked
description: "Modularize ESPHome configs with packages: local files and Git repositories, how merging works, shorthand URLs and per-package files, path and vars options."
sources: ["https://esphome.io/components/packages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome packages and remote configs

For many devices, move common configuration (Wi-Fi, API, logger) into shared files and keep only unique parts in each device's YAML. `packages:` brings these in using `!include`, merging them non-destructively with your main configuration so you can override parts of a package. Substitutions in your main configuration override same-named substitutions in a package.

Merge rules:
- Dictionaries merge key by key.
- Lists of components merge by component ID when IDs are specified.
- Other lists merge by concatenation.
- All other values are replaced with the later value.

The `packages:` value can be a list of includes or a mapping of keys to package references; mapping keys are for reference only. Example from the docs: a `device_base.yaml` defines `esphome`, `esp32`, `logger` and `api`, and the main file adds `api:` actions which merge into it.

Remote packages come from Git. Options per package:
- `url` (required) of the repository.
- `path`: base common path of included files.
- `username`, `password` when authentication is required.
- `files`: a list of paths, or objects with `path` and `vars`.

Shorthand URL schemes are supported for `codeberg://`, `github://` and `gitlab://`. Remote packages cannot contain `secret` lookups; use substitutions with an optional default in the packaged YAML, and have the local device file set the value from its own secrets.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/packages/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
