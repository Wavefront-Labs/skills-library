---
id: computing-software.systems-network-administration.netbox.plugins-configuration
name: plugins-configuration
category: computing-software
field: systems-network-administration
product: netbox
tags: [plugins-setting, plugins-config, plugin-catalog]
level: practitioner
status: docs-checked
description: "List plugins in PLUGINS and pass their settings through PLUGINS_CONFIG."
sources: ["https://netboxlabs.com/docs/netbox/configuration/plugins/", "https://netboxlabs.com/docs/netbox/plugins/installation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Plugins configuration

Goal: turn plugins on and tune them.

Plugins do not take effect unless they are listed in `PLUGINS`. They run with the same access and privileges as NetBox itself, so install only from trusted sources; the maintainers give no guarantee of their integrity or security.

```
PLUGINS = ['plugin1', 'plugin2']
PLUGINS_CONFIG = {
    'plugin1': {'foo': 123, 'bar': True},
    'plugin2': {'foo': 456},
}
```

- `PLUGINS_CONFIG` is a dictionary keyed by installed plugin name; supported keys are plugin-specific. A plugin must also be in `PLUGINS` for its configuration to apply.
- `PLUGINS_CATALOG_CONFIG` (default empty) controls display under Admin > System > Plugins: names in `hidden` are omitted from the catalog.

Example:
```
PLUGINS_CATALOG_CONFIG = {'hidden': ['plugin1'], 'static': ['plugin2']}
```

For installing a plugin package into the virtualenv and for removal, follow the plugin installation and removal pages.

**Checklist**

1. Plugin installed in the venv.
2. Listed in PLUGINS.
3. Config keys checked in plugin docs.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Plugins configuration and installation pages: PLUGINS, PLUGINS_CONFIG, PLUGINS_CATALOG_CONFIG hidden/static, trust warning. Removed: Nothing.

Method: documentation only; no commands were run.
