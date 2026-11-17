---
id: computing-software.web-development.hugo.config-files-and-merge
name: config-files-and-merge
category: computing-software
field: web-development
product: hugo
tags: [configuration, hugo-toml, config-directory, environments, merge-strategy]
level: practitioner
status: docs-checked
description: "Hugo configuration files, the config directory by environment, --config merging, theme merge strategies with _merge, HUGO_ environment variables and hugo config."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configuration is optional. File names in precedence order: `hugo.toml`, `hugo.yaml`, `hugo.json`, in the project root.

```sh
hugo build --config a.toml,b.yaml,c.json
```

`--config` merges files left to right; the last file wins on conflicts.

A `config` directory splits settings by environment, category and language. Hugo loads `_default` first, then the current environment's directory, which overrides conflicting keys.

```sh
hugo build --environment staging
```

Category names may be omitted in component files, but are required for slice-typed keys such as `cascade` and `permalinks`.

Theme and module settings merge into the project, project settings win, and only maps (not slices) merge. Control it with `_merge`: `none`, `shallow` or `deep`, at any nesting level or at the root.

```toml
[markup.goldmark.extensions.typographer]
_merge = 'deep'
```

Most categories default to `none` to protect against third-party themes. Setting `shallow` or `deep` on sensitive keys like `markup` or `security` removes that protection.

Environment variables start with `HUGO_` and override files; custom parameters use `HUGO_PARAMS_`.

```sh
export HUGO_BASEURL=https://example.org/
hugo config
hugo config mounts
```

## Checked

2026-11-04: file names and precedence, --config left-to-right merge, config directory and environment loading, omitted category names, _merge values and root-level use, security note, HUGO_ variables and hugo config commands confirmed against the Hugo docs Configuration introduction page. Nothing removed.

Method: documentation only; no commands were run.
