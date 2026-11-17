---
id: computing-software.web-development.mkdocs.plugins-config
name: plugins-config
category: computing-software
field: web-development
product: mkdocs
tags: [plugins, plugin-options, search-plugin, pip-install]
level: practitioner
status: docs-checked
description: "Install and configure MkDocs plugins: pip install, the plugins list, options, the search default that vanishes when you set plugins, and disabling all."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install the package first (bundled plugins already came with MkDocs):

```bash
pip install mkdocs-foo-plugin
```

Installing a plugin runs the author's code; there is no sandboxing. Then enable it:

```yaml
plugins:
  - search
  - your_other_plugin:
      option1: value
      option2: other value
```

Gotchas:
- Default is `['search']`. Once you define `plugins`, all defaults are ignored: re-add `search` if you want it.
- Disable everything, defaults included: `plugins: []`.
- Alternate dict syntax (needed for inheritance overrides) requires an empty value for plugins without options:

```yaml
plugins:
  search: {}
  your_other_plugin:
    option1: value
```

Use the plugin's documented name; a listed plugin must already be installed.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (plugins) and the Plugins guide: `pip install`, the no-sandboxing warning, bundled plugins installed with MkDocs, default `['search']`, `plugins: []`, the dict syntax, and that a listed plugin must already be installed. Removed: a generic verify line.

Method: documentation only; no commands were run.
