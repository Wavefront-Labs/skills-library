---
id: computing-software.database-administration.memcached.meta-command-basics
name: meta-command-basics
category: computing-software
field: database-administration
product: memcached
tags: [meta-commands, mg, ms, md, meta-protocol]
level: practitioner
status: docs-checked
description: "Syntax of the meta text protocol: two-letter commands, single-character flags with tokens, return codes HD VA EN NF NS EX."
sources:
  - https://docs.memcached.org/protocols/meta/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Meta commands are ASCII-based commands with a flag system. They replace the basic storage and retrieval commands, include every feature of the binary protocol (which is deprecated), and mix freely with classic commands on the same connection. They do not replace specialised commands outside the storage and retrieval categories.

Request: `<cm> <key> <datalen*> <flag1> <flag2> ...\r\n` where `<cm>` is a 2-character command code and datalen is only for commands with payloads. Response: `<RC> <datalen*> <flag1> <flag2> ...\r\n` with a 2-character return code; `datalen` appears only with `VA`.

Examples (Meta page):
```
ms foo 2 T90 F1\r\nhi\r\n     -> HD
mg foo t f v                  -> VA 2 t78 f1\r\nhi
md foo                        -> HD
mn                            -> MN
me foo                        -> ME foo exp=.. la=.. cas=.. fetch=.. cls=.. size=..
```
Commands: `mg`, `ms`, `md`, `ma` (arithmetic), `mn` (no-op), `me` (debug). Flags are single characters, some with token arguments directly after (`T30`, `Oopaque`); requested response flags come back in the order they were sent.

Return codes: `HD` (success, header only), `VA <size>` (value follows), `EN` (miss), `NF` (not found), `NS` (not stored), `EX` (exists, for example CAS mismatch). Syntax errors are handled like the normal ERROR/CLIENT_ERROR strings.

All commands accept the tokens `P` and `L`, which are completely ignored; they can be used as hints or path specifications for a proxy or router in between.

## Checked

2026-11-04. Confirmed against the Meta Text Protocol page (Command Basics) and protocol.txt (Meta Commands, Meta Debug, return codes). Removed: nothing factual; wording tightened.

Method: documentation only; no commands were run.
