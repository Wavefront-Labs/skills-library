---
id: computing-software.digital-forensics-incident-response.log-analysis.sysmon-process-and-image-load-events
name: sysmon-process-and-image-load-events
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sysmon-process-events, sysmon, process-creation, image-load, process-access, dfir]
level: practitioner
status: docs-checked
description: "Investigate with Sysmon process events: Event 1 process creation, ProcessGuid linking, Event 7 image loads, Event 8 remote threads and Event 10 access."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysmon process and image load events

**Goal:** reconstruct execution chains and spot injection and credential access from Sysmon.
Run `sysmon -s` to print the schema with the exact field names for your Sysmon version.

## Event 1: process creation
Extended information about a newly created process, including the full command line for the
current and parent processes. The `ProcessGUID` is a unique value for the process across a
domain, so you can correlate events even when Windows reuses process IDs; each event also
carries a session GUID to correlate events in the same logon session. Hashes are full-file
hashes using the algorithms in the HashType field (SHA1 is the default; MD5, SHA256 and
IMPHASH can also be configured, several at once).
- Build process trees from the GUIDs, not PIDs.
- Event 5 (process terminated) gives UtcTime, ProcessGuid and ProcessId, so you can measure
  a process lifetime.

## Event 7: image loaded
Logs when a module is loaded in a specific process, with hashes and signature information.
Disabled by default and enabled with the `-l` option or an `ImageLoad` filter. The signature
is created asynchronously and indicates if the file was removed after loading. Monitoring all
image loads generates a significant amount of logging, so configure it carefully.

## Event 8: CreateRemoteThread
Detects a process creating a thread in another process, a technique used by malware to inject
code and hide. It shows source and target process and, for the new thread, StartAddress,
StartModule and StartFunction. StartModule and StartFunction are inferred and may be empty if
the start address is outside loaded modules or known exported functions.

## Event 10: ProcessAccess
Reports when a process opens another, often followed by queries or reading and writing the
target's memory; it enables detection of tools that read LSASS memory to steal credentials.
Enable it only with filters that remove expected accesses (see the sysmon-processaccess-event-10
skill).

## Self-check
Execution chains are built from GUIDs; any injection or credential-access finding names the
source process, target process, time (UTC) and the config rules that were active.

## Checked
2026-11-09. Confirmed on the Sysmon page (read in full): Events 1, 5, 7, 8, 10 descriptions, ProcessGUID/session GUID, hash algorithms and default, ImageLoad disabled by default and -l, asynchronous signature, StartModule/StartFunction caveat. Removed: OriginalFileName, LogonId, IntegrityLevel and other field lists, renamed-tool examples, DLL side-loading and execute-assembly hunts, GrantedAccess masks, CallTrace UNKNOWN claim, KQL queries, procdump lab test, the SANS poster source (not readable).
Method: documentation only; no commands were run.
