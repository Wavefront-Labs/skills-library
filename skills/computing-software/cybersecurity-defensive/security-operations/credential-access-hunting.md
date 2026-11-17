---
id: computing-software.cybersecurity-defensive.security-operations.credential-access-hunting
name: credential-access-hunting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, credential-access-hunting, lsass-access, sysmon-event-10, ntds-dit, sam-dump, browser-credential-theft, t1003]
level: advanced
status: draft
description: "Hunt credential theft on endpoints: LSASS access and dumps, SAM/SECURITY hive saves, NTDS.dit extraction, DCSync, browser credential stores and cloud token theft."
sources: ["https://attack.mitre.org/techniques/T1003/", "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon", "https://www.microsoft.com/en-us/security/blog/2022/10/05/detecting-and-preventing-lsass-credential-dumping-attacks/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Credential access hunting

## LSASS (T1003.001)
- Sysmon 10 (ProcessAccess) with `TargetImage` lsass.exe and suspicious `GrantedAccess`
  (`0x1010`, `0x1410`, `0x1438`, `0x143a`, `0x1fffff`) from unexpected sources.
  Baseline the legitimate accessors (AV/EDR, `MsMpEng.exe`, `csrss.exe`, `wininit.exe`).
- Dump tools by command line: `comsvcs.dll, MiniDump` via rundll32, `procdump -ma lsass`,
  `taskmgr` create dump file (`lsass.DMP` in Temp), `nanodump`, `sqldumper.exe`.
- File creation of `*.dmp` by non-debugging processes.
```kql
DeviceProcessEvents
| where ProcessCommandLine has_any ("comsvcs","MiniDump","lsass") and ProcessCommandLine has_any ("dump","#24","full")
```

## SAM, SECURITY, SYSTEM hives (T1003.002)
`reg save HKLM\SAM`, `reg save HKLM\SECURITY`, shadow copy access
(`\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy`), or `esentutl /y /vss`.

## NTDS.dit (T1003.003)
On DCs: `ntdsutil "ac i ntds" "ifm" "create full"`, `vssadmin create shadow /for=C:`, copy of
`ntds.dit` from shadow copies; 8222/7036 shadow copy service events; large file writes in odd paths.

## DCSync (T1003.006)
4662 on the domain object with properties `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` /
`1131f6ad-...` (Replicating Directory Changes / All) by an account that is not a DC computer
account. Defender for Identity alerts on this natively.

## Browser and application stores (T1555)
Non-browser processes reading `Login Data`, `Cookies`, `Local State` under browser profiles;
infostealers do exactly this. Also `vaultcmd`, `cmdkey /list`, KeePass config tampering.

## Cloud tokens
Processes reading Office/Teams token caches, `TokenBroker` folders, or `.azure`/`.aws` credential
files; follow with identity logs for token reuse from new IPs.

## Hunt approach
Stack accessors of LSASS and readers of credential files by process path and signer across the
fleet; one-offs are leads. Check whether LSA protection (RunAsPPL) and Credential Guard are on
where hits occur: if not, prioritise hardening.

## Gotchas
- Sysmon config must include lsass ProcessAccess with a sensible filter, or there is no data.
- EDR blocks often show as alerts only; hunt for attempted (blocked) dumping too: it reveals the
  intruder even when it failed.

## Verify
In a lab, run comsvcs MiniDump against lsass and a `reg save` of SAM; each query should return the test.
