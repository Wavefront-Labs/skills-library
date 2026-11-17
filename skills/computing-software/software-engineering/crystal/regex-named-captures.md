---
id: computing-software.software-engineering.crystal.regex-named-captures
name: regex-named-captures
category: computing-software
field: software-engineering
product: crystal
tags: [regex-named-captures, regex, named-captures, match-data, capture-groups, to-h, optional-group, nilable-capture, crystal]
level: practitioner
status: docs-checked
description: "Read named and numbered groups from MatchData, use optional groups safely, and convert to hashes."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MatchData and named captures

Goal: parse structured text.

```crystal
if m = line.match(/(?<ip>[\d.]+) (?<code>\d{3})(?: (?<bytes>\d+))?/)
  ip = m["ip"]            # String, raises if group missing
  code = m["code"].to_i
  bytes = m["bytes"]?     # String?
end
```
- `m[1]`, `m[1]?`, `m["name"]`, `m.to_a` (Array(String?)), `m.named_captures` (Hash), `m.captures`.
- Group not participating gives nil via `?`; `[]` raises IndexError/KeyError.
- `Regex#name_table` lists group names (index to name).
- Case-switch: `case line when /^GET/ ... end` sets `$~`.

Gotchas:
- Mixing named and numbered groups numbers named ones too.
- Use `String#match(re, pos)` to continue at an offset.
- Anchors: `\A` and `\z` for whole-string checks; `^`/`$` are line anchors.

Verify: parse a log line spec with and without the optional group.

## Checked

Date 2026-11-03. Confirmed MatchData#[] and []? (index and name), to_a (Array(String?)), captures (Array(String?)), named_captures (Hash(String, String?)), Regex#name_table and String#match(regex, pos) in the Regex and MatchData source. Removed Regex#names (no such method in the source).

Method: documentation only; no commands were run.
