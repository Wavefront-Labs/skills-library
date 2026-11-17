---
id: computing-software.it-support-helpdesk.intune-mdm.admx-ingestion-and-administrative-templates
name: admx-ingestion-and-administrative-templates
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, admx-ingestion, administrative-templates, imported-admx, settings-catalog, group-policy, adml, intune]
level: advanced
status: docs-checked
description: "Deliver Group Policy-style settings from Intune: settings catalog administrative templates, importing third-party ADMX/ADML files, limits, dependency errors and replacing imports."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/administrative-templates-windows"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/administrative-templates-import-custom"
  - "https://learn.microsoft.com/en-us/windows/client-management/win32-and-centennial-app-policy-configuration"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# admx-ingestion-and-administrative-templates

Windows MDM can apply ADMX-backed policies through the Policy CSP. Intune exposes them
three ways:

| Route | Use when |
|---|---|
| **Settings catalog > Administrative Templates** | First choice: built-in ADMX settings, no download and no OMA-URI. Platform Windows 10 and later, profile type Settings catalog |
| **Templates > Administrative Templates** (legacy profile type) | Deprecated and read-only since the December 2412 release; do not build new profiles here |
| **Imported administrative templates** | Custom or partner apps with their own ADMX/ADML (the Intune page lists Adobe Reader, Mozilla Firefox and Zoom as examples) |

In the settings catalog, a setting with (User) in its name applies to users when they
sign in; settings without it apply to devices.

## Importing a custom ADMX
1. Get the vendor's ADMX and matching en-us ADML.
2. Sign in with an account that has the Policy and Profile Manager built-in role. In the
   Intune admin center: Devices > Manage devices > Configuration > **Import ADMX** tab >
   Import. Upload the ADMX and the ADML for the default language, then Review + Create.
   Check the Status column (Refresh to update).
3. Upload dependencies first. If the ADMX has a `using prefix` entry in its
   `policyNamespaces` node, the referenced ADMX must be imported first, or the error
   names the missing namespace. Example from the page: import mozilla.admx/mozilla.adml
   (status Available) before firefox.admx/firefox.adml. Some files need Windows.admx
   first (error: `ADMX file referenced not found NamespaceMissing:Microsoft.Policies.Windows. Please upload it first.`).
4. Create profile: Devices > Manage devices > Configuration > Create > New policy >
   Platform Windows 10 and later > Profile type Templates > **Imported Administrative
   templates (Preview)**, configure, assign.

Do not import ADMX files that ship in the Windows `PolicyDefinitions` folder to configure those
settings (use the settings catalog or a custom profile); import them only when another
file needs them as a parent namespace.

## How it lands on the device
Per the Win32 and Desktop Bridge ADMX ingestion article, ADMX files are ingested through
the Policy CSP URI `./Device/Vendor/MSFT/Policy/ConfigOperations/ADMXInstall` and then
processed into MDM policies. Settings are addressed as
`./{user or device}/Vendor/MSFT/Policy/Config/{AppName}~{SettingType}~{CategoryPathFromAdmx}/{PolicyName}`,
where `{AppName}` and `{SettingType}` come from the ADMXInstall URI. Class `User` maps to
`./user`, `Machine` to `./device`.

## Limits and gotchas
- Maximum 20 ADMX files, each 1 MB or smaller. One ADML per ADMX, one language per
  ADMX, and only en-us ADML files are supported.
- The combo box setting type is unsupported: ADMX files using it fail to import.
- The feature is in public preview.
- Ingestion refuses registry locations under System, Software\Microsoft and
  Software\Policies\Microsoft except an allow-list (Office, Edge, OneDrive,
  Visual Studio and others are on it). Settings that cannot be ingested must be set by
  pushing registry keys directly, for example with a PowerShell script.
- Some OS components enforce ADMX values only on domain-joined devices; ingestion and
  setting still succeed on non-domain-joined devices.
- Uploading an ADMX whose settings are already imported fails with a namespace error.
  To update: delete profiles using the old ADMX, delete the original ADMX, import the
  new ADMX/ADML (option 1); or give the new ADMX a different namespace, ideally with a
  version number, and import it (option 2).
- To remove a dependency, delete the dependent ADMX first (firefox.admx), then the
  prerequisite (mozilla.admx).
- Updating a "Not Configured" imported ADMX policy needs the Device configurations >
  Delete permission (included in Policy and Profile Manager).

## Verify
Check that the imported ADMX shows Status Available. On the device, check the registry key named by the
`key` attribute in the ADMX for the expected value.

## Checked
Date: 2026-11-07. Read in full: the settings catalog ADMX article, the import custom
ADMX article, and the Win32 and Desktop Bridge ADMX ingestion article (long SyncML
payload examples skimmed, prose and URI-format sections read).
Removed as unconfirmed: the claim that the Administrative templates profile is merely
"being superseded" (page says deprecated and read-only from December 2412), Office,
Edge and Chrome listed as settings catalog contents, Citrix Workspace as an example,
the "Create report"/MdmDiagnosticsTool and event log error 404/454 troubleshooting, the
HKLM\SOFTWARE\Policies registry claim, "max import count and file size" wording
(replaced by the 20 files/1 MB limits), the "can't delete while a profile uses it"
claim (the page says delete profiles first when replacing), and the Firefox
`about:policies` verify step.
Method: documentation only; no commands were run.
