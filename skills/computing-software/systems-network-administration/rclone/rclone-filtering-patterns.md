---
id: computing-software.systems-network-administration.rclone.rclone-filtering-patterns
name: rclone-filtering-patterns
category: computing-software
field: systems-network-administration
product: rclone
tags: [filtering, include, exclude, glob, regex, filter-from, dump-filters]
level: practitioner
status: docs-checked
description: "How rclone filter patterns work: glob syntax, rooted patterns, regex in double braces, rule ordering and testing with dump filters."
sources: ["https://rclone.org/filtering/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Filter flags decide which files sync, move, ls, size, delete, check and similar commands apply to. `purge` ignores filters. Filters only work as command-line flags, not inside remote specs (`rclone copy "remote:dir*.jpg"` does nothing special).

## Glob syntax

`*` matches non-separator characters, `**` matches anything including `/`, `?` one non-separator, `[a-z]` ranges, `{a,b}` alternatives, `{{regexp}}` a regular expression. A pattern starting with `/` is rooted at the remote root (not necessarily the drive root); otherwise it matches from the end of the name on a path-element boundary, so `file.jpg` matches `dir/file.jpg` but not `afile.jpg`. Patterns are case sensitive unless `--ignore-case`. Always use `/`, even on Windows.

## Regular expressions

`{{regexp}}` becomes `(^|/)(regexp)$`, and `/{{regexp}}` becomes `^(regexp)$`. Mix with glob: `*.{{jpe?g}}`, case-insensitive `*.{{(?i)jpg}}`. Keep wildcards from crossing separators: `{{start[^/]*end\.jpg}}`, not `{{start.*end\.jpg}}`. Any regex disables directory-filter optimisation.

## Rule order

Do not mix `--include`, `--exclude` and `--filter` in one command; use `--filter` with `+ ` and `- ` prefixes in one ordered list. Same-type flags are processed in command-line order, and files in `--filter-from` top to bottom. First match wins; no match means included. Any `--include` or `--include-from` implies a final `- **`, but a `+` in `--filter` does not.

```text
- /dir1/
- /dir2/
+ *.pdf
- **
```

Run with `-vv --dump filters` to see the compiled rules and how each path is matched.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
