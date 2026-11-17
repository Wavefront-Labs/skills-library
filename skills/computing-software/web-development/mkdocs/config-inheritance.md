---
id: computing-software.web-development.mkdocs.config-inheritance
name: config-inheritance
category: computing-software
field: web-development
product: mkdocs
tags: [inherit, config-inheritance, deep-merge, stdin-config]
level: advanced
status: docs-checked
description: "Share MkDocs settings across sites with the INHERIT key, understand the deep-merge rules and why plugins/extensions need dict syntax, and override via stdin."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Put common options in a parent file and point at it from the site's `mkdocs.yml` (path relative to the primary file):

```yaml
INHERIT: ../base.yml
site_name: Foo Project
site_url: https://example.com/foo
```

MkDocs parses both files and deep merges them. Rules:
- To merge, options must be key/value pairs. `markdown_extensions` and `plugins` must use the alternative syntax (`toc: {permalink: true}`), not `- item` lists.
- Any non-key (a list) is replaced, never appended to. You cannot merge `nav` items; define the full navigation in the primary file.
- Path options are not rewritten, and are relative to the primary file; define them there only.

Override a key from the command line using stdin as the config:

```bash
echo '{INHERIT: mkdocs.yml, site_name: "Renamed site"}' | mkdocs build -f -
```

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (Configuration Inheritance): the `INHERIT` key, deep merge, dict syntax for plugins and extensions, lists replaced not appended, nav not mergeable, path options relative to the primary file, and the stdin example. Removed: a generic verify line.

Method: documentation only; no commands were run.
