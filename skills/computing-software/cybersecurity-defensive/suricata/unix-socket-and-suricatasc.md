---
id: computing-software.cybersecurity-defensive.suricata.unix-socket-and-suricatasc
name: unix-socket-and-suricatasc
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [unix-socket, suricatasc, runtime-commands, pcap-processing-mode]
level: practitioner
status: docs-checked
description: "Control a running Suricata with suricatasc: enabling the unix socket, common commands, memcap changes and pcap-file queue mode."
sources: ["https://docs.suricata.io/en/latest/unix-socket.html", "https://docs.suricata.io/en/latest/command-line-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unix socket and suricatasc

Enabled by default under `unix-command` (`enabled` yes or auto, optional `filename`). `--unix-socket=<file>` overrides.

`suricatasc` runs interactively or as `suricatasc -c "<command>"`.

## Common commands
`shutdown`, `reload-rules`, `ruleset-reload-nonblocking`, `ruleset-stats`, `iface-list`, `iface-stat <if>`, `dump-counters`, `version`, `uptime`, `running-mode`, `capture-mode`, `conf-get`, `memcap-set`/`memcap-show`/`memcap-list`, `reopen-log-files` (after external rotation), tenant and hostbit commands, `get-flow-stats-by-id`, `command-list`.

## pcap-file mode
Start with `--unix-socket`, then `pcap-file <input> <output-dir>` (use absolute paths), `pcap-file-continuous`, `pcap-file-number`, `pcap-file-list`, `pcap-current`, `pcap-last-processed`, `pcap-interrupt`. Files run sequentially, avoiding signature reload per file.

Custom clients speak JSON, starting with `{"version": "0.1"}`; messages may arrive in partial reads.

## Checked

2026-11-04. Every command, mode and protocol detail above confirmed against the Interacting via Unix Socket page; `--unix-socket` against Command Line Options.

Method: documentation only; no commands were run.
