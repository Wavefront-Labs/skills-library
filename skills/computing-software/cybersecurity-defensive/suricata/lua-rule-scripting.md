---
id: computing-software.cybersecurity-defensive.suricata.lua-rule-scripting
name: lua-rule-scripting
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [lua, lua-sandbox, luaxform, security-lua]
level: sme
status: docs-checked
description: "Write Lua detection scripts: the lua keyword, init and match functions, sandbox libraries and limits, per-thread state and security.lua settings."
sources: ["https://docs.suricata.io/en/latest/rules/lua-detection.html", "https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Lua in rules

Suricata 8.0 enables Lua rules by default, in a sandbox, on Lua 5.4. Keyword: `lua:[!]<scriptfilename>;` (path relative to the default rules directory; `!` negates).

## Script functions
- `init`: usually returns an empty table; request buffers explicitly, such as `packet = true`. Buffers needing this: ja3, ja3s, packet, payload, stream.
- `match`: return `1` for a match, `0` otherwise.

## Sandbox
Libraries: base, table, string, math, utf8. Not available: coroutine, package, io, os, debug. Instruction and memory limits apply.

`security.lua` options: `allow-rules: true`, `max-bytes: 500000` (0 disables), `max-instructions: 500000`, `allow-restricted-functions: false`.

## State
One Lua state per rule per thread, shared across unrelated flows, and values persist until rules reload. Kept state reduces later memory budget, so store little.

Lua is also available as the `luaxform` transform.

## Checked

2026-11-04. Confirmed against the Lua Scripting for Detection page (keyword, init and match, sandbox libraries, script state) and the Configuration hardening Lua section of the suricata.yaml page (`security.lua` values).

Method: documentation only; no commands were run.
