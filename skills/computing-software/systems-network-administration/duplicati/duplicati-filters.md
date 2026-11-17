---
id: computing-software.systems-network-administration.duplicati.duplicati-filters
name: duplicati-filters
category: computing-software
field: systems-network-administration
product: duplicati
tags: [filters, include-exclude-rules, globbing, regex-filters, filter-groups, environment-variables-in-filters]
level: advanced
status: docs-checked
description: "Write Duplicati include and exclude filters with paths, globs, regular expressions and predefined groups, and understand first-match ordering."
sources: ["https://docs.duplicati.com/detailed-descriptions/security-and-secrets/filters-in-duplicati"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Filters in Duplicati

Duplicati represents folders with a trailing path separator and requires a full match including it, so `/data/photos/` is a folder and `/data/photos` a file. Four filter kinds exist:
- Path: the full path of a file or folder.
- Glob: `?` matches one character, `*` any number; for example `/data/IMG_????.jpeg`, `/data/*/Download/` and `*.iso`.
- Regular expression, wrapped in square brackets: `[/data/IMG_\d{4}\.jpeg]`, `[.*\.iso]`. On Windows each path separator must be escaped as a double backslash.
- Predefined groups in curly braces, comma separated: `SystemFiles`, `OperatingSystem`, `CacheFiles`, `TemporaryFiles`, `Applications` and `DefaultExcludes` (all of them), not case sensitive, with aliases such as `Sys`, `OS`, `Cache`, `Temp`, `App` and `Exc`. `duplicati-cli help filter-groups` lists the paths each group holds on your system.

Environment variables use the `%NAME%` form on every OS (not `$NAME`); in a backup configuration the UI folder names `%MY_DOCUMENTS%`, `%DESKTOP%` and `%HOME%` are replaced too, and in regex filters the value is escaped.

Evaluation: everything is included by default, so most filters are excludes. Prefix `+` for include and `-` for exclude. Only the first full match counts, rules run in the order given and folders are evaluated before files. You cannot include a file if its parent folder is excluded. Example: `+/data/*.txt`, `-*.txt` includes txt files in `/data/` and excludes other txt files. A final `-/data/` excludes the whole folder, so the include never runs, which also avoids scanning subfolders.

## Checked

2026-11-04. Confirmed against the Filters in Duplicati page. Example paths in the skill (/data/...) are illustrative variants of the page's /usr/share examples; rules and group names confirmed.

Method: documentation only; no commands were run.
