---
id: computing-software.web-development.eleventy.incremental-builds
name: incremental-builds
category: computing-software
field: web-development
product: eleventy
tags: [incremental-builds, ignore-initial, template-dependencies, explicit-incremental]
level: advanced
status: docs-checked
description: "Speed local Eleventy rebuilds with --incremental: what is rebuilt for templates, layouts, data, includes and collections, and when a full build runs."
sources:
  - https://www.11ty.dev/docs/usage/incremental/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--incremental` rebuilds only what changed during local development. It starts with a full build as a baseline.

- **Templates:** a changed template rebuilds alone.
- **Layouts** (v2.0.0+): templates using a changed layout rebuild.
- **Dependencies** (v2.0.0+): templates using something registered via `addDependencies` (custom languages) rebuild when it changes.
- **Includes, JS modules, data files** (pre-release only, v4.0.0-alpha.11): templates using a changed include or imported JS module rebuild; template/directory data files rebuild only their templates; global data rebuilds templates reading that top-level key. A full build runs when the file is new, deleted, or unused, or when a module is also imported by the config or a data file.
- **Render plugin** (pre-release only, v4.0.0-alpha.11): templates rendering a changed file rebuild; files outside the input directory still need `addWatchTarget`.
- **Collections** (v2.0.0+): adding or removing a tag rebuilds templates using that collection, as declared by `pagination.data` or `eleventyImport.collections`.
- **Passthrough copy:** copy only changed files; prefer serve emulation (`setServerPassthroughCopyBehavior("passthrough")`).
- **Config file** change: full build.

Flags: `--ignore-initial` skips the startup build (v2.0.0+). `--incremental=filename` (v3.0.0+) builds one file and its dependencies; multiple files via `--incremental=file1 --incremental=file2` or `--incremental=file1,file2` (pre-release only, v4.0.0-alpha.8).

WebC adds component-graph rebuilds. Not yet available: cold-start incremental and incremental on CI.

## Checked

2026-11-04. Source page corrected: the cited usage-incremental URL returns 404; the content is at /docs/usage/incremental/. Confirmed there: the --incremental flag, templates, layouts (v2.0.0), addDependencies template dependencies (v2.0.0), includes, JavaScript dependencies and data files (pre-release only, v4.0.0-alpha.11) with the full-build conditions, Render plugin rebuilds and the addWatchTarget note, collections via pagination.data or eleventyImport.collections (v2.0.0), passthrough copy behavior and serve emulation (v2.0.0), config file full build, --ignore-initial (v2.0.0), explicit incremental (v3.0.0), batched incremental (pre-release only, v4.0.0-alpha.8), WebC graph rebuilds and the to-do items. Corrected pre-release version gates to the stable or pre-release labels the page gives.

Method: documentation only; no commands were run.
