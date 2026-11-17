---
id: computing-software.systems-network-administration.audiobookshelf.migrate-os-or-paths-overview
name: migrate-os-or-paths-overview
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [migration, absolute-paths, windows-to-docker, abstoolbox, unsupported]
level: advanced
status: docs-checked
description: "Understand why moving Audiobookshelf between OS, install method or paths is unsupported, and the best-effort approaches the docs give."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/migration-os.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/cors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Switching installation methods (Linux, Windows, Docker) is **not a supported process**. The guide is best-effort, with no guarantee, and the docs ask people not to open GitHub issues about it; use the Discord server for help.

Why it is hard: Audiobookshelf stores all data with absolute paths. Full file paths to books and folders are hardcoded and do not adapt when the root changes. Paths inside metadata files are absolute too, and will not update if you change the metadata path; that can only be set at initial setup.

Generally reliable method: replicate the original file system structure on the new system, even from Windows to Linux. Preserve the exact directory structure and, where possible, file permissions. Migrations from Windows are problematic because of the backslash (`\`) in paths.

Preferred tooling: a web-first community tool, ABS Toolbox (Migrate-Server), a third-party tool not affiliated with Audiobookshelf. It needs no local Python or manual database edits. Add the tool's origin to the CORS allowed origins on both old and new servers. An older community Python script is the legacy method for Windows to Docker.

## Checked

Method: docs-checked 2026-11-09 against the Migrating an OS or File Paths page and the CORS page of the Audiobookshelf docs repo, both read in full from raw markdown.
