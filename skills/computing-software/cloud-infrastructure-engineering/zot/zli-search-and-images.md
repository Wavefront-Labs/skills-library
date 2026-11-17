---
id: computing-software.cloud-infrastructure-engineering.zot.zli-search-and-images
name: zli-search-and-images
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, zli-search, zli-image, search-query, search-subject, sort-by]
level: practitioner
status: docs-checked
description: "List images and repos and search a Zot registry with zli image, repo and search query/subject, including sort options and tag-prefix queries."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/user-guides/zli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Listing:

```
bin/zli image list --config local
bin/zli image name busybox:latest --config local
zli repo list
```

`zli image` subcommands: `base`, `cve`, `derived`, `digest`, `list`, `name`. `zli repo` has `list`.

Search:

```
bin/zli search query ng --config local
bin/zli search query nginx: --config local
zli search query "test/repo:2.1."
zli search subject "repo@sha256:f9a0981..."
zli search subject "repo:tag"
```

- `search query`: repository or image search; a trailing colon after a repository name matches that name exactly and lists its tags; without a colon the name is a substring search. `--sort-by` relevance (default), update-time, alpha-asc, alpha-dsc.
- `search subject`: lists all referrers of a subject given as repo:tag or repo@digest. `--sort-by` update-time, alpha-asc (default), alpha-dsc.

Sorting on other commands: `--sort-by <option>`; see `bin/zli image name --help` for the options of that command.

Output format: `-f text|json|yaml`. Use `--config <name>` or a default server to choose the registry; `-u` supplies user credentials.

## Checked

2026-11-08. Read in full: docs/user-guides/zli.md and compared every claim above against it. Removed: the search-extension requirement and the signatures/SBOM example for referrers (not on this page).

Method: documentation only; no commands were run.
