---
id: computing-software.cybersecurity-defensive.suricata.runmodes
name: runmodes
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [runmode, workers, autofp, autofp-scheduler]
level: practitioner
status: docs-checked
description: "Choose a runmode: workers, autofp and single, what each does, and the autofp scheduler options hash, ippair and ftp-hash."
sources: ["https://docs.suricata.io/en/latest/performance/runmodes.html", "https://docs.suricata.io/en/latest/command-line-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Runmodes

A runmode arranges threads, thread-modules and queues. List them with `--list-runmodes`; set with `runmode:` or `--runmode`.

- `workers`: generally best. The NIC or driver balances packets and each thread runs the full pipeline.
- `autofp`: used for pcap files and some IPS setups such as NFQ. Capture threads decode and pass packets to flow worker threads.
- `single`: like workers but one thread; mostly for development.

## autofp-scheduler
- `hash` (default): 5 to 7-tuple hash, the same used to store flows.
- `ippair`: IP addresses only.
- `ftp-hash`: like hash but groups FTP and FTP-data flows on one thread.

Unix socket `running-mode` reports workers, autofp or simple.

## Checked

2026-11-04. Every point above confirmed against the Runmodes page, Command Line Options (`--runmode`, `--list-runmodes`), the suricata.yaml sample (`runmode: autofp`) and the Unix Socket page.

Method: documentation only; no commands were run.
