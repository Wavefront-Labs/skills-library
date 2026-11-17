---
id: computing-software.database-administration.memcached.startup-flags-m-d-v
name: startup-flags-m-d-v
category: computing-software
field: database-administration
product: memcached
tags: [startup-options, memory-limit, daemonize, verbosity, m]
level: intro
status: docs-checked
description: "First-run startup flags for memcached: -m item memory, -d daemonize, -v verbosity, and how limit_maxbytes proves the flag took."
sources:
  - https://docs.memcached.org/serverguide/configuring/
  - https://docs.memcached.org/serverguide/maintenance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Check `memcached -h` or `man memcached` for current options; defaults are meant to be sensible. On first setup look at -m, -d and -v.

- `-m <MB>`: RAM for item storage. It is not a global limit: memcached uses a little more than you set. Values under 64 MB may still use up to 64 MB.
- `-d`: daemonize. Skip it under an init system; when learning, run in the foreground.
- `-v`: verbosity to stdout/stderr. One `-v` prints startup info; more (`-vv`, `-vvv`) print increasingly detailed request info, handy to watch what a test script really sends. `-vv` also prints the slab class table.

Example: `memcached -m 1024 -v`.

Verify the flag took (init scripts are sometimes misconfigured and start with defaults): run `stats` and compare `limit_maxbytes` with your -m value in bytes.

If installed from a package, look for its alternate config path (for example /etc/sysconfig/memcached) before editing init scripts.

## Checked

Confirmed 2026-11-09: -m in megabytes and not a global limit, values under 64 MB may still use 64 MB, -d daemonize, -v levels, `memcached -h` and `man memcached`, package init scripts and /etc/sysconfig/memcached (Configuring page); `limit_maxbytes` verifies the -m flag took (Maintenance page); `-vv` prints the slab class table (Performance page). Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Configuring, Maintenance and Performance pages
