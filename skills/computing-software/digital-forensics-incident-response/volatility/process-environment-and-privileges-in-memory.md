---
id: computing-software.digital-forensics-incident-response.volatility.process-environment-and-privileges-in-memory
name: process-environment-and-privileges-in-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [envars, privileges-plugin, volatility3, cmdline, process-environment, token-privileges, memory-forensics, dfir, getsids]
level: practitioner
status: docs-checked
description: "Read process command lines, environment variables and token privileges from a Windows memory image with Volatility 3 to spot abuse and staging."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.html", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Process command lines, environment variables and privileges in memory

**Goal:** for each suspicious process, recover how it was launched, what environment it ran
with, and which token privileges it held/enabled. These answer "what was it told to do" and
"what could it do" without touching the live host.

## Commands (Volatility 3)
```bash
vol -f mem.raw windows.cmdline                 # full command line from each PEB
vol -f mem.raw windows.cmdline --pid 4312
vol -f mem.raw windows.envars --pid 4312        # environment block (PEB->ProcessParameters->Environment), plus registry-persistent variables
vol -f mem.raw windows.envars --silent          # suppress common and non-persistent variables
vol -f mem.raw windows.privileges --pid 4312    # token privileges with Present/Enabled/Default flags
vol -f mem.raw windows.getsids --pid 4312       # owning user and group SIDs
vol -r csv -f mem.raw windows.privileges > privs.csv
```

## What to look for
- **cmdline:** encoded PowerShell (`-enc`, `-e`, `FromBase64String`), `rundll32` with an odd
  export or no args, `regsvr32 /i:http`, LOLBins pointing at user-writable paths, tool
  arguments (`sekurlsa::`, `-ma lsass`), a process whose command line path differs from its
  image path (hollowing, masquerading). Empty cmdline for a user process is itself a finding
  (paged-out PEB or a tampered PEB).
- **envars:** `COMPUTERNAME`/`USERNAME` revealing the session behind a process, odd
  `PATH` prepends (search-order hijack), `__COMPAT_LAYER=RunAsInvoker` (UAC bypass),
  `COR_ENABLE_PROFILING`/`COR_PROFILER` (.NET profiler hijack), `PSModulePath` changes,
  attacker-set variables used to pass payloads (`set x=...` then `%x%`).
- **privileges:** a user-launched process with **enabled** `SeDebugPrivilege` (credential
  dumping), `SeImpersonatePrivilege` abused by potato-style escalation from service
  accounts, `SeBackupPrivilege`/`SeRestorePrivilege` (hive/NTDS theft), `SeLoadDriverPrivilege`
  (BYOVD), `SeTcbPrivilege` in non-SYSTEM processes. *Present* is normal for admins; the
  *Enabled* column shows what was actually switched on (AdjustTokenPrivileges).

## Gotchas
- The PEB lives in user space; if it was paged out the plugins return nothing or partial data.
  Absence is not proof; corroborate with Sysmon 1/4688 or EDR telemetry.
- Malware can overwrite its own PEB command line after start; compare against `windows.pstree`
  parent and EDR process-creation records captured at launch time.

## Self-check
For each process you flag, can you state the launching command, the user SID and any enabled
dangerous privilege, and have you corroborated at least one with a log source?

## Checked

- Confirmed: plugin names and --pid/--silent options; privileges reports Present/Enabled/Default attributes; envars also reads registry-persistent variables.

Method: docs-checked 2026-11-09 against volatility3 develop source: plugins windows/cmdline.py, envars.py, privileges.py, getsids.py and the cli options. Dropped the unverified Volatility 2 equivalence line. The attacker-technique heuristics (LOLBin, privilege abuse, env-var tricks) are practitioner guidance, not sourced from the cited pages.
