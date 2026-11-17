---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.detecting-sam-and-security-hive-dumping-with-reg-save
name: detecting-sam-and-security-hive-dumping-with-reg-save
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [reg-save-hives, credential-theft, sam-dumping, lsa-secrets, windows-forensics, dfir]
level: practitioner
status: docs-checked
description: "Detect SAM, SECURITY and SYSTEM hive dumping with reg save or shadow copies (T1003.002, T1003.004): what the command does, where secrets live, and impact assessment."
sources: ["https://attack.mitre.org/techniques/T1003/002/", "https://attack.mitre.org/techniques/T1003/004/", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg-save"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting SAM and SECURITY hive dumping with reg save

Adversaries extract credential material from the Security Account Manager (SAM), which holds the host's local accounts (T1003.002), and from LSA secrets (T1003.004), which can contain service account credentials and are stored under `HKEY_LOCAL_MACHINE\SECURITY\Policy\Secrets`. ATT&CK documents `reg save` as a way to copy the hives from the registry, then processing them offline.

## What the tool does
- `reg save <keyname> <filename> [/y]` writes the specified subkey to a file; `/y` overwrites without prompting; a remote computer can be named in the key path, and then only HKLM and HKU are valid roots. Return value 0 is success, 1 failure.
- ATT&CK examples: `reg save HKLM\sam sam` and `reg save HKLM\system system`; real campaigns it cites also save `hklm\security`, sometimes as `.hiv` files (Operation CuckooBees, APT28 Nearest Neighbor).
- ATT&CK notes the SAM extraction needs SYSTEM-level access for enumeration, and that Creddump7 can process saved SAM and SYSTEM hives locally.
- Other routes named by ATT&CK: in-memory tools (Mimikatz, secretsdump.py, gsecdump, pwdump variants), and copying hives out of volume shadow copies (APT41 and MirrorFace with `vssadmin`).

## Evidence to look for
- Process creation with command lines (event 4688 with command line, Sysmon, EDR): `reg.exe` with `save` and a SAM, SECURITY or SYSTEM key; `vssadmin` use near hive copies.
- File creation and deletion of the output file (MFT, USN journal) in temp, public or user paths.
- Remote use of secretsdump (Impacket): check how the hives were read and what artefacts the source host holds; see the skill `computing-software.digital-forensics-incident-response.disk-memory-forensics.impacket-execution-footprints`.
- Sigma maintains community rules for process creation (the repository folder is cited in sources); take rule logic from there rather than from this skill.

## Impact assessment
- Local account hashes from the SAM: treat reused local administrator passwords across hosts as exposed. ATT&CK notes RID 500 is the built-in administrator, RID 501 the guest, and user accounts start at RID 1000.
- LSA secrets: rotate service account credentials stored on the host.
- ATT&CK mitigation: consider disabling or restricting NTLM.

## Gotchas
- Backup and imaging tools legitimately save hives; baseline by parent process and destination.
- Attackers can rename tools; do not rely on file name alone.

## Verify
For each dump event: account used, the files created and their fate (deleted, exfiltrated), and the credentials considered exposed with rotation tracked.

## Checked
2026-11-08. Confirmed against ATT&CK T1003.002 and T1003.004 and Microsoft Learn `reg save`: command syntax, /y, return values, remote root keys, example commands, LSA secrets registry path, RID notes, shadow copy and vssadmin examples, NTLM mitigation. Removed as unconfirmed: file-size figures, event IDs for registry auditing and VSS, RemoteRegistry/pipe details, the KQL query, and OriginalFileName advice.
Method: documentation only; no commands were run.
