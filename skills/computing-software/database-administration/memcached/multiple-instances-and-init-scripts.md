---
id: computing-software.database-administration.memcached.multiple-instances-and-init-scripts
name: multiple-instances-and-init-scripts
category: computing-software
field: database-administration
product: memcached
tags: [init-scripts, multiple-instances, sysconfig, port, p]
level: intro
status: docs-checked
description: "Run several memcached instances on one host and find where packaged init scripts keep startup options."
sources:
  - https://docs.memcached.org/serverguide/configuring/
  - https://docs.memcached.org/serverguide/hardware/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Init scripts: if you installed memcached from your OS package manager, odds are it already comes with an init script, with alternative ways to configure the startup options, such as a `/etc/sysconfig/memcached` file. Check these before editing init scripts or writing your own. If you build from source, the `scripts/` directory in the source tarball contains several example init scripts.

Multiple instances (a developer environment or localhost test cluster): simply change the port the instance listens on.
```
memcached -p 11212
```
When you change the TCP port with -p, the UDP port follows suit.

For NUMA hosts, the Hardware page suggests running one memcached instance per NUMA node and binding the instances via numactl or similar.

`stats settings` reports `tcpport` and `udpport` for a running instance.

## Checked

2026-11-04. Confirmed against the Configuring page (Init Scripts, Multiple Instances, TCP) and the Hardware page (NUMA). Removed: the `-m 64 &` background examples, the sum-of-RAM remark and the nc Verify line, none of which the pages state.

Method: documentation only; no commands were run.
