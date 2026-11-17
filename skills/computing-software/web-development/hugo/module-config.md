---
id: computing-software.web-development.hugo.module-config
name: module-config
category: computing-software
field: web-development
product: hugo
tags: [module-config, imports, mounts, replacements, proxy]
level: advanced
status: docs-checked
description: "Configure the module section: proxy and private settings, replacements, version requirements, imports options, and mounts with files and sites."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/module.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defaults:

```toml
[module]
noProxy = 'none'
noVendor = ''
private = '*.*'
proxy = 'direct'
vendorClosest = false
workspace = 'off'
```

- `proxy`: `direct` uses methods like `git clone`.
- `replacements`: comma-separated `module -> directory` mappings for local development; honoured only in the project configuration.
- `workspace`: Go workspace file; needs Go 1.18 or later.
- Hugo version: `min` and `max` under `module.hugoVersion` warn users of an incompatible Hugo version. The `extended` check is deprecated and disabled in v0.153.2 and later.
- Env vars: `HUGO_MODULE_PROXY`, `HUGO_MODULE_REPLACEMENTS`, `HUGO_MODULE_WORKSPACE`.

Imports:

```toml
[[module.imports]]
path = 'my-shortcodes'
disable = false
```

Other import options: `ignoreConfig`, `ignoreImports`, `noMounts`, `noVendor` (main project only), `usePackageJSON` (`auto`, `always`, `never`) and `version`.

Mounts: a mount in project configuration removes the default mount for that component; in a module it removes all of that module's defaults. Add a default back explicitly. Do not combine mounts with legacy settings like `contentDir`.

```toml
[[module.mounts]]
source = 'content'
target = 'content'
files = ['! docs/*']
```

`target` must begin with a component directory. `disableWatch` stops watching; `files` replaces deprecated `excludeFiles` and `includeFiles`.

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure modules: the defaults, `proxy`, `replacements` (project configuration only), `workspace` and the Go 1.18 requirement, the Hugo version warning keys, the three environment variables, the import options and `usePackageJSON` values, the mount replacement rules, the legacy-setting warning, `target` component rule, and `files` replacing `excludeFiles` and `includeFiles`. Clarified that the version keys live under `module.hugoVersion`.

Method: documentation only; no commands were run.
