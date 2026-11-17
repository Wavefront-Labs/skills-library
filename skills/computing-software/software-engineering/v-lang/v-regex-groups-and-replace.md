---
id: computing-software.software-engineering.v-lang.v-regex-groups-and-replace
name: v-regex-groups-and-replace
category: computing-software
field: software-engineering
product: v-lang
tags: [v-regex-groups-and-replace, regex-module, regex groups, capture group, replace, replace_by_fn, split, get_group, named groups, v-lang]
level: practitioner
status: draft
description: "Read capture groups after find, replace matches with replace or replace_by_fn, and split text by regex."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capture groups, replace and split

Goal: extract and transform with regex.

- After `start, end := re.match_string(s)` (or `find`), read groups: `re.get_group_by_id(s, 0)`, named `(?P<year>\d{4})` via `re.get_group_by_name(s, 'year')`, or the raw `re.groups` index array (pairs of start,end).
- Replace: `re.replace(text, 'X')`, with groups `re.replace(text, r'\1-\0')` (confirm group reference syntax), or callback `re.replace_by_fn(text, fn (re regex.RE, in string, start int, end int) string { return 'N' })`.
- Split: `re.split(text)`.
- Always check `start >= 0` to detect no match.
- For simple needs prefer string methods (`split`, `replace`, `contains`).

Gotchas:
- Group indexes are 0-based and index into positions array not strings.
- Greedy quantifiers on large inputs can be slow.

Verify: extract year, month, day from a date string via groups.
