---
id: computing-software.systems-network-administration.active-directory.ou-group-and-gpo-design
name: ou-group-and-gpo-design
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-ds, organizational-unit, ou-design, agdlp, agudlp, security-groups, group-policy, gpo, lsdou, gpo-precedence, enforced, block-inheritance, security-filtering, wmi-filter, gpresult, gpupdate, rsop, dcdiag, repadmin, replication, tiering, tier-0, privileged-access, entra-id, entra-connect, entra-cloud-sync, hybrid-identity, azure-ad, ou-structure-design, gpo-enforced]
level: advanced
status: gated
description: "Design AD OUs, groups and GPOs: AGDLP, LSDOU precedence, gpresult/gpupdate, dcdiag and repadmin health checks, admin tiering, Entra Connect/Cloud Sync."
sources:
  - https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/cannot-apply-user-gpo-when-computer-objects-dont-have-read-permissions
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/what-is-cloud-sync
  - https://learn.microsoft.com/en-us/powershell/module/grouppolicy/backup-gpo
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# OU, group and GPO design - structure for delegation and policy, not the org chart

**Goal:** an Active Directory layout where Group Policy targeting and admin delegation
are obvious, health is checkable in two commands, and privileged accounts are fenced off.

## 1. OU structure: design for GPO and delegation
OUs exist for two reasons only: **applying GPOs** and **delegating admin rights**. Mirror
the org chart and you will re-org AD every time HR re-orgs.

```
<DOMAIN>
|-- Admin              (Tier 0: admin accounts, groups, PAWs - locked down)
|-- Corp
|   |-- Users          (Standard, Service-Accounts, Disabled)
|   |-- Workstations   (Laptops, Desktops, Kiosk)
|   |-- Servers        (by role: File, Web, SQL - each Tier 1)
|   `-- Groups         (Security, Distribution)
`-- Staging            (new computers land here; redircmp)
```
- Group policy can be applied to OU containers but not to the default `CN=Computers` and `CN=Users` containers.
  Keep those containers empty and redirect the defaults with `redircmp "OU=Staging,DC=example,DC=com"` and `redirusr`.
  Redirection affects objects created by earlier-version APIs (Domain Join UI, `net user`, `net computer`).
- Separate users and computers into different OUs; user and computer settings then live
  in separate GPOs.
- Keep the tree shallow so inheritance stays easy to reason about.

## 2. Groups: AGDLP
Accounts -> **Global** (role: `GG-HR-Staff`) -> **Domain Local** (resource+right:
`DL-FS01-HR-Modify`) -> Permission. In multi-domain forests, insert **Universal** groups
(AGUDLP). Name with a prefix scheme and put the purpose in the description field.
Group SIDs are carried in the Kerberos ticket, so membership changes show up after the user gets a new ticket.

## 3. GPO processing
Order of application: Local, then Site, then Domain, then OU (parent before child), and the last one applied wins
(gated: unconfirmed, source is paywalled or blocked). Modifiers:
- **Enforced** on a link cannot be overridden by lower links and ignores Block Inheritance
  (gated: unconfirmed, source is paywalled or blocked).
- **Block Inheritance** on an OU stops higher non-enforced GPOs (gated: unconfirmed, source is paywalled or blocked).
  Inspect and change it with `Get-GPInheritance` / `Set-GPInheritance`; link order and enforcement with `Set-GPLink`.
- Within one OU, link order 1 has the highest precedence (gated: unconfirmed, source is paywalled or blocked).
- **Security filtering:** since MS16-072 user settings are retrieved with the computer's security context, so if you
  remove `Authenticated Users` you must give the computer account **Read** on the GPO, for example by granting Read to
  `Domain Computers` (all domain computers belong to it); otherwise user policy fails to apply.
- WMI filters can be denied or slow down logon and boot; use them sparingly.
Reason for the gates: the Group Policy processing-order rules are documented in GPMC help and Learn pages that were
not readable in this review.

Design habits: one purpose per GPO (`C-Workstations-BitLocker`, `U-AllUsers-DriveMaps`), disable the unused half (User
or Computer configuration), and back up with `Backup-GPO -All -Path <BACKUP_DIR>`. Set all password policy in the
Default Domain Policy, and do not enable Block Inheritance on the Domain Controllers OU, or password policy changes may
not apply to DCs.

