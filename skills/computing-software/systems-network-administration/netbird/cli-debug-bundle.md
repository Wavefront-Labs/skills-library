---
id: computing-software.systems-network-administration.netbird.cli-debug-bundle
name: cli-debug-bundle
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, debug-bundle, trace-logging, packet-trace, log-level]
level: practitioner
status: docs-checked
description: "Collect NetBird diagnostics: debug bundle ZIP with anonymize and upload options, timed trace logging, runtime log level change and firewall packet tracing."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`netbird debug` subcommands:

- `bundle`: create a diagnostic ZIP and print its path. Flags: `-A, --anonymize`, `-S, --system-info` (default true), `-U, --upload-bundle`, `-C, --log-file-count` (rotated logs to include, default 1), `--upload-bundle-url`, `--upload-bundle-insecure` (self-hosted http or untrusted-TLS upload server; needs root or administrator).
- `for <time>`: set trace logging, run for the duration (for example `5m`), then create a bundle; same flags as `bundle`. Useful for capturing logs over a period when the issue occurs.
- `log level <level>`: change the daemon log level for the current session only (reverts on daemon restart). Levels: `panic`, `fatal`, `error`, `warn`, `info`, `debug`, `trace`.
- `trace <direction> <source-ip> <dest-ip>`: trace a packet through the firewall rules. `self` stands for the local peer IP. Flags: `-p, --protocol` (`tcp`, `udp`, `icmp`; default tcp), `--sport`, `--dport`, `--icmp-type`, `--icmp-code`, TCP flags `--syn --ack --fin --rst --psh --urg`.

The bundle is written in the daemon's temporary directory (for example `/tmp/netbird.debug.<number>.zip` on Linux and macOS) and is owned by the daemon account, so reading it may need elevated permissions. The local ZIP is created even with `--upload-bundle`, which additionally prints an upload key to share with the NetBird team.

`-A` anonymizes IP addresses and non-netbird.io domains in the output.

On Linux the userspace packet filter is only active when the kernel firewall backend is unavailable, so `debug trace` is mainly useful on macOS and Windows.

## Checked

2026-11-04: read the CLI page (get-started/cli) debug sections in full. Confirmed subcommands, flags and defaults, output location, upload behaviour, log levels and the Linux trace note. Removed the invented "support case" workflow (the 2m duration and attach-the-ZIP steps are not on the page) and the unstated claim that trace answers policy questions in general.

Method: documentation only; no commands were run.
