---
id: computing-software.networking-hardware-and-wireless.unbound.running-the-unbound-daemon
name: running-the-unbound-daemon
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, daemon, command-line, debug-mode, pidfile]
level: intro
status: draft
description: "Start the unbound daemon and use its command-line options: config file, foreground debug, verbosity, no pidfile and version."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# running the unbound daemon
Synopsis: `unbound [-hdpVv] [-c <cfgfile>]`.

- `-c <cfgfile>` reads settings from that file instead of the default `/usr/local/etc/unbound/unbound.conf`.
- `-d` is debug mode: stay in the foreground instead of forking. Log output to a log file or syslog is delayed until thread-spawn time, so early config and setup errors show on stderr. Giving `-d` twice or more keeps all log messages on stderr.
- `-v` increases verbosity, in addition to any verbosity in the config file; repeat for more detail.
- `-p` runs without a pidfile; intended only for supervision systems that guarantee a single running instance.
- `-V` shows the version and build options, then exits.
- `-h` shows help.

Unbound is a caching resolver with built-in root hints: it starts at the root, follows delegations to the authoritative servers, and caches answers for their TTL. It can perform DNSSEC validation. To use a local instance, point resolv.conf at 127.0.0.1.

Running NSD on the same machine needs careful setup because both use port 53.
