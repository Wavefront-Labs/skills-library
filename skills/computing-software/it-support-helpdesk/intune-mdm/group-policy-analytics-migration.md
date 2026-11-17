---
id: computing-software.it-support-helpdesk.intune-mdm.group-policy-analytics-migration
name: group-policy-analytics-migration
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, group-policy-analytics, gpo-migration, settings-catalog, mdm-support-percentage, gpo-backup, intune]
level: practitioner
status: docs-checked
description: "Migrate GPOs to Intune with Group Policy analytics: export GPO XML, read MDM support %, readiness report, migrate to settings catalog, and handle unsupported settings."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-configuration/import-group-policy-analytics"
  - "https://learn.microsoft.com/en-us/intune/device-configuration/migrate-group-policy"
  - "https://learn.microsoft.com/en-us/powershell/module/grouppolicy/get-gporeport"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# group-policy-analytics-migration

Group Policy analytics (Intune admin center > Devices > Manage devices > Group
Policy analytics) imports exported GPOs, shows which settings MDM providers
support, flags deprecated or unavailable ones, and can migrate the supported
ones into a settings catalog policy. Windows only. Role: Intune administrator,
or a role with Security baselines and Device configurations permissions.

## Export GPOs
In GPMC: expand Group Policy Objects, right-click the GPO, Save report, type
XML File. Or with the GroupPolicy module (Get-GPOReport needs -ReportType Xml or
Html):
```powershell
Get-GPO -All | ForEach-Object {
  Get-GPOReport -Guid $_.Id -ReportType Xml -Path ".\gpo-$($_.DisplayName -replace '[^\w-]','_').xml"
}
```
Each file must be under 4 MB with proper Unicode encoding or the import fails;
split a larger GPO by reducing its settings.

## Import and read the results
Select Import, pick one or more XML files, choose scope tags (Default tag if you
pick none; only admins sharing a scope tag see the GPO), Create. Columns:
| Column | Meaning |
|---|---|
| MDM Support | Percentage of the GPO's settings with an Intune equivalent; updates itself when Microsoft changes the mapping |
| Active Directory Target | OU target from the GPO |
| Unknown Settings | CSPs that could not be analysed |
| Targeted in AD | Yes = linked to an OU |
Select the percentage for per-setting detail: Setting Name, category, MDM
Support (Yes, No, or a suggested newer replacement), Value, Scope (user or
device), Min OS Version (build number), CSP Name, CSP Mapping (an OMA-URI you
can use in a custom profile).

Parsed sources: Policy, PassportForWork, BitLocker, Firewall and AppLocker CSPs
and Group Policy Preferences. Known issue: only non-ADMX settings in English
are supported; other languages make MDM Support inaccurate.

Readiness report: Reports > Device management > Group policy analytics.
Statuses: Ready for migration, Not supported (typically not exposed to MDM),
Deprecated (old Windows or Edge versions). Reports > Group policy migration
readiness filters by Migration Readiness, Profile type and CSP Name; after
adding or removing GPOs the data can take about 20 minutes to refresh.

## Migrate
1. Devices > Manage devices > Group Policy analytics, tick Migrate on the GPO(s),
   then in Settings to migrate tick the settings. Review first: some settings
   make no sense on cloud-native devices.
2. Review values (copied from the GPO; editable after creation), name the
   profile, scope tags, assignments, Create.
3. Conflicts: when several GPOs set the same setting differently, you get
   "Conflicts are detected for the following settings"; untick all but one.
Migrate is best effort:
- AppLocker and Firewall rule settings have Migrate disabled; configure them
  with Endpoint Security (Firewall policy, Application control policy).
- Old Office ADMX or older Chrome settings may map to a different supported
  setting that Intune suggests.
- Errors appear in Notifications, usually an unexpected value format or a
  missing required child setting.
- Only admins scoped to the GPO can create a policy from it.
- For settings with no MDM equivalent, use the CSP Mapping column with a custom
  OMA-URI profile where one exists; otherwise redesign (for example a script or
  app).

## Cleanup
Delete imported GPOs from the context menu in Group Policy analytics when done.

## Verify
On a pilot device the migrated settings catalog profile reports Succeeded and the
effective settings match what the GPO delivered.

## Checked
2026-11-08. Confirmed against the Microsoft Learn pages Import and analyze your
on-premises GPOs using Group Policy analytics (last updated 2026-06-22), Create
a Settings Catalog policy using your imported GPOs (2026-04-14) and the
Get-GPOReport reference (-ReportType Xml or Html). Removed as unconfirmed: the
replacement table (drive maps, printers, scripts), MDMWinsOverGP pilot advice,
the WMI filter, loopback and item-level targeting gotcha, the claim that GPP is
always unsupported (the page lists Group Policy Preferences as parsed), and the
gpresult verification.
Method: documentation only; no commands were run.
