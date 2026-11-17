---
id: computing-software.systems-network-administration.windows-server.group-policy-management
name: group-policy-management
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, group-policy, gpo, gpmc, grouppolicy-module, new-gpo, new-gplink, backup-gpo, restore-gpo, import-gpo, get-gporeport, admx, adml, central-store, policydefinitions, group-policy-preferences, gpp, item-level-targeting, loopback-processing, security-baseline, security-compliance-toolkit, lgpo, policy-analyzer, migration-table, starter-gpo, change-control, active-directory, gpo-settings-report]
level: practitioner
status: docs-checked
description: "Operate Group Policy day to day: ADMX Central Store, GPO lifecycle with the GroupPolicy module, backups and reports, Preferences with item-level targeting, loopback, and baseline imports."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-client/group-policy/create-and-manage-central-store
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/group-policy-settings-show-as-extra-registry-settings
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-preferences
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-processing
  - https://learn.microsoft.com/en-us/powershell/module/grouppolicy/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Group Policy management — build, change, back up and report GPOs like code

**Goal:** run the GPO lifecycle safely: templates in one place, every change tested
and reversible, settings documented. Design (OU layout, LSDOU precedence) lives in
`computing-software.systems-network-administration.active-directory.ou-group-and-gpo-design`;
broken processing in
`computing-software.systems-network-administration.active-directory.group-policy-and-sysvol-troubleshooting`.

## 1. ADMX Central Store
Copy current ADMX/ADML templates to
`\\<DOMAIN>\SYSVOL\<DOMAIN>\Policies\PolicyDefinitions` (with the `en-US` language
folder). GPMC on any admin box then edits with the same templates instead of its local
`%SystemRoot%\PolicyDefinitions`.
- Build the store from a pristine PolicyDefinitions folder of the newest Windows release you manage, then merge in
  application ADMX/ADML files; keep the previous folder renamed so you can revert. Replacing files in
  `%SystemRoot%\PolicyDefinitions` is not supported.
- Gotcha: GPMC and RSAT machines that use different ADMX/ADML versions can show settings as "Extra Registry Settings"
  that cannot be edited; the registry value `EnableLocalStoreOverride` (0 = use the SYSVOL store, the default) controls
  whether the Group Policy editor uses the local folder.

## 2. Lifecycle with the GroupPolicy module (RSAT)
```powershell
Import-Module GroupPolicy
New-GPO -Name 'SEC - Workstation - Firewall' -Comment 'Ticket <ID>; owner: <TEAM>'
Set-GPRegistryValue -Name 'SEC - Workstation - Firewall' -Key 'HKLM\Software\Policies\...' `
  -ValueName '<NAME>' -Type DWord -Value 1
New-GPLink -Name 'SEC - Workstation - Firewall' -Target 'OU=Pilot,OU=Workstations,DC=corp,DC=example' -LinkEnabled Yes
```
- **Naming:** `<scope> - <target> - <purpose>` so GPMC sorts sensibly.
- **One purpose per GPO**; monolithic GPOs can't be rolled back partially.
- **Disable the unused half** (user or computer configuration) of a GPO to make intent clear.
- **Pilot first:** link to a pilot OU or security-filter to a pilot group, then widen the
  link. Removing a *link* is instant rollback; deleting a GPO is not.

## 3. Backups, reports, change control
```powershell
Backup-GPO -All -Path '<BACKUP_DIR>' -Comment (Get-Date -f yyyy-MM-dd)
Get-GPOReport -Name 'SEC - Workstation - Firewall' -ReportType Html -Path '<DIR>\fw.html'
Restore-GPO -Name 'SEC - Workstation - Firewall' -Path '<BACKUP_DIR>'   # same domain, same GUID
Import-GPO -BackupGpoName 'X' -Path '<BACKUP_DIR>' -TargetName 'X' -MigrationTable '<FILE>.migtable' -CreateIfNeeded
```
- Back up **before** every change and nightly. `Backup-GPO` writes to a directory that must already exist; record
  links separately (`Get-GPInheritance` per OU) so a restore can be re-linked.
- `Import-GPO` copies settings into another GPO (`-TargetName`, `-CreateIfNeeded`); a migration table
  (`-MigrationTable`) maps security principals and paths between domains.
- Keep XML reports (`-ReportType Xml`) in source control to see what changed.

## 4. Preferences (GPP) and item-level targeting
GPP sets drive maps, printers, registry, local users and groups, scheduled tasks, files. By default preferences do not
remove settings when the GPO stops applying (they **tattoo**); *Remove this item when it is no longer applied* changes
that and automatically sets the action to Replace.
- *Apply once and do not reapply* applies an item a single time.
- **Item-level targeting** (security group, OU, site, operating system, IP address range, registry match, WMI query,
  and more) lets one GPO carry many conditional items, combined with AND/OR logic.

## 5. Loopback processing
For kiosks, RDS hosts and labs, set *Configure user Group Policy loopback processing
mode* (Computer Configuration > Policies > Administrative Templates > System > Group Policy) on the computer GPO:
**Merge** (the computer's GPO list is added after the user's, so its user settings win on conflict) or **Replace** (only
the user settings of GPOs that apply to the computer object are used).

## 6. Security baselines
Import baseline GPO backups with `Import-GPO` and keep your exceptions in a separate, higher-precedence GPO so the
baseline can be replaced cleanly on the next release. Test `Import-GPO` with migration tables in a lab first.

## Verify
- [ ] Central Store exists and GPMC shows no "Extra Registry Settings" for known policies.
- [ ] Every GPO has an owner/ticket comment and one purpose.
- [ ] Nightly `Backup-GPO -All` runs, and links/WMI filters are exported separately.
- [ ] A change was piloted (link or filter) before broad linking.
- [ ] GPP items that must disappear on removal have "remove when no longer applied".

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: Central Store location and build procedure, the unsupported replacement of %SystemRoot%\PolicyDefinitions, the Extra Registry Settings cause and the EnableLocalStoreOverride value; the cmdlet parameters of New-GPO (-Comment), Set-GPRegistryValue, New-GPLink (-LinkEnabled), Backup-GPO, Get-GPOReport, Restore-GPO and Import-GPO (-MigrationTable, -CreateIfNeeded); GPP behaviour (no removal by default, Remove this item sets Replace, Apply once, item-level targeting items); loopback Merge and Replace semantics and policy path. Removed as unconfirmed: the claim that Backup-GPO omits links, WMI filters and permissions, the Update-versus-Replace churn advice, cpassword and MS14-025, LAPS advice, the AGPM support status, the Security Compliance Toolkit, Policy Analyzer and LGPO steps (not readable in a public repository), and the GpoStatus processing-speed claim.

Method: documentation only; no commands were run.
