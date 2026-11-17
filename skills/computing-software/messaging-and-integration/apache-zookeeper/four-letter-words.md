---
id: computing-software.messaging-and-integration.apache-zookeeper.four-letter-words
name: four-letter-words
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, four-letter-words, ruok, mntr, srvr, stat, wchc, 4lw]
level: practitioner
status: docs-checked
description: "ZooKeeper four-letter-word commands: ruok, srvr, stat, mntr, conf, cons, dump, envi, wchs/wchc/wchp, isro, hash, stmk and which are expensive."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Four-letter words

Sent as plain text to the client port (for example with `echo ruok | nc host port`). Since 3.5.3 each command must be whitelisted with `4lw.commands.whitelist` (a list such as `stat, ruok, conf, isro`, or `*`).

- `ruok`: `imok` if running (does not prove quorum membership); otherwise no reply, or a "not in the whitelist" message when disabled.
- `srvr`: full server details; `stat`: brief server plus clients.
- `mntr`: tab-separated key/value pairs for monitoring (3.4.0+); keys may change, and some are leader-only or platform-specific.
- `conf`: serving configuration; `envi`: serving environment.
- `cons`: full connection/session details; `crst` resets connection stats.
- `dump`: outstanding sessions and ephemeral nodes.
- `wchs`: watch summary; `wchc`: watches by session; `wchp`: watches by path.
- `srst`: reset server statistics.
- `isro`: `ro` or `rw` (3.4.0+).
- `hash`: recent tree digest history by zxid (3.6.0+).
- `gtmk` / `stmk`: get/set the 64-bit trace mask (default 0b0100110010; logback must enable TRACE).
- `wchc` and `wchp` are documented as potentially expensive; the AdminServer docs say the same of `cons`, `dump` and `stat`.
- Four-letter words are slated for deprecation in favour of the AdminServer (HTTP on port 8080 by default, /commands/name).

Verify: sending `ruok` to the client port returns `imok` (after whitelisting).

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Administrator's Guide (Four Letter Words and AdminServer sections).
