---
id: computing-software.messaging-and-integration.apache-zookeeper.admin-server
name: admin-server
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, adminserver, jetty, http-commands, admin-serverport, commands-endpoint]
level: practitioner
status: docs-checked
description: "The ZooKeeper AdminServer: Jetty HTTP endpoint on port 8080 at /commands, its settings with defaults and the list of commands it serves."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AdminServer

New in 3.5.0: an embedded Jetty server giving an HTTP interface to the four-letter-word commands. Commands are at `/commands/[command name]` (for example `http://localhost:8080/commands/stat`) and `/commands` lists them; responses are JSON. Commands can have several names (`stmk` is also `set_trace_mask`).

Enabled by default, listening on `0.0.0.0` over plain HTTP with no client authentication. The guide says the defaults suit trusted environments only: bind to a management address or `127.0.0.1`, use `admin.forceHttps=true` with `admin.needClientAuth=true`, and restrict the port with firewall rules.

Settings and documented defaults:
- `admin.enableServer` true; `admin.serverAddress` 0.0.0.0; `admin.serverPort` 8080.
- `admin.commandURL` /commands; `admin.idleTimeout` 30000 ms.
- `admin.snapshot.enabled` and `admin.restore.enabled` true; `admin.rateLimiterIntervalInMS` 5 mins (3.9.0+).
- `admin.needClientAuth` false (x509 auth requires true); `admin.forceHttps` disabled (3.7.1+, overrides `admin.portUnification`); `admin.portUnification` disabled (3.6.0+).

Commands (long names/short): conf, cons, crst, dirs, dump, envi, gtmk, hash, icfg, isro, lsnp (last_snapshot), lead (leader), mntr, obsr, orst, rest (restore), ruok, snap (snapshot), srvr, stat, srst, stmk, sysp, voting_view, wchc, wchp, wchs, zabstate. `snap` and `rest` are rate-limited to once every 5 mins by default. Several (cons, dump, stat, wchc, wchp) can be expensive on a busy server.

Disable with the `zookeeper.admin.enableServer` system property set to false (config key `admin.enableServer=false`), or by removing Jetty from the classpath. The four-letter-word TCP interface stays available either way.

Verify: `curl http://localhost:8080/commands/stat` returns JSON.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the AdminServer, AdminServer configuration and Security Considerations sections of the Administrator's Guide. Corrected: the disable property is a system property, and the example host is localhost as in the guide.
