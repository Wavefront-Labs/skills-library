---
id: computing-software.cybersecurity-defensive.suricata.content-matching-basics
name: content-matching-basics
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [content, nocase, hex-content, negated-content]
level: intro
status: docs-checked
description: "Match payload bytes with content: hex escapes, case sensitivity, nocase, multiple contents and negation."
sources: ["https://docs.suricata.io/en/latest/rules/payload-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# content and nocase

- `content` matches raw bytes. Hex goes between pipes, such as `|0D|`.
- Characters that break rule syntax must be hex: `"` as `|22|`, `;` as `|3B|`, `:` as `|3A|`, `|` as `|7C|`.
- Several `content` keywords may appear in one rule. With no modifiers each searches the whole payload.
- Matching is case sensitive by default.
- `nocase` follows the content it modifies and affects only that one.
- A leading `!` negates: `content:!"Firefox/3.6.13";` alerts when that string is absent.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/payload-keywords) read in full; the claims, names, values and examples left in this skill match the page text. Removed the unsourced remark about sticky buffers.

Method: documentation only; no commands were run.
