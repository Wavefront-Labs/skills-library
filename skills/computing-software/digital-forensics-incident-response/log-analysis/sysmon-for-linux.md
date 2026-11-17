---
id: computing-software.digital-forensics-incident-response.log-analysis.sysmon-for-linux
name: sysmon-for-linux
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sysmon-for-linux, sysmon, linux-logging, ebpf, dfir]
level: practitioner
status: docs-checked
description: "Deploy and read Sysmon for Linux: package install, BTF kernel offsets, events written to syslog, sysmonLogView, and syslog size limits and FieldSizes."
sources: ["https://github.com/microsoft/SysmonForLinux"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysmon for Linux

Sysmon for Linux monitors and logs system activity including process lifetime, network connections and
file system writes. It works across reboots, uses advanced filtering, and is part of Sysinternals. It depends
on SysinternalsEBPF and ships eBPF programs. Events follow the Sysmon model, so Windows Sysmon habits carry over.

## Install
Packages are in the official Microsoft Linux repositories; the project's Installation instructions list the
steps per distribution. Do not build from source unless you must (see its BUILD instructions).

## Kernel offsets
- On BTF-enabled systems Sysmon uses BTF for accurate kernel offsets; standalone BTF files can be given with
  the `/BTF` switch (BTFHub has files for many distributions and kernels).
- Without BTF it tries to discover offsets of some kernel struct members automatically. If that fails, report
  the kernel version and error to the project's GitHub issues, or override discovery with a configuration file
  built from the getOffsets module (see the README in that directory).

## Reading events
- Output goes to syslog: `sudo tail -f /var/log/syslog`, or more readable by piping into `/opt/sysmon/sysmonLogView`,
  which has options to filter by event and to reduce fields. It is installed into `/opt/sysmon` with Sysmon.
- Syslogger defaults are often between 1KB and 8KB, so large events (for example over 64KB) may need the
  syslog configuration changed. Alternatively limit field lengths with `<FieldSizes>` under `<Sysmon>` in the
  configuration, for example `<FieldSizes>CommandLine:100,Image:20</FieldSizes>`.
- A man page ships in the package directory with both deb and rpm packages.

## Investigation value
Process creation and network events with the process image let you reconstruct how an intruder or malware
operates; forward the syslog lines to your SIEM and parse the XML there.

## Checked
2026-11-01. Confirmed against the SysmonForLinux README (what it logs, Sysinternals, SysinternalsEBPF, package repositories, BTF and offset discovery, `/BTF`, syslog output, sysmonLogView, large-event and `FieldSizes` guidance, man page).
Removed: the install and config command lines, the supported-event-ID list, journalctl and rsyslog forwarding, SIEM parser claims, kernel version minimums, and the reverse-shell example detections, because the page read does not state them.
Method: documentation only; no commands were run.
