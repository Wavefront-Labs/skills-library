---
id: computing-software.messaging-and-integration.apache-zookeeper.four-letter-word-whitelist
name: four-letter-word-whitelist
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, 4lw-commands-whitelist, whitelist, srvr, isro, security]
level: practitioner
status: docs-checked
description: "Enable ZooKeeper four-letter words with 4lw.commands.whitelist: default is srvr only, isro added in read-only mode, and the star wildcard."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 4lw.commands.whitelist

- New in 3.5.3: four-letter words must be explicitly whitelisted before use.
- Property `4lw.commands.whitelist` (Java system property `zookeeper.4lw.commands.whitelist`): comma-separated list of commands. By default it contains only `srvr`, which zkServer.sh uses. If Read Only Mode is enabled through the Java system property `readonlymode.enabled`, `isro` is added.
- Other commands are disabled by default; using one gets the response "... is not executed because it is not in the whitelist."
- Example from the guide: `4lw.commands.whitelist=stat, ruok, conf, isro`. The asterisk enables all: `4lw.commands.whitelist=*`.
- The guide says four-letter words will be deprecated and recommends the AdminServer instead.

## Checked

Confirmed against the Administrator's Guide (4lw.commands.whitelist, four-letter words, isro). Removed the unsourced advice about expensive commands and the Verify step.

Method: docs-only read of cited pages, 2026-11-08
