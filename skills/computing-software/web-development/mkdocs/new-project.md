---
id: computing-software.web-development.mkdocs.new-project
name: new-project
category: computing-software
field: web-development
product: mkdocs
tags: [mkdocs-new, project-scaffold, mkdocs-yml, getting-started]
level: intro
status: docs-checked
description: "Create a new MkDocs project with mkdocs new, what files it generates, and the single required setting, site_name."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
mkdocs new my-project
cd my-project
```

This creates one configuration file, `mkdocs.yml`, and a `docs` folder holding a single page, `index.md`. `docs` is the default value of the `docs_dir` setting.

The config file is `mkdocs.yml` in the project directory by default; use `-f`/`--config-file` to point at another path (see `mkdocs build --help`).

`site_name` is the only required option:

```yaml
site_name: MkLorum
```

Everything else is optional. Run commands from the directory that contains `mkdocs.yml`.

Next: `serve-live-preview`, `nav-config-basics`.

## Checked

2026-11-04. Confirmed against Getting Started and the configuration guide (Introduction, site_name): `mkdocs new my-project`, the generated `mkdocs.yml` and `docs/index.md`, `docs_dir` default, `-f`/`--config-file`, and `site_name` as the only required setting. Removed: a generic verify line.

Method: documentation only; no commands were run.
