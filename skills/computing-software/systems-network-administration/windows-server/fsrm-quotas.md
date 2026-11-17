---
id: computing-software.systems-network-administration.windows-server.fsrm-quotas
name: fsrm-quotas
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, fsrm, file-server-resource-manager, fsrm-quotas, new-fsrmquota, new-fsrmquotatemplate, auto-apply-quota, hard-quota, soft-quota, threshold-notifications, home-folders, fsrm-auto-apply-quota]
level: practitioner
status: docs-checked
description: "Use FSRM quotas: hard vs soft, templates with threshold notifications, auto-apply quotas for home folders, and how users see quota limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/quota-management.md
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmquota
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmquotatemplate
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/set-fsrmquotatemplate
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# FSRM quotas

FSRM quotas are **per folder** (not per user like NTFS disk quotas) and count actual disk
usage of the folder tree.

## Install and template
```powershell
Install-WindowsFeature FS-Resource-Manager -IncludeManagementTools
Set-FsrmSetting -SmtpServer smtp.ad.example.com -AdminEmailAddress 'storage-team@example.com' -FromEmailAddress 'fsrm@example.com'
$t85  = New-FsrmQuotaThreshold -Percentage 85 -Action (New-FsrmAction Email -MailTo '[Admin Email]' -Subject 'Quota threshold reached at 85%' -Body 'A folder quota passed 85% of its limit.')
$t100 = New-FsrmQuotaThreshold -Percentage 100 -Action (New-FsrmAction Event -EventType Warning -Body 'A folder quota reached its limit.')
New-FsrmQuotaTemplate -Name 'Home 10GB' -Size 10GB -Threshold $t85,$t100
```
- **Hard** quota (default, no `-SoftLimit`) blocks writes at the limit; **soft** (`-SoftLimit`) reports usage and runs thresholds but does not enforce the limit,
  useful for monitoring growth before enforcing.
- Bracketed variables such as `[Admin Email]` are expanded by FSRM; the cmdlet reference shows `[Admin Email]`, `[File Owner]` and `[source file path]`.

## Apply
```powershell
New-FsrmQuota -Path '<DATA_DRIVE>:\Shares\Projects\Apollo' -Template 'Home 10GB'
# every existing and future subfolder of Home gets its own quota
New-FsrmAutoQuota -Path '<DATA_DRIVE>:\Shares\Home' -Template 'Home 10GB'
Get-FsrmQuota | Format-List *
```
Auto-apply quotas are ideal for home folders: each existing and future subfolder gets the template.
Changing the template can update derived quotas: `-UpdateDerived` changes all of them, `-UpdateDerivedMatching` only those that still match the original template (`Set-FsrmQuotaTemplate`).

## Verify
- [ ] Copying beyond the limit fails for a hard quota; email/event at 85%.
- [ ] `Get-FsrmQuota` usage matches folder size (`Update-FsrmQuota` starts a long-running rescan; use it only when usage is out of sync, for example after re-enabling a disabled quota).

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- New-FsrmQuotaTemplate / New-FsrmQuota: -Size, -SoftLimit (soft limit reports and runs thresholds without enforcing), -Threshold, -Template; hard is the behaviour without -SoftLimit.
- New-FsrmAutoQuota applies a template to existing and future subfolders; Set-FsrmQuotaTemplate has -UpdateDerived and -UpdateDerivedMatching; Update-FsrmQuota starts a quota scan.
- The quota-management page confirms quotas apply to a volume or folder. Removed unconfirmed details: the per-user comparison, expansion variables not shown in the cmdlet reference, the client free-space display and error text, and the Usage/SoftLimit property list.

Method: documentation only; no commands were run.
