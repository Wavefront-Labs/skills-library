---
id: computing-software.cybersecurity-defensive.suricata.pcap-file-replay
name: pcap-file-replay
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [pcap-replay, offline-mode, read-pcap, pcap-file]
level: practitioner
status: docs-checked
description: "Replay pcap files offline with -r: directories, continuous mode, recursion, delete-when-done and buffer options."
sources: ["https://docs.suricata.io/en/latest/command-line-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Replaying pcap files

`suricata -r <path>` processes pcap files offline.

- A directory is processed in order of modification time; flow state carries across files.
- `--pcap-file-continuous`: keep running and pick up new files added to the directory.
- `--pcap-file-recursive`: walk subdirectories to a depth of 255. Cannot combine with continuous; symlinks are skipped.
- `--pcap-file-delete`: delete each file after processing; overrides `pcap-file.delete-when-done`.
- `delete-when-done` in the config accepts `false` (default), `true`, or `"non-alerts"` (delete only files that produced no alerts).
- `--pcap-file-buffer-size <value>`: `setvbuf` size on Linux only; 0 or 4 KiB to 64 MiB, default 128 KiB.
- `--pcap-buffer-size=<size>`: 0 to 2147483647.
- `--erf-in=<file>`: replay an Endace ERF file.

Use `-l` to choose where the logs of the run go.

## Checked

2026-11-04. Every option and limit above confirmed against the Suricata Command Line Options page.

Method: documentation only; no commands were run.