## 4. Testing and troubleshooting
```cmd
gpupdate /force
gpresult /r /scope computer
gpresult /h report.html          rem HTML report including the reason a GPO was not applied
```
Use the Group Policy operational event log for per-run detail (identify the activity ID of the processing run).

## 5. Replication and DC health
```cmd
repadmin /replsummary            rem replication summary per DC
repadmin /showrepl * /csv > repl.csv
dcdiag /v /c /e /q               rem /e all servers in the enterprise, /q only errors, /c comprehensive
dcdiag /test:dns
```
Investigate any failure count above zero. Most "GPO applies on some machines" issues are SYSVOL (DFSR) or DNS
problems: `dfsrdiag ReplicationState`, and check the `SYSVOL` share exists on every DC. Restore a DC from backup
only within the tombstone lifetime (default 180 days) and back DCs up well inside it; a DC offline longer than the
tombstone lifetime must be rebuilt, not reconnected.

## 6. Administrative tiering
- Classic model: **Tier 0** = DCs, AD, PKI, Entra Connect servers, identity backup; **Tier 1** = servers;
  **Tier 2** = workstations. Admins get a separate account per tier (`adm-t0-<user>`), and a higher-tier account
  never logs on to a lower-tier machine.
- Enforce with GPO "Deny log on" user rights, the `Protected Users` group, and Authentication Policy Silos.
  Keep `Domain Admins` near empty (Microsoft: needed only for break-glass use in a well-delegated model); Windows
  LAPS manages local admin passwords on Windows Server 2019 and later (April 2023 update and later).
Microsoft's Enterprise Access Model now extends Tier 0 into a control plane and splits tier 1 and tier 2 into
management/data-plane and user/app access areas; the separation principle is the same.

## 7. Hybrid identity
**Entra Connect Sync** (on-prem server, treat as Tier 0) or **Entra Cloud Sync** (provisioning agent, cloud-managed)
synchronise to Entra ID. Cloud Sync synchronises users, groups and contacts and, with device sync enabled, AD
computer objects for Microsoft Entra hybrid join; check the current comparison page for remaining feature gaps.
Scope sync to the `Corp` OUs only, never `Admin`.

## Verify
- [ ] Default `Computers`/`Users` containers are empty and redirected to a staging OU.
- [ ] Every ACL on resources references a DL group; no user is directly on an ACL.
- [ ] `gpresult /h` on a test machine shows the expected GPOs applied and no unexpected denials.
- [ ] `repadmin /replsummary` shows zero failures; `dcdiag /e /q` returns no errors.
- [ ] Tier 0 accounts cannot log on to workstations (test it).
- [ ] Sync scope excludes admin OUs; GPO backups exist.

## Checked
2026-10-27. Documentation: Microsoft Learn Enterprise access model, the MS16-072 GPO Read-permission article, Entra Cloud
Sync overview (updated 21 Oct 2026), GroupPolicy and dcdiag references, restore-virtualized-DC article, Windows LAPS overview
and Redirect users and computers containers. Confirmed: GPO user settings are read in the computer's security context with
Read for Domain Computers or Authenticated Users; `Backup-GPO -All -Path`; `Get-GPInheritance`, `Set-GPInheritance`,
`Set-GPLink`; `gpresult /r /scope computer` and `/h`; `dcdiag` flags /v /c /e /q and /test; `repadmin /replsummary` and
`showrepl * /csv`; `dfsrdiag ReplicationState`; default tombstone lifetime 180 days; WMI filters can slow logon and boot;
password policy belongs in the Default Domain Policy and Block Inheritance on the DC OU breaks it; Cloud Sync now includes
device sync. Corrected: the draft said Cloud Sync lacks device writeback, which the current overview contradicts. Gated:
LSDOU order, Enforced, Block Inheritance and link-order semantics. Removed as unconfirmed: the 3-5 level depth rule,
the 180-minute inter-site interval, the Denied/Filtered status strings, folder-redirection timing and the Intune remark.
Method: documentation only; no commands were run.
