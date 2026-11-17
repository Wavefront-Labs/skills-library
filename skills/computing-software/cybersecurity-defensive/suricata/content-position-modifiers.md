---
id: computing-software.cybersecurity-defensive.suricata.content-position-modifiers
name: content-position-modifiers
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [depth, offset, distance, within, startswith, endswith]
level: practitioner
status: docs-checked
description: "Constrain where content matches: absolute depth and offset, relative distance and within, and startswith and endswith anchors."
sources: ["https://docs.suricata.io/en/latest/rules/payload-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Positional modifiers

## Absolute
- `depth:N;`: only the first N bytes of the buffer are checked.
- `offset:N;`: start at byte N (`offset:3;` starts at the fourth byte). Combine: `content:"def"; offset:3; depth:3;`.

## Relative to the previous match
- `distance:N;`: where to start searching, N bytes after the last match. Negative values are allowed.
- `within:N;`: the match must lie within N bytes after the previous one. Cannot be zero.
- The absolute value of either must not exceed 1MB (1048576). They are often combined.

## Anchors
- `startswith`: shorthand for `depth:4; offset:0;` style anchoring to the buffer start.
- `endswith`: shorthand for `isdataat:!1,relative;`.
- Both take no arguments, follow a `content`, and startswith cannot be combined with depth, offset, within or distance on that pattern.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/payload-keywords) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
