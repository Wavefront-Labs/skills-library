---
id: computing-software.web-development.jekyll.theme-gem-config-and-dependencies
name: theme-gem-config-and-dependencies
category: computing-software
field: web-development
product: jekyll
tags: [theme-config, runtime-dependencies, ignore-theme-config, theme-preconfiguration]
level: sme
status: docs-checked
description: "Understand theme-gem runtime dependencies (3.5.0+) and a bundled _config.yml (4.0+): merge rules, restrictions, silent ignores and ignore_theme_config."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/themes.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/config_options/global.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dependencies (3.5.0+): Jekyll automatically requires all whitelisted `runtime_dependencies` of the theme gem even if they are not under `plugins` in the site config, so users need not track the plugins a theme needs. Whitelisting matters only with `--safe`.

Bundled config (4.0+): Jekyll reads a `_config.yml` at the root of the theme gem and merges it into the site configuration. Restrictions:

- Jekyll's default settings cannot be overridden by the theme config.
- The theme config file cannot be a symlink, regardless of safe mode.
- It must be key-value pairs. An empty file, a file that only lists items under a key, or a plain string is silently ignored, with no warning or log output.
- The user can override any setting the theme config defines.

The restrictions ensure a theme config cannot affect the build in a worrying way. Plugins the theme needs must be listed manually by the user or provided via the theme's gemspec. This lets a theme work with its own config variables out of the box.

If a bundled theme config breaks the merged configuration, opt out entirely (4.1.0+):

```yaml
ignore_theme_config: true
```

## Checked

2026-11-04. Confirmed against the Jekyll Themes page (3.5.0 dependencies, 4.0 pre-configuring) and the global configuration data (ignore_theme_config, 4.1.0). Nothing removed.

Method: documentation only; no commands were run.
