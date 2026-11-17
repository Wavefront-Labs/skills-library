---
id: computing-software.it-support-helpdesk.intune-mdm.intune-log-analysis-and-sync-troubleshooting
name: intune-log-analysis-and-sync-troubleshooting
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, mdmdiagnosticstool, dsregcmd, csp-error-codes, policy-conflict, sync-failure, event-viewer, mdm-diagnostics, device-management-event-log, intune-management-extension, troubleshooting-portal, devicemanagement-event-log]
level: practitioner
status: draft
description: "Diagnose Intune policy sync failures and CSP errors from device-side MDM diagnostic logs, dsregcmd, Event Viewer, and resolve policy conflicts between overlapping profiles."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/diagnose-device-restrictions-profiles"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# intune-log-analysis-and-sync-troubleshooting

Goal: go past "it's not syncing, try a restart" and actually read what the
device is telling you — this is the diagnostic layer underneath the
higher-level enrollment and policy skills in this field.

## First: confirm enrollment and identity are healthy
- `dsregcmd /status` (elevated PowerShell/cmd) is the starting point for
  any sync issue. Check `AzureAdJoined`, `TenantId` matches the expected
  tenant (wrong-tenant joins happen with shared devices or MSP-managed
  fleets), and `KeySignTest`/token-related lines under the "Diagnostic
  Data" section passing — a failed primary refresh token means the device
  can authenticate to Entra but MDM check-ins will still fail downstream.
- In Settings → Accounts → Access work or school → the account → Info →
  "Create report" generates an MDM diagnostic report (same engine as
  `MdmDiagnosticsTool.exe`) with a full policy/CSP dump — use this before
  digging through raw event logs by hand.

## MdmDiagnosticsTool.exe
- `MdmDiagnosticsTool.exe -area DeviceEnrollment;DeviceProvisioning;Autopilot -cab <OUTPUT_PATH>\report.cab`
  collects a focused cab file for enrollment-specific issues — smaller and
  faster to generate than the full diagnostic report when you already
  know it's an enrollment problem.
- The full report (`-out <OUTPUT_PATH>` mode) includes an HTML summary
  listing every applied/failed configuration, by CSP, with the raw error
  code — this is usually faster to read than Event Viewer for "which
  policy failed" questions.

## Event Viewer: Device Management event log
- Applications and Services Logs → Microsoft → Windows →
  DeviceManagement-Enterprise-Diagnostics-Provider → Admin. This is where
  MDM policy push/pull attempts actually log, separate from the general
  System/Application logs most techs check first.
- Event ID 76/77/78 family covers CSP set/get failures; the event detail
  includes the CSP URI path and a hex error code — cross-reference the
  code against Microsoft's MDM error code documentation rather than
  guessing from the message text alone, several unrelated failures share
  similar wording.

## Common CSP/policy failure patterns
- **Policy conflict**: two profiles (e.g. a Settings Catalog profile and
  an older Device Restriction profile, or two admins' overlapping
  profiles) targeting the same CSP with different values — Intune
  resolves conflicts per-setting but will mark the policy as "Conflict"
  in the portal rather than silently picking one. Check the per-device
  policy report in the portal (Devices → device → Device configuration)
  for "Conflict" status before assuming a sync failure.
- **Scope/licensing mismatch**: a policy requiring a license the device's
  user doesn't have (e.g. certain Settings Catalog Defender settings
  needing specific M365 licensing) fails silently per-device rather than
  blocking assignment — check license assignment when one user's device
  fails a policy that works fleet-wide.
- **Stale cached policy**: a device that was offline when a policy was
  retracted/changed can hold a stale version until its next successful
  full sync — force sync (`Settings → Accounts → Access work or school →
  Info → Sync`, or Intune portal's remote "Sync" device action) rather
  than waiting for the normal ~8-hour cycle when testing a change.

## IME vs MDM channel — know which one owns the failing item
- Compliance policies, configuration profiles, and Settings Catalog go
  through the native MDM channel (the layer `dsregcmd`/Event Viewer above
  cover). Win32 apps, scripts, and Proactive Remediations go through the
  **Intune Management Extension**, a separate Windows service
  (`<PROGRAMDATA>\Microsoft\IntuneManagementExtension\Logs\`) with its
  own health. A device can be perfectly MDM-compliant with IME broken (or
  vice versa) — check IME service status
  (`Get-Service IntuneManagementExtension`) separately before assuming
  one failure implies the other.

## Gotchas
- "Not compliant" in the portal can mean the policy genuinely failed, or
  that the device just hasn't reported in since the policy was created —
  check "Last check-in" time before troubleshooting a compliance failure
  that might just be stale data.
- Changing a policy's assignment (adding/removing a group) does not
  retroactively remove settings already applied from the old
  assignment on some CSPs — some configuration requires an explicit
  removal/conflicting policy to actually unwind, not just unassignment;
  verify the setting is actually gone on-device, not just unassigned in
  the portal.

## Verify
- `dsregcmd /status` shows healthy join state and valid tokens, the MDM
  diagnostic report shows the previously-failing CSP/policy as applied
  with no conflict flag, and a forced sync completes with the portal's
  per-device policy report matching the device's actual on-disk/registry
  state for the setting in question.
