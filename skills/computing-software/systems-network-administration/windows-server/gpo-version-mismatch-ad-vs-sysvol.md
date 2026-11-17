---
id: computing-software.systems-network-administration.windows-server.gpo-version-mismatch-ad-vs-sysvol
name: gpo-version-mismatch-ad-vs-sysvol
category: computing-software
field: systems-network-administration
product: windows-server
tags: [group-policy, gpo, gpo-version-mismatch, sysvol, gpotool]
level: advanced
status: gated
description: "Detect and fix GPOs whose AD (GPC) and SYSVOL (GPT) versions disagree across DCs, the usual cause of settings applying on some sites only."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/applying-group-policy-troubleshooting-guidance
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/force-authoritative-non-authoritative-synchronization
  - https://learn.microsoft.com/en-us/powershell/module/grouppolicy/restore-gpo
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# GPO version mismatch between AD and SYSVOL

A GPO has two halves: the Group Policy Container in AD (`CN={GUID},CN=Policies,CN=System`, attribute `versionNumber`) (gated: unconfirmed, source is paywalled or blocked) and
the Group Policy Template folder in SYSVOL, which holds `gpt.ini` (path `\\<dcName>\SYSVOL\<domain>\Policies\<guid>\gpt.ini`).
The `Version=` line inside it is the SYSVOL-side version number (gated: unconfirmed, source is paywalled or blocked). Clients can skip a GPO when the halves disagree or
when the DC they query has stale SYSVOL (gated: unconfirmed, source is paywalled or blocked).
The container and template details are specified in the Group Policy protocol documents, which are not in a public
repository; the Group Policy troubleshooting guide only confirms that the template (gpt.ini) must be readable over the network.

## Detect on every DC
```powershell
$dcs = (Get-ADDomainController -Filter *).HostName
foreach ($gpo in Get-GPO -All) {
  foreach ($dc in $dcs) {
    $ad  = (Get-ADObject "CN={$($gpo.Id)},CN=Policies,CN=System,$((Get-ADDomain).DistinguishedName)" -Server $dc -Properties versionNumber).versionNumber
    $ini = Get-Content "\\$dc\SYSVOL\$((Get-ADDomain).DNSRoot)\Policies\{$($gpo.Id)}\GPT.INI" -ErrorAction SilentlyContinue |
           Select-String '^Version=(\d+)' | ForEach-Object { [int]$_.Matches[0].Groups[1].Value }
    if ($ad -ne $ini) { [pscustomobject]@{GPO=$gpo.DisplayName;DC=$dc;AD=$ad;SYSVOL=$ini} }
  }
}
```
GPMC also shows AD and SYSVOL versions on a GPO's Details tab and has a Status tab that reports across DCs (gated: unconfirmed, source is paywalled or blocked).

## Read the numbers
`versionNumber` combines a user version and a computer version (`user * 65536 + computer`) (gated: unconfirmed, source is paywalled or blocked). A GPO edited on DC1 increments both halves there; if
SYSVOL on DC2 lags, DC2 shows the old GPT version.

## Fix
- Mismatch on one DC only: SYSVOL replication problem. Check DFSR backlog and events on that DC and fix
  replication; Microsoft documents a non-authoritative (and authoritative) synchronization procedure for DFSR-replicated SYSVOL (set on the DC through ADSI Edit, then update DFSR configuration).
- Mismatch everywhere for one GPO: someone edited GPT.INI by hand or restored half a GPO. Open the GPO in GPMC,
  make a trivial change and undo it so both halves get a new version (gated: unconfirmed, source is paywalled or blocked). Or restore the GPO from a GPMC backup (`Restore-GPO`).
- Missing SYSVOL folder (GPT gone, GPC present): restore from backup; confirm the GPO is unused before deleting an orphan container.

## Verify
- [ ] Script returns nothing.
- [ ] `gpresult /h` on an affected client lists the GPO as applied.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: the gpt.ini network path form and the requirement that the Group Policy template be readable, the DFSR SYSVOL non-authoritative and authoritative synchronization procedures, and Restore-GPO. Gated: the versionNumber attribute, the Version= line in gpt.ini, the user*65536+computer formula, the GPMC Details and Status tab wording and the stale-SYSVOL skip behaviour, because the protocol specifications are not available in a public GitHub repository. Removed as unconfirmed: the 60-day non-authoritative synchronization threshold and the Replication in sync wording.

Method: documentation only; no commands were run.
