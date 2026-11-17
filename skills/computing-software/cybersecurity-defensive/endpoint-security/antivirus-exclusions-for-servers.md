---
id: computing-software.cybersecurity-defensive.endpoint-security.antivirus-exclusions-for-servers
name: antivirus-exclusions-for-servers
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [antimalware, av-exclusions, defender-exclusions, sql-server, exchange-server, domain-controllers, exclusion-review, exclusions]
level: practitioner
status: draft
description: "Set antivirus exclusions for servers without opening holes: vendor-documented lists (SQL, Exchange, DCs, Hyper-V), automatic server-role exclusions, scoping, auditing and abuse."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/configure-server-exclusions-microsoft-defender-antivirus", "https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/security/antivirus-and-sql-server", "https://learn.microsoft.com/en-us/exchange/antispam-and-antimalware/windows-antivirus-software"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Antivirus exclusions for servers

Exclusions exist for performance and stability (databases, mail stores, virtualisation). Attackers
look for them: excluded folders are where they drop tools. Every exclusion is a documented trade-off.

## Use vendor lists, not folklore
- **Defender on Windows Server 2016+**: automatic exclusions for server roles (DCs, DNS, DHCP, Hyper-V,
  File Server, IIS...) apply automatically and do not appear in the exclusion list. Do not re-add them.
- **SQL Server**: data/log file extensions (`.mdf`, `.ldf`, `.ndf`) or their directories, backup
  directories, FILESTREAM, full-text catalogs per Microsoft's SQL antivirus article; plus process
  exclusions for `sqlservr.exe` only where the doc says so.
- **Exchange**: databases, transaction logs, queue folders, specific processes per the Exchange
  version's documented list.
- **Hyper-V/cluster**: VM configuration and VHDX directories, CSV paths per doc.
- **Domain controllers**: NTDS database and logs, SYSVOL staging (automatic on 2016+).

## Scope narrowly
- Prefer file extensions in specific paths over whole drives; avoid wildcards like `*\temp\*`.
- **Process exclusions** exclude everything that process opens: dangerous for interpreters or
  generic hosts (`powershell.exe`, `java.exe`, `w3wp.exe`, `node.exe`). Never.
- Defender: contextual exclusions (path + process + file type) where supported reduce scope.
- Apply via Intune/GPO per server role group, not via local settings.

## Prevent tampering and discovery
- Defender: "Disable local admin merge" so local admins cannot add exclusions; tamper protection with
  exclusions protection.
- Hide exclusions from non-admins (`HideExclusionsFromLocalUsers`, default on newer builds).
- Alert on exclusion changes: Defender event 5007 (configuration changed) with `Exclusions` in the
  path; advanced hunting `DeviceRegistryEvents` on `...\Windows Defender\Exclusions`.

## Review
Quarterly: export exclusions per device group (`Get-MpPreference | select Exclusion*`), check each
against the vendor list and owner justification; remove leftovers from old apps.

## Gotchas
- Exclusions from one AV product copied into another product with different semantics.
- Excluding backup software paths that attackers also use for staging.
- EDR telemetry is usually unaffected by AV exclusions, but some products also skip behavioural
  monitoring for excluded processes; check vendor docs.

## Verify
Drop the EICAR test file into a non-excluded path (detected) and confirm exclusion lists on servers
match the approved baseline; attempting to add a local exclusion as admin fails with tamper protection on.
