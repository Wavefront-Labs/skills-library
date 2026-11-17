---
id: computing-software.web-development.mkdocs.plugin-write-basics
name: plugin-write-basics
category: computing-software
field: web-development
product: mkdocs
tags: [base-plugin, config-scheme, entry-points, plugin-development]
level: advanced
status: docs-checked
description: "Write a MkDocs plugin: BasePlugin subclass, typed config schema, on_event methods, errors and logging, and the mkdocs.plugins entry point."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A plugin is a `mkdocs.plugins.BasePlugin` subclass plus a setuptools entry point. Define options with a Config subclass (1.4+):

```python
class MyPluginConfig(mkdocs.config.base.Config):
    foo = mkdocs.config.config_options.Type(str, default='a default value')
    baz = mkdocs.config.config_options.Type(bool, default=True)

class MyPlugin(mkdocs.plugins.BasePlugin[MyPluginConfig]):
    def on_pre_build(self, config, **kwargs):
        if self.config.baz: ...
```

Invalid or undeclared user options raise `ValidationError`. Event handlers are `on_<event>` methods; return the (modified) positional argument, or None to keep it, and always accept `**kwargs`.

Errors: raise `mkdocs.exceptions.PluginError("message")` for a clean abort. Logging: use a logger under `mkdocs.plugins.` (or `get_plugin_logger()` in 1.5+) so MkDocs formatting and the `--verbose`/`--debug` flags apply.

Entry point:

```python
entry_points={'mkdocs.plugins': ['pluginname = path.to.some_plugin:SomePluginClass']}
```

Registering does not activate it; users add it to `plugins`. Publish to PyPI and the catalog; pick a unique entry-point name.

## Checked

2026-11-04. Confirmed against the MkDocs Plugins guide (Developing Plugins: BasePlugin, config schema as a `Config` subclass new in 1.4, `ValidationError`, `on_<event_name>` return rules and `**kwargs`, Handling Errors with `PluginError`, Logging in plugins, Entry Point, Publishing a Plugin). Removed the Verify line and the claim that `--strict` depends on the logger namespace, which the page does not state.
Method: documentation only; no commands were run.
