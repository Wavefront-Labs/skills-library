---
id: computing-software.it-support-helpdesk.intune-mdm.compliance-not-evaluated-and-grace-states
name: compliance-not-evaluated-and-grace-states
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, compliance-not-evaluated, compliance-states, in-grace-period, compliance-troubleshooting, intune, compliance-validity-period, compliance-reports]
level: practitioner
status: docs-checked
description: "Troubleshoot Intune compliance states (Not evaluated, In grace period, Error) and the Is active validity-period setting that makes silent devices noncompliant."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-security/compliance/monitor-policy"
  - "https://learn.microsoft.com/en-us/intune/device-security/compliance/overview"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# compliance-not-evaluated-and-grace-states

## States and what they mean
| State | Meaning | First thing to check |
|---|---|---|
| Compliant | Device applied the compliance policy settings | n/a |
| In grace period | Targeted but not yet compliant with all settings; noncompliant but within the admin-defined grace period | Which setting fails; the action schedule |
| Not compliant | Failed one or more settings, or the user didn't comply | Failing setting |
| Not evaluated | Initial state for newly enrolled devices (see below) | Check-in time, assignments |
| Error | Shown under "Others" in a policy's device status chart, with Not evaluated | Per-setting status report |

## Why a device is Not evaluated
The monitoring page lists these causes:
- Newly enrolled device (initial state).
- No compliance policy assigned and no trigger to check compliance.
- Device hasn't checked in since the policy was last updated.
- Devices without a specific user: iOS/iPadOS from Apple's Device Enrollment Program with no
  user affinity, Android Enterprise dedicated devices, and devices enrolled with a device
  enrollment manager (DEM) account.
For user-targeted policies on such devices, target device groups instead.

## Validity period ("Is active")
Compliance policy settings include a **Compliance status validity period**: default 30 days,
configurable 1 to 120. A device that doesn't report on all its policies in that time is
treated as noncompliant. See the device's row for the setting named **Is active** under
Devices > Monitor > Setting compliance.

## Timing
- A device appears in a policy's Device status chart only after it checks in, processes the
  policy and reports; this can take up to 24 hours when the device is online.
- The same-policy report shows only that policy's status; another policy can still make the
  device noncompliant.
- Force a sync from the device or the admin center to speed up the first report.

## Gotchas
- "Devices without compliance policy" tile lists devices with nothing assigned. The tenant
  setting "Mark devices with no compliance policy assigned as" defaults to Compliant;
  change it to Not compliant if Conditional Access should block unassigned devices.
- Conditional Access reads the compliance status reported to Entra, so allow time after
  Intune evaluates.

## Verify
After the fix, the device shows Compliant in the policy's View report, the per-setting rows
pass, and Conditional Access access is restored.

## Checked
2026-11-01. Confirmed against Intune Learn pages "Monitor device compliance" and "Compliance
overview": state definitions, Not evaluated causes, 30-day default and 1 to 120 range of the
validity period, "Is active" setting name, 24-hour reporting delay, no-policy tenant default.
Removed: Conflict and Not applicable states, the Default Device Compliance Policy's other
two settings, the Health Attestation reboot claim and the 8-hour first-sync claim, none of
which the fetched pages confirmed; the troubleshooting source returned 404.
Method: documentation only; no commands were run.
