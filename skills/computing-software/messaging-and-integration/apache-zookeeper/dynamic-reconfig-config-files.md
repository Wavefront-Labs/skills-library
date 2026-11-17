---
id: computing-software.messaging-and-integration.apache-zookeeper.dynamic-reconfig-config-files
name: dynamic-reconfig-config-files
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, dynamic-reconfiguration, dynamicconfigfile, reconfigenabled, server-line, role]
level: advanced
status: docs-checked
description: "Dynamic reconfiguration setup: reconfigEnabled, server line syntax with role and client port, dynamicConfigFile split, version naming and backward compatibility."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic reconfiguration: config layout

- Since 3.5.0 the set of servers, their roles (participant / observer), all ports and even the quorum system can change at runtime without rolling restarts. Since 3.5.3 the feature is disabled by default; set `reconfigEnabled=true` in `zoo.cfg` to allow reconfig (otherwise reconfig attempts fail, authenticated or not). Reconfig also needs ACL setup and authentication; see the Security section of the page.
- Server line: `server.<positive id> = <address1>:<port1>:<port2>[:role];[<client port address>:]<client port>`. Role is `participant` (default) or `observer`; the client port address defaults to 0.0.0.0.
- From 3.5.0 `clientPort` and `clientPortAddress` should no longer be used; the client port is part of the server line. Since 3.6.0 several addresses per server may be given, separated by a pipe, for example `server.2=zoo2-net1:2888:3888|zoo2-net2:2889:3889;2188`.
- Dynamic parameters are `server`, `group` and `weight`. They live in a separate dynamic configuration file linked from the static file with `dynamicConfigFile`. Once created, do not edit it by hand: ZooKeeper pushes changes to it on all servers.
- A single-file config is split automatically at boot into static and dynamic files; redundant `clientPort` lines are removed and the original static file is backed up as a `.bak` file.
- The config version equals the zxid of the reconfig command that created it. It becomes part of the dynamic file name, the static file is updated to point at the new file, and earlier files are kept as backups. Never alter the version manually.
- `standaloneEnabled=false` (static file) runs the distributed stack even with one participant, so a single-participant ensemble can grow and an ensemble can shrink to one participant. With the default (true) a single-server ensemble cannot grow, and one with several servers cannot shrink below two participants.
- Upgrading to 3.5.0 in a rolling fashion requires going through 3.4.6 first.

Verify: `config -c` in the CLI prints only the version and the client connection string, for example `400000003 localhost:2791,localhost:2793,localhost:2792`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the whole Dynamic Reconfiguration page. Reworded: the client-port line now says the old keys should no longer be used rather than "supersedes".
