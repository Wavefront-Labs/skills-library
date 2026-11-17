---
id: computing-software.systems-network-administration.windows-server.fsrm-classification-and-file-management-tasks
name: fsrm-classification-and-file-management-tasks
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, fsrm, file-server-resource-manager, file-classification, file-management-tasks, classification-properties, content-classifier, new-fsrmclassificationrule, file-expiration, data-retention]
level: advanced
status: docs-checked
description: "Use FSRM File Classification Infrastructure: classification properties and rules (folder, content regex), scheduled classification, and file management tasks like expiring stale files."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/classification-management.md
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/create-automatic-classification-rule.md
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/file-management-tasks.md
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmclassificationrule
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmfmjcondition
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmfmjaction
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSRM classification and file management tasks

## Classification
1. **Property** definitions (global): e.g. `Confidentiality` (Ordered list: Public, Internal, Confidential), `Department` (String).
```powershell
New-FsrmClassificationPropertyDefinition -Name 'Confidentiality' -Type OrderedList `
  -PossibleValue (New-FsrmClassificationPropertyValue -Name 'Public'),(New-FsrmClassificationPropertyValue -Name 'Internal'),(New-FsrmClassificationPropertyValue -Name 'Confidential')
```
2. **Rules** set properties:
   - Classification mechanism: the `-ClassificationMechanism` value names the method that sets the property, for example `Content Classifier` with `-ContentString` or `-ContentRegularExpression`.
```powershell
New-FsrmClassificationRule -Name 'Mark confidential files' -Property 'Confidentiality' -PropertyValue 'Confidential' `
  -Namespace @('<DATA_DRIVE>:\Shares\HR') -ClassificationMechanism 'Content Classifier' -ContentString 'Confidential' -ReevaluateProperty Aggregate
Set-FsrmClassification -Continuous -ContinuousLog    # classify new/changed files as they are saved
Start-FsrmClassification -Confirm:$false             # scheduled/full run
```
`-ReevaluateProperty` takes Never, Aggregate or Overwrite: without re-evaluation a rule only sets a property that has no value yet. Classification properties can select files for file management tasks and appear in storage reports.

## File management tasks
Scheduled actions on files matching conditions:
- **File expiration** (`New-FsrmFmjAction -Type Expiration -ExpirationFolder`): move matching files to an expiration folder.
- **Custom** (`-Type Custom`): run a command per file. A third type, `Rms`, applies Rights Management.
```powershell
$action = New-FsrmFmjAction -Type Expiration -ExpirationFolder '<ARCHIVE_DIR>'
$cond   = New-FsrmFmjCondition -Property 'File.DateLastModified' -Condition LessThan -Value 'Date.Now' -DateOffset 730   # DateOffset is an Int32 offset from -Value; the reference does not state the sign convention, so confirm in the job report before enabling expiration
$sched  = New-FsrmScheduledTask -Time (Get-Date '23:00') -Weekly Sunday
New-FsrmFileManagementJob -Name 'Expire stale Projects' -Namespace @('<DATA_DRIVE>:\Shares\Projects') `
  -Action $action -Condition $cond -Schedule $sched -Notification (New-FsrmFmjNotification -Days 14 -Action (New-FsrmAction Email -MailTo '[Admin Email]' -Subject 'Files will be archived'))
```

## Verify
- [ ] Sample files carry the expected property values (`Get-FsrmClassification` shows the classification run state).
- [ ] The file management job report lists moved files and the notification went out.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- New-FsrmClassificationPropertyDefinition -Type accepts OrderedList, MultiChoice, SingleChoice, String, MultiString, Integer, YesNo, DateTime; New-FsrmClassificationRule parameters (-ClassificationMechanism, -ContentString, -ContentRegularExpression, -ReevaluateProperty Never|Aggregate|Overwrite); rules without re-evaluation only set properties that are unset (create-automatic-classification-rule page); Set-FsrmClassification -Continuous -ContinuousLog.
- New-FsrmFmjAction types Expiration, Custom, Rms with -ExpirationFolder; New-FsrmFmjCondition -Property -Condition -Value -DateOffset (Value may be File.DateCreated, File.DateLastModified, File.DateLastAccessed or Date.Now with DateOffset); New-FsrmFMJNotification -Days -Action.
- Removed unconfirmed details: the Folder Classifier mechanism name, storage of properties in files or alternate data streams, Dynamic Access Control and Rights Management integration claims, and the owner-email variable. The DateOffset sign convention is not in the reference and is flagged in the skill.

Method: documentation only; no commands were run.
