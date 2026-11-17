---
id: computing-software.systems-network-administration.active-directory.install-from-media-ifm
name: install-from-media-ifm
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-ds, install-from-media, ntdsutil-ifm, ifm, domain-controller-deployment, branch-office, rodc, installationmediapath, sysvol]
level: practitioner
status: docs-checked
description: "Promote a DC from IFM media made with ntdsutil so the initial directory copy comes off local disk, not across a slow WAN; media types and handling."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc732530(v=ws.10)
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-a-replica-windows-server-2012-domain-controller-in-an-existing-domain--level-200-
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/install-addsdomaincontroller
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install from media (IFM)

**Goal:** promote a DC at a remote site without pulling the full NTDS.dit over the WAN.

## Create the media on an existing DC
Run on a healthy DC of the same domain. Set the active instance first (`activate instance ntds`), then:
```cmd
ntdsutil "activate instance ntds" ifm "create sysvol full <DATA_DRIVE>:\IFM" quit quit
```
- `create full` = writable DC media (database and registry); `create sysvol full` also includes SYSVOL so the new DC
  can use it as a replication source; `create rodc` / `create sysvol rodc` make RODC media with cached secrets such as
  passwords removed.
- Writable DC media can only be made on a writable DC. You can make RODC media on a writable DC or on another RODC.
- The tool needs free space in `%TMP%` of at least 110% of the database size; redirect `%TMP%` to a bigger disk if
  needed.
- Writable media is a full copy of the directory, so treat it like a DC backup: encrypt it in transit and delete it
  after use. Media can be protected with a SYSKEY; the install prompts for the password.

## Promote using the media
Copy the IFM folder to the target server, then:
```powershell
Install-ADDSDomainController -DomainName ad.example.com -SiteName BRANCH01 `
  -InstallationMediaPath '<DATA_DRIVE>:\IFM' -InstallDns -Credential (Get-Credential) `
  -SafeModeAdministratorPassword (Read-Host -AsSecureString 'DSRM') -Force
```
`-InstallationMediaPath` takes the media location; the wizard has a Verify step for it. If the media uses a SYSKEY
you also supply it (`-SystemKey`). Promotion still replicates changes made since the media was created, so make media
shortly before use.

## Limits and gotchas
- Make the media on a DC running a Windows Server version the target can use: the Windows Server 2012 install page
  says media made on Windows Server 2008 R2 or earlier cannot be used for a 2012 DC (confirm the rule for newer
  releases).
- Without SYSVOL in the media, SYSVOL has to replicate from a partner after promotion; the DC does not share SYSVOL
  until DFSR initial sync completes (events 4614, then 4604).

## Verify
- [ ] `repadmin /showrepl` on the new DC: all partitions succeed.
- [ ] SYSVOL and NETLOGON shared after initial sync.
- [ ] Media copies destroyed and the transfer device wiped.

## Checked

Date: 2026-10-27. Documentation: ntdsutil `ifm` subcommand reference (Windows Server 2008 / 2008 R2 archive page; no
current-release page was readable), the Windows Server 2012 replica DC install page, Install-ADDSDomainController
(Windows Server 2025 module page), Microsoft Support DFSR and backup-latency articles.
Confirmed: the four `ifm create` forms and what each includes, writable-vs-RODC source rules, 110% `%TMP%` space
requirement, SYSKEY handling, `-InstallationMediaPath` and `-SystemKey` parameters, 2008 R2-to-2012 media restriction,
DFSR events 4614/4604.
Removed unconfirmed claims: "password hashes unless RODC", the "same domain only" and "drive letters need not match"
statements, the tombstone-lifetime and few-days freshness rules for media, `dcpromo.log` as the proof of media use and
the ntdsutil output-folder name.

Method: documentation only; no commands were run.
