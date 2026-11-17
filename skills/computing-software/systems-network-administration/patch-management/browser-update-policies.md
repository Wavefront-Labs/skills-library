---
id: computing-software.systems-network-administration.patch-management.browser-update-policies
name: browser-update-policies
category: computing-software
field: systems-network-administration
product: patch-management
tags: [browser-updates, chrome-enterprise, edge-update, firefox-esr, relaunch-notification, third-party-patching]
level: practitioner
status: gated
description: "Keep Chrome, Edge and Firefox patched in the enterprise: update policies, version pinning and rollback, forced relaunch notifications, and ESR vs rapid channels."
sources:
  - https://support.google.com/chrome/a/answer/6350036
  - https://learn.microsoft.com/en-us/deployedge/microsoft-edge-update-policies
  - https://learn.microsoft.com/en-us/deployedge/microsoft-edge-browser-policies/relaunchnotification
  - https://mozilla.github.io/policy-templates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browser update policies

**Goal:** browsers (the most attacked desktop apps) get security fixes within days, and actually restart onto them.

## Chrome (Google Update policies)
- Google's update guidance (Windows Group Policy, Google Update Applications): enable "Update policy override default" with "Allow updates (recommended)", and repeat under Google Chrome so auto-updates are always allowed.
- "Target version prefix override" pins to a version prefix only for temporary compatibility holds; "Rollback to Target version" is used with it to roll back temporarily, and Google notes user data can be deleted on a version downgrade unless snapshots or sync are kept.
- The Chrome browser policies `RelaunchNotification` and `RelaunchNotificationPeriod` control restart prompts for pending updates; confirm accepted values on Google's policy list (gated: unconfirmed, source is paywalled or blocked).

## Edge (Microsoft Edge Update policies)
- Edge Update policies include `UpdateDefault`, `Update`, `TargetVersionPrefix` and `RollbackToTargetVersion` (Edge Update 1.2.145.5 and later for UpdateDefault).
- Browser policy `RelaunchNotification` can be Recommended (dismissable warning) or Required (browser restarts automatically after the notification period); `RelaunchNotificationPeriod` is in milliseconds with a default of 604800000 (one week).
- Channels: Stable and Extended Stable, which follows a longer release cadence than Stable (see Edge documentation for the current cadence).

## Firefox
- Use Firefox ESR for managed fleets needing fewer feature changes; check Mozilla's release schedule for how quickly ESR receives security fixes.
- `policies.json` (or ADMX) supports `AppAutoUpdate`, `DisableAppUpdate`, `AppUpdatePin` (prevent updating beyond a version) and `AppUpdateURL` (internal update URL).

## Process
- Emergency browser fixes (zero-days) roll out automatically; your job is to make sure policies do not block updates and relaunch happens.
- Report actual running versions (not installed) from EDR or inventory, because updates apply only after relaunch.

## Gotchas
- Per-user installs (Chrome in AppData) escape machine policies; block or migrate them.
- VDI golden images need browser updates baked in, or non-persistent desktops revert.

## Verify
Within your policy window (for example 72 hours) of a browser security release, your target share of devices (for example 95%) report the new version as running.

## Checked
Date: 2026-10-27. Documentation: Google Chrome Enterprise "Manage Chrome updates (Windows)" (Group Policy names, target version prefix, rollback), Microsoft Edge Update policies and RelaunchNotification and RelaunchNotificationPeriod pages (Recommended or Required, milliseconds, one-week default), Mozilla policy templates (AppAutoUpdate, DisableAppUpdate, AppUpdatePin, AppUpdateURL). Chrome's RelaunchNotification values could not be read on Google's script-rendered policy list, so that claim is gated. Removed unconfirmed Edge cadence numbers and Chrome version example.
Method: documentation only; no commands were run.
