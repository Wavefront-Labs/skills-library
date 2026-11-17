---
id: computing-software.cybersecurity-defensive.wazuh.decoder-syntax-options
name: decoder-syntax-options
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [decoder-syntax, prematch, plugin-decoder, fts, offset, parent, order]
level: advanced
status: docs-checked
description: "Wazuh decoder XML reference: prematch, program_name, parent, regex, order, offset, plugin_decoder and fts options, and why regex needs prematch."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Decoder options:
- `prematch`: regex the log must match, checked after any syslog header. Optional `offset` (`after_regex`, `after_parent`) and `type` (`osregex` default, or `pcre2`).
- `program_name`: regex matched against the program name in the log header. `type` is `osmatch` by default, `osregex` or `pcre2`.
- `parent`: links a child decoder to a parent that must match first. A child cannot be a parent.
- `regex`: captures values in parentheses. It requires `order`, plus a `prematch` or `program_name` on the decoder or its parent. Optional `offset` (`after_regex`, `after_parent`, `after_prematch`) and `type`.
- `order`: names the captured groups in sequence. Static names include `srcip`, `dstip`, `srcuser`, `dstuser`, `id` and `status`; any other name becomes a dynamic field.
- `offset`: skips part of the entry on prematch, regex or plugin_decoder.
- `plugin_decoder`: built-in plugins PF_Decoder, SymantecWS_Decoder, SonicWall_Decoder, OSSECAlert_Decoder and JSON_Decoder, for when regex is impractical.
- `fts`: triggers an alert the first time the decoder matches; rules use `if_fts`. `ftscomment` adds a note.

Gotchas:
- Repeated prematch, program_name or regex labels are concatenated, and the last label's `type` applies.
- A regex without a prematch or program_name (on itself or its parent) will not work.
- Test decoders with `wazuh-logtest` before writing custom ones.

## Checked

2026-11-08. Read the whole Decoders Syntax page. Confirmed: option list, parent rule (child cannot be parent), program_name and prematch and regex attributes, types and defaults, offset values, concatenation and last-type rule, regex needing order plus prematch or program_name, static field names, plugin_decoder names, fts, ftscomment and if_fts, wazuh-logtest advice. Nothing removed.
Method: documentation only; no commands were run.
