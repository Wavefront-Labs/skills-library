---
id: computing-software.it-support-helpdesk.intune-mdm.custom-oma-uri-profiles
name: custom-oma-uri-profiles
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, oma-uri, custom-profile, policy-csp, configuration-service-provider, intune]
level: advanced
status: docs-checked
description: "Write Intune custom OMA-URI profiles for Windows CSP settings not in the catalog: URI structure, data types, device vs user scope, the Add/Replace/Get rule, who sees values."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/custom-settings-windows-10"
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-configuration-service-provider"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# custom-oma-uri-profiles

A Windows custom profile sets Configuration Service Provider (CSP) nodes by OMA-URI. Use
it only when the setting is not in the settings catalog or the Windows device restriction
profile, which cover many settings already. Microsoft notes Intune may support more
settings than the pages list; browse the Settings catalog first.

## URI structure (Policy CSP)
```text
./Device/Vendor/MSFT/Policy/Config/<AreaName>/<PolicyName>   device scope
./User/Vendor/MSFT/Policy/Config/<AreaName>/<PolicyName>     user scope
./Vendor/MSFT/Policy/Config/<AreaName>/<PolicyName>          same as Device (Device/ may be omitted)
```
Read the result of a policy at the matching `.../Policy/Result/<AreaName>/<PolicyName>`
path. Some policies can only be configured at device level; the CSP page for each setting
states its scope. The OMA-URI field in Intune is case sensitive.

## Fields for each setting
- **Name** (unique), **Description**, **OMA-URI** (case sensitive), **Data type**, **Value**.
- Data types offered: Base64 (file), Boolean, String (XML file), Date and time, String,
  Floating point, Integer. The value format depends on the type (a date picker for Date and
  time).
- **Export** writes the list of settings you added to a CSV file.

## Choosing a setting
- The CSP reference lists every CSP Windows supports and the versions each supports; not
  all settings suit all Windows versions.
- Intune does not support every setting in the CSP reference. The setting's page must show
  the **Add, Replace and Get** operations. If the value returned by Get does not match the
  value supplied by Add or Replace, Intune reports a compliance error.

## Security
For String, Base64 and XML data types the stored value is obscured, but anyone with a
Microsoft Intune role holding Device configurations > Create, Read and Update (for
example the Policy and Profile manager built-in role) or the Intune Administrator Entra
role can see it. Do not put secrets in custom profiles.

## Steps
1. Find the setting's CSP page; check scope, supported versions and allowed values.
2. Create a Windows custom profile and add the OMA-URI rows.
3. Assign it to a pilot device group, then monitor the profile status.

## Checked
Date: 2026-11-07. Read in full: Intune "Use custom settings for Windows client devices" and the opening sections (Policy scope,
node list) of the Policy CSP page. Removed as unconfirmed: the Widgets/NewsAndInterests example, ADMX `<enabled/>` string format,
the Intune menu path "Templates > Custom", per-setting status labels, error codes `0x87d1fde8` and `-2016281112`, SyncML 404 meaning,
the MdmDiagnosticsTool `-cab` flag, the PolicyManager registry location, the Home/Pro edition and tattooing claims, and the Verify
step. The configuration-service-provider-reference source was dropped (the fetched page was a 599-character index stub).
Method: documentation only; no commands were run.
