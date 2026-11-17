---
id: computing-software.software-engineering.lua.lua-text-processing-recipes
name: lua-text-processing-recipes
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-text-processing, text-processing-recipes]
level: practitioner
status: docs-checked
description: "Implement split, trim, join, simple CSV parsing and template substitution with correct patterns."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splitting, trimming, CSV and template substitution
- Trim: `s:match("^%s*(.-)%s*$")`; split on a delimiter: `for part in (s .. ","):gmatch("(.-),") do ... end` (this keeps empty fields).
- Plain-text find without patterns: `s:find(needle, 1, true)` (the fourth parameter of `string.find` is `plain`).
- Template: `s:gsub("{{(%w+)}}", vars)` where `vars` is a table queried with the first capture as key; if the value is `false` or `nil` the original match is kept. `gsub` also returns the match count as a second value.
- Join with `table.concat(list, sep)`.
- CSV with quoted fields needs a state machine or a library; `split` on commas breaks on quoted commas.
- Process large files line by line with `io.lines(filename)` (it closes the file at the end) instead of reading the whole file.
Verify: unit tests with empty fields, quotes and trailing delimiters.

## Checked
2026-11-08. Confirmed in the Lua 5.4 Reference Manual: `string.find`, `string.gsub` (table and function replacement rules), `table.concat`, `io.lines`, read via targeted reads of those entries. The pattern items in the trim and split lines follow section 6.4.1 but were not re-read there. Removed: the named CSV library.
Method: documentation only; no commands were run.
