---
id: computing-software.digital-forensics-incident-response.volatility.cross-view-hidden-process-detection
name: cross-view-hidden-process-detection
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [psxview, rootkit, dkom, pslist, psscan, volatility3, dfir]
level: advanced
status: docs-checked
description: "Find hidden processes by cross-viewing process sources (pslist, psscan, thrdscan, sessions, handles, csrss) and interpreting differences safely."
sources: ["https://volatility3.readthedocs.io/en/latest/", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cross-view hidden process detection

**Goal:** rootkits using DKOM unlink their `_EPROCESS` from the active process list, so `pslist`
(and Task Manager) do not show them. Other data structures still reference the process.

## Sources to compare
| Source | Volatility 3 plugin | How a process appears |
|---|---|---|
| ActiveProcessLinks list | `windows.pslist` | Linked list walk |
| Pool tag scan for `Proc` | `windows.psscan` | Finds terminated and unlinked EPROCESS structures |
| Thread scan | `windows.thrdscan` | Threads point to their owning process |
| Session info | `windows.sessions` | Processes with session details taken from environment variables (cross-check only) |
| Handle tables | `windows.handles` | Processes with handles to the target |
| csrss handles | handles of csrss.exe | Every Win32 process has a csrss handle |
| psxview-style comparison | `windows.malware.psxview` (newer releases) | Lists processes found by four of the methods in The Art of Memory Forensics |

```bash
vol -f mem.raw windows.pslist > pslist.txt
vol -f mem.raw windows.psscan > psscan.txt
# diff by offset/PID
comm -13 <(awk '{print $1}' pslist.txt | sort) <(awk '{print $1}' psscan.txt | sort)
```

## Interpreting differences
- In psscan but not pslist **with an exit time**: terminated process (normal) - still useful history.
- In psscan but not pslist, **no exit time, threads alive** (thrdscan shows active threads): hidden process -> strong rootkit indicator.
- In pslist but not psscan: pool header tampering or paged structures; less common.

## Follow-up
- Dump the hidden process (`windows.pslist --pid` will not work; use `windows.psscan --dump` or memmap by offset), check its image path, handles, network (netscan owner PIDs).
- Look for the driver responsible: `windows.modscan` vs `windows.modules`, callbacks, SSDT.

## Gotchas
- Memory smear in live acquisitions creates phantom differences; confirm with threads and handles before concluding.
- Short-lived processes captured mid-creation/termination look odd; check create/exit times.

## Verify
A hidden process claim is supported by at least two independent structures (threads, handles, sessions).

## Checked

- Confirmed: psscan pool-tag scan for Proc, psscan has --dump, thrdscan and psxview exist; psxview covers four methods from The Art of Memory Forensics.

Method: docs-checked 2026-11-09 against volatility3 develop source plugins/windows/{pslist,psscan,thrdscan,sessions,handles,malware/psxview}.py (the Wiley book page was dropped as a source, not read). Corrected the sessions row (session info from environment variables, not per-session process lists) and psxview description. The interpretation rules for psscan vs pslist differences are practitioner guidance.
