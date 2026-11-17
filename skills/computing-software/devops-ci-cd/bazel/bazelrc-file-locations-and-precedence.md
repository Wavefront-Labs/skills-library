---
id: computing-software.devops-ci-cd.bazel.bazelrc-file-locations-and-precedence
name: bazelrc-file-locations-and-precedence
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bazelrc, rc-files, try-import, bazelrc-precedence, ignore-all-rc-files, nohome-rc, import-if-bazel-version]
level: practitioner
status: docs-checked
description: "Know which bazelrc files Bazel reads and in what order, how import and try-import behave, and how command-line flags win."
sources: ["https://bazel.build/run/bazelrc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# bazelrc locations, imports and precedence

Bazel reads rc files in this order, later files overriding earlier ones:

1. System RC: `/etc/bazel.bazelrc` (Linux/macOS), `%ProgramData%\bazel.bazelrc` (Windows). Disable with `--nosystem_rc`.
2. Workspace RC: `.bazelrc` next to `MODULE.bazel`. Disable with `--noworkspace_rc`.
3. Home RC: `$HOME/.bazelrc`. Disable with `--nohome_rc`.
4. Each path in the `BAZELRC` environment variable (comma-separated).
5. Files named with `--bazelrc=file` (repeatable). `--bazelrc=/dev/null` makes all later `--bazelrc` entries be ignored.

These control flags are startup options: they go after `bazel` and before the command. `--ignore_all_rc_files` skips everything.

Line grammar: one directive per line, words tokenized like Bourne shell, `#` comments. Lines for the same command are combined as if on one line.

Imports: `import %workspace%/path/x.rc` fails if missing; `try-import` does not; `try-import-if-bazel-version >=7.0.0 %workspace%/y.rc` also checks the Bazel version (operators `>`, `>=`, `<`, `<=`, `==`, `!=`, `~`). Options in an imported file beat options before the import and lose to options after it.

Precedence: command-line flags beat rc files. Within rc files a more specific command beats a less specific one: `test`, `run`, `clean`, `mobile-install`, `info`, `print_action`, `config`, `cquery`, `aquery` inherit from `build`; `coverage`, `fetch`, `vendor` inherit from `test`; everything inherits `common`. Put `common` first and specific commands last so reading order equals precedence.

## Checked

2026-11-04. Read against the Bazel docs page(s): Write bazelrc configuration files (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the user.bazelrc best-practice line (not on the page) and the closing Verify line.
Method: documentation only; no commands were run.
