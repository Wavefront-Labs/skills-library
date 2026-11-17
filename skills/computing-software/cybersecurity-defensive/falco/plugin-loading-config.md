---
id: computing-software.cybersecurity-defensive.falco.plugin-loading-config
name: plugin-loading-config
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [plugins-config, load-plugins, library-path, init-config, required-plugin-versions]
level: practitioner
status: docs-checked
description: "Configure plugins in falco.yaml with plugins and load_plugins, bind rules to a source, and pin versions with required_plugin_versions."
sources:
  - https://falco.org/docs/concepts/plugins/usage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Define the plugins Falco can load under `plugins`, then choose which to load with `load_plugins`:

```yaml
plugins:
  - name: cloudtrail
    library_path: libcloudtrail.so
    init_config: ""
    open_params: ""
  - name: json
    library_path: libjson.so
    init_config: ""
load_plugins: [cloudtrail, json]
```

The loader uses dlopen and dlsym (LoadLibrary on Windows) and checks that the plugin exports the expected symbols, has a compatible API version, that only one event-sourcing plugin loads per event source, and that fields from sourcing and extraction plugins for the same source have unique names.

A rule binds to an event source with its `source` key. A rule with `source: aws_cloudtrail` is evaluated for events from the CloudTrail plugin, and an extractor listing that source can supply fields in the rule's condition, exceptions or output. Falco compiles rules, macros and lists selectively based on loaded plugin sources. Macros have no `source` key, so mind fields that exist only for some sources.

Rule files declare compatible plugin versions:

```yaml
- required_plugin_versions:
  - name: <plugin_name>
    version: x.y.z
```

The field is optional; if absent, no plugin compatibility checks are made. If a loaded plugin has a matching name, its version must be semver-compatible with `version`. Entries across files merge, and duplicates must all be compatible.

`load_plugins` is optional and controls which of the defined plugins are loaded at start.

Gotcha: if a plugin with event sourcing capability is loaded, the only events processed are from that plugin and syscall events are disabled.

## Checked

2026-11-08. Read the cited plugin usage page in full and corrected details to match it, including the required_plugin_versions behavior.

Method: documentation only; no commands were run.
