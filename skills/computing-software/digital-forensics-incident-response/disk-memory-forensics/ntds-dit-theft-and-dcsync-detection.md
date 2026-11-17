---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.ntds-dit-theft-and-dcsync-detection
name: ntds-dit-theft-and-dcsync-detection
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [dcsync, ntds-dit, credential-theft, 4662, active-directory, vssadmin, dfir]
level: advanced
status: draft
description: "Detect NTDS.dit theft (ntdsutil IFM, VSS copy) and DCSync replication abuse from 4662 GUIDs, directory service events, network RPC and file artefacts on DCs."
sources: ["https://attack.mitre.org/techniques/T1003/003/", "https://attack.mitre.org/techniques/T1003/006/", "https://adsecurity.org/?p=1729"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NTDS.dit theft and DCSync detection

**Goal:** determine whether the attacker obtained all domain password hashes, which forces
domain-wide credential reset.

## DCSync (T1003.006)
- DC Security **4662** (operation performed on an object) on the domain naming context with
  properties containing replication rights GUIDs:
  `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` (DS-Replication-Get-Changes),
  `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` (Get-Changes-All),
  `89e95b76-444d-4c62-991a-0facbeda640c` (Get-Changes-In-Filtered-Set),
  by an account that is **not a domain controller computer account**. Requires "Audit
  Directory Service Access" with appropriate SACL.
- Network: DRSUAPI `DRSGetNCChanges` RPC from non-DC IPs (Zeek `dce_rpc.log`, NDR/MDI alert).
- Source host: Mimikatz `lsadump::dcsync`, Impacket `secretsdump.py -just-dc`.
- Check who holds replication rights: attackers grant them to a normal account for
  persistence (`Get-Acl "AD:DC=contoso,DC=com"` / 5136 ACL change events).

## NTDS.dit file theft (T1003.003)
- `ntdsutil "ac i ntds" "ifm" "create full \temp\x" q q` -> Application log ESENT events
  (325, 326, 327, 216) and ntdsutil Prefetch/4688.
- Volume Shadow Copy: `vssadmin create shadow /for=C:` then copy
  `\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyN\Windows\NTDS\ntds.dit` and `SYSTEM` hive
  (System 7036 VSS service, 8222 shadow created, 4688 command lines).
- Also `diskshadow`, `esentutl /y /vss`, raw NTFS readers; look for ntds.dit copies and large
  archives in staging paths and their exfiltration.

## Response
All domain hashes compromised: reset every user and service account, KRBTGT twice, computer
accounts as feasible, trust passwords; consider forest recovery if persistence is deep.

## Verify
Show the event or file evidence with time and account, and the list of replication-right
holders after remediation contains only DCs and approved accounts.
