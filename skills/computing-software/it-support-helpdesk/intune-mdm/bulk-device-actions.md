---
id: computing-software.it-support-helpdesk.intune-mdm.bulk-device-actions
name: bulk-device-actions
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, bulk-device-actions, remote-actions, graph-api, sync, restart, rename, multi-admin-approval]
level: practitioner
status: docs-checked
description: "Run Intune remote actions on many devices: the Bulk device actions blade, Graph PowerShell loops, throttling, multi admin approval for wipes, and confirming results per device."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-management/actions/"
  - "https://learn.microsoft.com/en-us/graph/api/resources/intune-devices-manageddevice"
  - "https://learn.microsoft.com/en-us/intune/fundamentals/role-based-access-control/multi-admin-approval"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bulk-device-actions

Sync many devices after a policy fix, restart a lab, rename a batch, retire a department's
phones. Intune has a portal blade for up to 100 devices at a time and the Graph API for more.

## Portal
Devices > All devices > **Bulk device actions**: on Basics pick the OS and action, on
Devices pick up to the action's maximum (100 devices at a time), then Review + create.
Windows bulk actions: Autopilot reset, Collect diagnostics, Delete, Rename, Restart, Retire,
Sync, Wipe. Apple mobile adds Send custom notification and Update cellular data plan;
macOS and Android offer a shorter list; ChromeOS offers Deprovision, Lost mode, Restart and
Wipe. Bulk rename names must include `{{serialnumber}}` or `{{rand:x}}`.

## Graph PowerShell for larger sets
The managedDevice resource in Microsoft Graph exposes the actions `syncDevice`,
`rebootNow`, `retire` and `wipe`. Script them with the Graph SDK or REST calls, pausing
between calls and backing off on HTTP 429 throttling responses. Look up exact cmdlet names
and required permission scopes in the Graph reference for each action.

## Safety for destructive actions
- **Multi Admin Approval**: access policies requiring a second admin to approve changes;
  device actions covers wipe, retire and delete. It needs at least two administrator
  accounts. Turn it on before you need it; it protects against a compromised admin account.
- Daily tenant limits apply across portal, bulk and Graph requests: Wipe 500, Retire 1,000,
  Delete 1,000. Retire, Wipe and Delete override other pending actions on a device.
- Build the device list from a filter, export it, have someone review it, then run.
- Never test a bulk script with wipe/retire. Test with Sync.

## Confirming results
- Devices > **Device actions** shows the status of actions; export for the ticket.
- Devices must be online to receive commands. For MDM devices a Delete hides the device at
  once and starts a Retire; Completed means the server side finished, not the device.
- Review pending actions before closing the change.

## Gotchas
- Entra hybrid joined Windows devices can't be renamed from Intune.
- Restart on a user's device without notice loses work; send comms or schedule.
- Delete removes the device from Intune management, removes company data and retires it.

## Verify
Device actions report shows every target Complete (or a list of pending/failed handled),
and spot checks on devices confirm the effect (new name, last sync time, restarted).

## Checked
2026-11-01. Confirmed against Intune Learn "Device actions" (bulk list per OS, 100-device
maximum, daily limits, action precedence, Delete behaviour), Multi Admin Approval and the
Graph managedDevice resource (syncDevice, rebootNow, retire, wipe). Removed: the PowerShell
loop and cmdlet and scope names, Rotate LAPS and Change primary user as bulk actions, wipe
option details and the pending-wipe-months claim, none confirmed by those pages.
Method: documentation only; no commands were run.
