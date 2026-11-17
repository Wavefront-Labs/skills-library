---
id: computing-software.systems-network-administration.windows-server.group-policy-registry-tattooing
name: group-policy-registry-tattooing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [group-policy, gpo, registry-tattooing, group-policy-preferences, admx]
level: advanced
status: docs-checked
description: "Understand which Group Policy settings tattoo the registry: Policies-key ADMX settings vs preferences and custom ADMX, and how to clean up after unlinking."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-preferences
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/adm-template-disable-drivers
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/gpmc-import-gpo-fails-restore-gpo-backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group Policy registry tattooing

## True policies (clean up themselves)
True Administrative Template policy settings (written under the policy keys, for example `HKLM\Software\Policies`)
are removed when the GPO stops applying.

## Tattooing settings (stay after the GPO is gone)
- **Group Policy Preferences** items: by default they do not remove settings when the GPO stops applying, unless
  "Remove this item when it is no longer applied" is selected (which sets the Replace action).
- **Custom ADM/ADMX** templates that are preferences rather than true policies (for example ones that write outside the
  policy keys); Microsoft documents such a template as tattooing the registry, with changes remaining when the template
  goes out of scope.
- Scripts and one-off changes made by startup scripts.

## Cleaning up
- Preferences: before unlinking, edit the item to **Delete** action and let it apply once, or tick the
  "Remove this item" option ahead of time.
- Security settings and other tattooed values: apply a GPO that sets the desired value explicitly.
- Custom templates: remove values with a GPP Registry Delete item or a script.

## Diagnose
```cmd
gpresult /h report.html
```
Compare a value in the registry against the report: present in the registry but not set by any applied GPO suggests a
tattoo. Preference items in the GPMC editor are hidden by default for ADMX templates; enable the view that shows
preferences when you work on such templates.

## Verify
- [ ] New preference registry items have "Remove this item when it is no longer applied" where appropriate.
- [ ] Decommission checklist for GPOs includes a cleanup pass.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: Group Policy Preferences do not remove settings when the GPO no longer applies unless Remove this item is selected (which sets Replace); Microsoft documents a custom ADM template that is a preference rather than a true policy as tattooing the registry; preference items are hidden by default in the template editor. Removed as unconfirmed: the claim that true policies are removed by comparing a previous Registry.pol, the exact list of policy key paths, security settings tattooing in the local security database, the secedit defltbase reset and its warnings, and the Machine Registry.pol path.

Method: documentation only; no commands were run.
