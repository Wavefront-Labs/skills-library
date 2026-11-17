---
id: computing-software.data-engineering.apache-hadoop.hdfs-ha-automatic-failover-fencing
name: hdfs-ha-automatic-failover-fencing
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, high-availability, zkfc, fencing, zookeeper]
level: advanced
status: docs-checked
description: "HDFS HA automatic failover: dfs.ha.automatic-failover.enabled, ha.zookeeper.quorum, zkfc -formatZK, and fencing methods sshfence and shell with their keys."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic failover and fencing

Enable:
- hdfs-site.xml: `dfs.ha.automatic-failover.enabled` = `true`.
- core-site.xml: `ha.zookeeper.quorum` = comma-separated host:port list. Optional `ha.zookeeper.auth` and `ha.zookeeper.acl` take an `@`-prefixed file path.

Initialise once from a NameNode host: `hdfs zkfc -formatZK`. Then `start-dfs.sh` starts the ZKFC automatically; manually use `hdfs --daemon start zkfc`.

Shut the cluster down first: the page says you cannot move from manual to automatic failover while it runs. Keys can be suffixed with the nameservice ID, e.g. `dfs.ha.automatic-failover.enabled.my-nameservice-id`. ZooKeeper is assumed already running (three or five nodes; its data best on separate disks from HDFS metadata). Each NameNode host runs a ZKFC that health-checks its NameNode, holds a ZooKeeper session, and takes an ephemeral lock znode to win election. If ZooKeeper goes down, no automatic failover occurs but HDFS keeps running. There is no preferred-primary setting; whichever NameNode starts first becomes active. Start order of ZKFC and NameNode does not matter. Monitor that ZKFC stays running and monitor the ZooKeeper servers.

Fencing: with QJM only one NameNode can write to the JournalNodes, so metadata cannot be corrupted, but the old active may still serve stale reads until it shuts down, so fencing is still advised. `dfs.ha.fencing.methods` is a carriage-return-separated list tried in order until one succeeds. Three methods ship: shell, sshfence, powershell (Windows only; `powershell(NameNode)`).
- `sshfence` (or `sshfence([[username][:port]])`) SSHes without a passphrase and uses fuser to kill the process on the service's TCP port. Needs `dfs.ha.fencing.ssh.private-key-files`; optional `dfs.ha.fencing.ssh.connect-timeout` in milliseconds.
- `shell(<command>)` is passed to bash and may not contain a closing parenthesis; exit code 0 means success. Variables: `$target_host`, `$target_port`, `$target_address`, `$target_nameserviceid`, `$target_namenodeid`. It has no built-in timeout.

For availability, end the list with a method guaranteed to succeed. A value must still be configured if you use no real fencing: `shell(/bin/true)`.

`dfs.ha.nn.not-become-active-in-safemode` = true stops a NameNode in safe mode from becoming active.

Manual switch: `hdfs haadmin -failover [--forcefence] [--forceactive] <id1> <id2>`.

To test, find the active NameNode in the web UI, then `kill -9` it (or power-cycle or unplug it); the other should become active within several seconds, governed by `ha.zookeeper.session-timeout.ms` (default 5 seconds). If not, check the zkfc and NameNode logs. A manual `hdfs haadmin` failover still works when automatic failover is configured.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HDFSHighAvailabilityWithQJM.md in the apache/hadoop repo). Core keys were accurate; added the shutdown prerequisite, powershell method and failure behaviour, and replaced the invented verify step with the page's own failover test.
