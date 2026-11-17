---
id: computing-software.web-development.hugo.project-directory-structure
name: project-directory-structure
category: computing-software
field: web-development
product: hugo
tags: [directory-structure, project-layout, unified-file-system, mounts, themes]
level: intro
status: docs-checked
description: "What each Hugo project directory holds (archetypes, assets, content, data, i18n, layouts, static, themes) and how the unified file system layers mounts."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/getting-started/directory-structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`hugo new project my-project` creates `archetypes/default.md`, `assets`, `content`, `data`, `i18n`, `layouts`, `static`, `themes` and `hugo.toml`.

- `archetypes`: templates for new content.
- `assets`: global resources for the asset pipeline (images, CSS, Sass, JavaScript, TypeScript).
- `config`: optional split configuration; a single `hugo.toml` suffices for minimal projects.
- `content`: Markdown and other markup plus page resources.
- `data`: JSON, TOML, YAML or XML files.
- `i18n`: translation tables.
- `layouts`: templates.
- `public`: the published site, recreated as needed.
- `resources`: cached asset pipeline output, recreated as needed.
- `static`: copied to `public` unchanged (for example `favicon.ico`, `robots.txt`).
- `themes`: one subdirectory per theme.

Unified file system:

- Hugo can mount two or more directories to one location, for `archetypes`, `assets`, `content`, `data`, `i18n`, `layouts` and `static`.
- A custom mount replaces the default mount for that component; mount both to overlay.
- Hugo does not follow symbolic links.
- When paths collide, the first mount wins. A project file overrides a theme file at the same path.

```toml
[[module.mounts]]
source = 'content'
target = 'content'
```

`hugo new theme my-theme` creates a theme skeleton.

## Checked

2026-11-04: skeleton contents, directory descriptions, mountable components, custom mount replacement, symlink note, mount precedence and theme skeleton confirmed against the Hugo docs Directory structure page. Nothing removed.

Method: documentation only; no commands were run.
