---
id: computing-software.it-support-helpdesk.intune-mdm.profile-conflicts-and-gpo-vs-mdm-precedence
name: profile-conflicts-and-gpo-vs-mdm-precedence
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, mdm-wins-over-gp, controlpolicyconflict, policy-conflict, group-policy, configuration-profiles, setting-conflict, intune]
level: advanced
status: docs-checked
description: "Resolve Intune profile conflicts and GPO vs MDM clashes on hybrid PCs: conflict reporting, ControlPolicyConflict MDMWinsOverGP, settings outside its reach, and fix order."
sources:
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-controlpolicyconflict"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/device-profile-troubleshoot"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/device-profile-monitor"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# profile-conflicts-and-gpo-vs-mdm-precedence

## Intune vs Intune conflicts
Conflicts happen when different policies set the same setting to different values. Intune handles them per setting:
- Compliance policy settings take precedence over the same setting in a configuration profile.
- Two compliance policies on the same setting: the most restrictive wins.
- Two configuration profiles on the same setting: Intune shows a **Conflict** and you resolve it manually.
- Two app protection policies: the first deployed stays applied and the second shows a conflict; if both apply at the same
  time, conflicting settings take the most restrictive value.
- Custom Apple profiles and custom OMA-URI policies are not evaluated by Intune (it is only the delivery mechanism). If
  they conflict with other policies, Apple randomly applies the settings.

Find them: Devices > All devices > the device > Device configuration > select the policy, then select the row in Conflict
state to see every policy and profile name that holds that setting. Per policy: Devices > Manage devices > Configuration >
Policies > the policy > Device and user check-in status > Per setting status. Check every place policies are created
(Group Policy analytics, endpoint security, security baselines), not only Configuration.

Statuses: Succeeded, Error, Conflict, Pending, Not applicable. Device assignment status can take 24-48 hours to reflect
group changes, so the numbers differ from check-in status.

Fix: one owner per setting. Split profiles by area, not by team, and avoid overlapping group assignments.

## GPO vs MDM on hybrid devices
To make MDM win for Policy CSP settings that have an equivalent Group Policy:
```text
OMA-URI: ./Device/Vendor/MSFT/Policy/Config/ControlPolicyConflict/MDMWinsOverGP
Integer: 1
```
Default is 0. At 1, the Group Policy service blocks setting those policies from the GP MMC. Setting 0 or deleting it removes
the blocks and restores the saved GP policies. Scope is device; Windows 10 1803 and later.

Limits stated by Microsoft:
- It applies only to policies in Policy CSP. Not all Group Policies exist in MDM.
- It does not apply to equivalent settings defined in other CSPs, such as the Defender CSP. Do not configure the same
  setting in both GPO and MDM unless it is under MDMWinsOverGP; otherwise there is a race condition and no guarantee which wins.
- For Windows Update conflicts, use `IgnoreWindowsUpdateGroupPolicies` (Update Policy CSP) instead: Windows Update Group
  Policy settings are ignored and only MDM values apply.
- In Windows 10 1803 the policy does not support Delete or setting back to 0 once set to 1.

Microsoft advises setting the policy at every sync, so the device removes settings that conflict with MDM: GP settings that
correspond to MDM-applied ones, refreshes the Policy Manager policies from MDM, and removes conflicting values set by scripts
or users outside GP.

## Recommended order on a migration
1. Run **Group Policy analytics** to map GPOs to MDM (see group-policy-analytics-migration).
2. Build the MDM profiles.
3. Set MDMWinsOverGP = 1 for the pilot group.
4. Unlink or security-filter the overlapping GPOs for the pilot computers; don't leave both long-term.

## Diagnosing a "setting won't stick"
- The MDM Diagnostic report lists GP settings blocked because the MDM equivalent is configured. Create it at Settings >
  Accounts > Access work or school > the account > Advanced Diagnostic Report > Create Report.
- Intune per-setting status for Conflict.
- Is the setting in Policy CSP at all? The Policy DDF tags settings that have a GP equivalent (ADMXBacked, ADMXMapped,
  GPRegistryMappedName, GPDBMappedName). If not, MDMWinsOverGP does not help.
- When a profile is removed, behaviour depends on the CSP: some remove the setting, some keep it (tattooing). On Windows the
  user must sign in and the device sync after unassigning.

## Gotchas
- Maintenance syncs run about every 8 hours, and a device allows one maintenance sync every 6.5 hours, so a fix may take
  that long to land unless you sync the device manually.
- A setting showing Not Applicable is not supported on that Windows version or edition.

## Verify
After the fix, per-setting status shows Succeeded (no Conflict), and the MDM Diagnostic report shows the expected blocked GP settings.

## Checked
Date: 2026-11-08. Read in full: Policy CSP ControlPolicyConflict, Intune "Common questions, answers, and scenarios with
policies and profiles", and "View and monitor device configuration policies". Removed as unconfirmed: "GPO wins in some
areas / last writer wins" default, the settings catalog name for MDMWinsOverGP, the Reports > Device configuration path,
Intune picking the stricter value for endpoint security, the gpresult and registry-key steps, the exceptions list
(GPP, scripts, security templates), and the "neither value guaranteed" wording for Intune-vs-Intune.
Method: documentation only; no commands were run.
