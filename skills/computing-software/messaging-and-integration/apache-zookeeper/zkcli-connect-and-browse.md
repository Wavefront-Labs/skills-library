---
id: computing-software.messaging-and-integration.apache-zookeeper.zkcli-connect-and-browse
name: zkcli-connect-and-browse
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, zkcli, zkcli-ls, zkcli-stat, startup-options, history]
level: intro
status: docs-checked
description: "zkCli.sh startup options and read commands: -server, -timeout, -waitforconnection, -client-configuration, ls, get, stat, history, redo and whoami."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
  - https://zookeeper.apache.org/doc/current/zookeeperStarted.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zkCli: connect and browse

Startup (`bin/zkCli.sh`):
- With no arguments it connects to localhost on the default port 2181.
- `-server host:port`, `-timeout ms` (the page's example `-timeout 3000` is 3 s), `-waitforconnection` (wait for connection success before executing commands), `-client-configuration file`.

Commands:
- `ls [-s] [-w] [-R] path`: children (`-s` stat, `-w` child watch, `-R` recursive).
- `get [-s] [-w] path`: data (`-s` stat, `-w` data watch).
- `stat [-w] path`; `getAllChildrenNumber path`; `getEphemerals [path]` (ephemeral nodes created by this session).
- `printwatches [on|off]` (watch events print only when on); `history`; `redo cmdno`; `whoami`; `version`; `help`; `quit`.
- `connect host:port`, `close`, `sync path`, `config [-c] [-w] [-s]`.

Prompt looks like `[zkshell: 8]`; on a new server `ls /` shows `[zookeeper]`. `get` output includes the stat fields (cZxid, ctime, mZxid, mtime, pZxid, cversion, dataVersion, aclVersion, ephemeralOwner, dataLength, numChildren).

Verify: `ls /` lists `zookeeper`, and `get -s` on a node shows stat fields.

## Checked
Confirmed against the zkCli reference and the Getting Started guide sample session, 2026-11-08.
Method: docs-only read of cited pages, 2026-11-08
