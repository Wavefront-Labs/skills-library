---
id: computing-software.web-development.mkdocs.dev-addr-and-watch
name: dev-addr-and-watch
category: computing-software
field: web-development
product: mkdocs
tags: [dev-addr, watch, mkdocs-serve, live-reload]
level: practitioner
status: docs-checked
description: "Persist the mkdocs serve address with dev_addr and extra watched directories with watch, and the relative-path difference from the -w CLI option."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set defaults in `mkdocs.yml` so you do not repeat CLI flags on every `mkdocs serve`.

```yaml
dev_addr: '127.0.0.1:8000'   # default; format IP:PORT
watch:
  - directory_a
  - directory_b
```

- `dev_addr` replaces passing `--dev-addr` each time. Must be `IP:PORT`.
- `watch` sets additional directories to watch when running `mkdocs serve`; it lets you set a custom default instead of passing `-w`/`--watch` each time.

Gotcha: paths in the config file are relative to the config file; paths given with `-w`/`--watch` on the command line are not.

Also see `site_url`: a path component there changes the served URL path.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (dev_addr, watch, site_url): default `127.0.0.1:8000`, `IP:PORT` format, YAML list for `watch`, and the relative-path difference. Removed: a claim about which directories are watched by default and a generic verify line.

Method: documentation only; no commands were run.
