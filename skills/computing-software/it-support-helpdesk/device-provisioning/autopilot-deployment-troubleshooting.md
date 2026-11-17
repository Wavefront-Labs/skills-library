---
id: computing-software.it-support-helpdesk.device-provisioning.autopilot-deployment-troubleshooting
name: autopilot-deployment-troubleshooting
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, windows-autopilot, enrollment-status-page, esp, hardware-hash, hybrid-azure-ad-join, entra-join, co-management, autopilot-profile, dsregcmd, intune-management-extension, provisioning-failure, oobe, white-glove, esp-blocking-apps, autopilot-diagnostics]
level: practitioner
status: draft
description: "Debug Windows Autopilot enrollment failures: ESP timeouts and blocking apps, hardware hash registration problems, hybrid join failures, profile not applying."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/troubleshooting"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# autopilot-deployment-troubleshooting

Goal: fix a device stuck mid-Autopilot rather than reimaging it, and tell
the difference between "still working" and "actually failed" during the
Enrollment Status Page (ESP).

## The device never shows the Autopilot profile / OOBE is generic
1. Confirm the hardware hash is actually registered: Intune admin center
   → Devices → Enrollment → Windows enrollment → Devices, search by
   serial. Not there means the hash never reached Autopilot — check who
   submitted it (OEM pre-registration via reseller, or
   `Get-WindowsAutoPilotInfo` run manually) and that it went to the right
   tenant.
2. Confirm an Autopilot **profile** is assigned to that device's group,
   and that the device is actually a *member* of that group — dynamic
   group membership can take up to a few hours to evaluate after the
   hash is imported; a device appearing in the enrollment list without a
   profile assigned yet is a timing issue, not a config error, for the
   first few hours.
3. Network at OOBE: Autopilot needs internet access before any sign-in
   screen — a captive portal Wi-Fi (hotel/guest network requiring a
   browser login) blocks it silently; wired Ethernet is the fastest way
   to rule out network as the cause.

## Enrollment Status Page (ESP) stuck or timing out
- ESP has two phases — Device setup (apps/profiles marked "blocking") and
  Account setup (user-targeted apps) — know which phase it's stuck in;
  the error screen names it.
- A single app marked "Block device use until this app and all other
  required apps are installed" with a broken detection rule or install
  script will hang the *entire* ESP indefinitely past its timeout (default
  60 minutes, configurable). Check Intune app install status for that
  specific device (Devices → the device → Managed apps / Device install
  status) rather than assuming it's a general Autopilot fault.
- `<PROGRAMDATA>\Microsoft\IntuneManagementExtension\Logs\IntuneManagementExtension.log`
  and `AgentExecutor.log` on the device (accessible via the ESP's own
  "collect logs" option if it offers one, or after boot if it eventually
  completes) show the actual Win32 app install failure — exit code and
  detection-rule mismatch are the two most common findings.
- If ESP is set to "Allow users to reset device if installation error
  occurs" (recommended default), a genuinely stuck device can self-reset
  from that screen without a full reimage — try that before escalating.
- Timeout tuning: raising the ESP timeout fixes "legitimately slow app
  installs on a cold network" but masks a broken blocking app for longer
  — fix the underlying app detection logic instead of just extending the
  clock when the same app always lands near the timeout.

## Hybrid Azure AD / Entra hybrid join failures
- Hybrid join needs line-of-sight to an on-prem domain controller (VPN or
  on-site network) *before* the join step, and Entra Connect syncing the
  device object back from on-prem AD to Entra ID — a device that joined
  on-prem AD successfully but never appears "Hybrid Azure AD joined" in
  `dsregcmd /status` usually means the sync hasn't run yet (default Entra
  Connect delta sync cycle, typically every 30 min) or the device is
  outside VPN range for the job that completes the handshake.
- Run `dsregcmd /status` on the device itself: check `AzureAdJoined`,
  `DomainJoined`, and `EnterpriseJoined` fields — a device showing
  `DomainJoined: YES` but `AzureAdJoined: NO` after hours is the sync
  issue above, not an Autopilot config problem; escalate to whoever owns
  Entra Connect rather than re-running Autopilot.
- Pure Entra-joined (cloud-native, no on-prem AD) avoids this whole class
  of failure — note in the ticket if a hybrid issue recurs often enough
  that migrating the Autopilot profile to Entra-joined is worth proposing.

## White Glove / pre-provisioning
- White Glove runs the device-setup phase at the depot/IT bench before
  shipping, so the end user's OOBE only does account setup — a device
  that fails during White Glove at the bench needs the same ESP log
  triage above; don't ship a device that failed White Glove hoping it
  "finishes at the user's desk", it won't retry the blocking phase
  automatically in the same way.

## Gotchas
- Re-registering a hash for a device already Autopilot-registered under
  a different profile (e.g. moved from one group/OU to another) can
  require removing the old registration first — duplicates sometimes
  cause the *wrong* profile to apply silently rather than an error.
- A factory reset or `systemreset` from Settings keeps Autopilot
  registration (that's the model's home tenant, not local state) — a
  wiped device will re-run Autopilot on next OOBE; a local account bypass
  (Shift+F10 exploits, now largely patched) does not remove the
  registration either.
- `Get-WindowsAutoPilotInfo` needs to run elevated and needs the TPM
  readable — a device with TPM disabled in firmware won't produce a
  usable hash; check firmware settings before assuming the script is
  broken.

## Verify
- Device appears in Intune Autopilot devices list with the correct
  profile and group tag, completes ESP within the configured timeout with
  all blocking apps showing "Installed" in device install status, and
  `dsregcmd /status` (hybrid) or the Entra sign-in (cloud-native) shows
  the expected join state post-OOBE.
