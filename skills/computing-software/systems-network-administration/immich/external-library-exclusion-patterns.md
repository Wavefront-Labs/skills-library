---
id: computing-software.systems-network-administration.immich.external-library-exclusion-patterns
name: external-library-exclusion-patterns
category: computing-software
field: systems-network-administration
product: immich
tags: [exclusion-patterns, glob, picomatch, raw-files, case-insensitive]
level: practitioner
status: docs-checked
description: "Write Immich external library exclusion glob patterns: full-path matching, ** and * semantics, extension groups, escaping, and case-insensitivity."
sources:
  - https://docs.immich.app/features/libraries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep unwanted files, such as raw originals or system folders, out of an external library.

By default everything under the import paths is added. Exclusion patterns are glob patterns matched against the full file path; a match excludes the file. Add them in the library's management page under Exclusion Patterns, then Scan.

Examples:

- `**/*.tif` excludes every `.tif` file.
- `**/hidden.jpg` excludes files named `hidden.jpg`.
- `**/Raw/**` excludes everything in any directory named `Raw`.
- `**/*.{tif,jpg}` excludes `.tif` and `.jpg` files.
- `**/*.{arw,dng}` excludes `.arw` and `.dng` files.
- `**/\@eaDir/**` excludes any directory named `@eaDir`; special characters such as `@` must be escaped with a backslash.

Semantics: `*` matches zero or more characters within one file or directory name. `**` matches zero or more subdirectories recursively; at the end of a pattern it also includes every file inside.

Matching is case-insensitive for both new files and already imported assets, so `**/*.{arw,dng}` also excludes `.ARW` and `.DnG`.

Glob syntax follows Picomatch.

The same ignore patterns work with the CLI: `immich upload --ignore **/Raw/** --recursive directory/`.

In the worked example, a trip library excludes `**/Raw/**` while videos and old photos live in a separate library with no exclusions. Plan libraries by exclusion needs, since patterns apply per library.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/libraries in full (Exclusion Patterns, Usage worked example) and features/command-line-interface (the `--ignore` option).
Removed: the Synology attribution for `@eaDir`, which the page does not state.
Method: documentation only; no commands were run.
