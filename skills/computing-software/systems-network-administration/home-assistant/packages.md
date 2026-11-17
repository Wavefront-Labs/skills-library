---
id: computing-software.systems-network-administration.home-assistant.packages
name: packages
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [packages, include-dir-named, merge]
level: advanced
status: docs-checked
description: "Bundle multi-integration configuration into Home Assistant packages, include them from a packages folder, and obey the merge rules for entity keys."
sources:
  - https://www.home-assistant.io/docs/configuration/packages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: group everything for one system (switches, lights, automations) into one package.

Packages live under `homeassistant:` in configuration.yaml. A package name has no spaces and is all lowercase.

Inline:

```yaml
homeassistant:
  packages:
    pack_1:
      switch:
        - platform: rest
          ...
      light:
        - platform: rpi
          ...
```

From a file:

```yaml
homeassistant:
  packages:
    pack_1: !include my_package.yaml
```

my_package.yaml contains top-level configuration (`switch:`, `light:` and so on).

A packages folder:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

With `!include_dir_named` the filename is the package name, so filenames must be unique across subfolders. `!include_dir_merge_named` is the alternative; it differs in how file contents are placed under the package name.

Merge rules:

1. Platform-based integrations (`light`, `switch`) always merge.
2. Integrations keyed by entity ID (`{key: config}`) need unique keys across packages and the main file. If the main file has `input_boolean: my_input:`, a package cannot reuse `my_input`.
3. Other integrations merge only if their non-list keys are defined once.

Platform entries inside packages must use the style where platforms are grouped under the integration name.

## Checked

2026-11-04. Confirmed against the Packages page. Nothing removed.

Method: documentation only; no commands were run.
