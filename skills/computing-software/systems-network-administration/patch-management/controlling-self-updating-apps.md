---
id: computing-software.systems-network-administration.patch-management.controlling-self-updating-apps
name: controlling-self-updating-apps
category: computing-software
field: systems-network-administration
product: patch-management
tags: [self-updating-apps, auto-update, browser-updates, zoom, third-party-patching, patch-management]
level: practitioner
status: docs-checked
description: "Decide and enforce how self-updating browsers (Chrome, Edge, Firefox) update in managed fleets: policies to allow, pin, roll back or disable the updater."
sources:
  - https://support.google.com/chrome/a/answer/6350036
  - https://learn.microsoft.com/en-us/deployedge/microsoft-edge-update-policies
  - https://mozilla.github.io/policy-templates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlling self-updating apps

Most modern apps ship their own updater, so the question is who decides when. Both Google and
Microsoft recommend leaving browser auto-updates on so users get security fixes as they
ship; turn them off or pin a version only temporarily and with a process to catch up.

## Chrome (Windows, Google Update policies)
- Load `google.admx` and `GoogleUpdate.admx` into the policy definitions folder; the
  policies are under Computer Configuration > Google > Google Update. Only domain-joined or
  MDM-managed computers honour computer policy.
- Allow updates: enable **Update policy override default** (Allow updates, recommended) under
  Applications, and repeat under Applications > Google Chrome.
- Disable Chrome updates: Applications > Google Chrome > **Update policy override** >
  Disable updates. Google Update keeps checking, and component updates (such as Widevine)
  continue unless you also disable component updates. Not recommended.
- Pin a version: enable **Target version prefix override**. `90.` means the latest 90.x
  (the trailing period matters); a full `xx.xx.xx.xx` pins one exact version and risks a
  version that is not the newest or has known bugs. Pin only temporarily.
- Roll back: enable **Rollback to Target version** with a target prefix. Only the three most
  recent major releases are supported, and the user-data snapshots retained default to three.
- Channel: **Target Channel override** with `stable` or `extended`.
- Quiet hours: **Time period in each day to suppress auto-update check** (Duration is the
  only required field, at least 1).

## Edge (Microsoft Edge Update policies, ADMX `msedgeupdate.admx`)
- `UpdateDefault` ("Update policy override default"): 0 updates disabled, 1 always allow
  (recommended), 2 manual only, 3 automatic silent only. The per-channel `Update` policy
  overrides it. Available only on domain-joined Windows devices.
- Related per-channel policies: `TargetVersionPrefix` (target version override),
  `RollbackToTargetVersion`, `TargetChannel`.
- Preferences include `AutoUpdateCheckPeriodMinutes` and `UpdatesSuppressed` (daily
  suppression period). The page applies to Edge version 77 or later.

## Firefox (policy templates, `policies.json`)
- `AppAutoUpdate`: true installs updates without approval inside Firefox; false downloads
  them and lets the user choose when to install. Has no effect if updates are disabled.
- `DisableAppUpdate`: turns off application updates.
- Policy examples:
```
{ "policies": { "AppAutoUpdate": true } }
```

## Gotchas
- Disabling an updater without a central replacement leaves apps unpatched; pair it with a
  deployment catalog and an inventory by version.

## Verify
`chrome://policy` shows the applied Google Update policies; About Chrome shows the
"updates are disabled by an administrator" note when updates are off.

## Checked
2026-11-08. Confirmed against Chrome's "Manage Chrome updates (Windows)" page, the Edge
update-policies page (`UpdateDefault` values 0 to 3, per-channel policies) and the Mozilla
policy-templates page (`AppAutoUpdate`, `DisableAppUpdate`). Removed: Zoom, Teams and
Slack rows (the Zoom page was unreadable), `RelaunchNotification` settings, Firefox ESR
advice, the VDI advice, and the 95%/7-day and two-versions-behind reporting figures, none of
which the pages support.
Method: documentation only; no commands were run.
