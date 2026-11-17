---
id: computing-software.it-support-helpdesk.intune-mdm.defender-for-endpoint-onboarding-edr-and-device-control
name: defender-for-endpoint-onboarding-edr-and-device-control
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, mde-onboarding, edr-policy, device-control, defender-for-endpoint, removable-storage, endpoint-security]
level: practitioner
status: docs-checked
description: "Onboard devices to Defender for Endpoint via Intune: connector, EDR policy and package types, offboarding, risk-based compliance, device control scope and events."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/protect/advanced-threat-protection-configure"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/endpoint-security-edr-policy"
  - "https://learn.microsoft.com/en-us/defender-endpoint/device-control-overview"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defender-for-endpoint-onboarding-edr-and-device-control

## Connect Intune and Defender for Endpoint (one time per tenant)
1. Check Intune admin center > Endpoint security > Defender for Endpoint: Connection status Enabled means done; Unavailable means continue.
2. Defender portal (security.microsoft.com) > System > Settings > Endpoints > General > Advanced features: set **Intune connection** to On and Save preferences. The status can take up to 15 minutes to update. Needed roles: Endpoint Security Manager (or equivalent Mobile Threat Defense rights) in Intune and Security Administrator in Entra (or the Defender manage-security-settings permission).
3. Under Compliance policy evaluation, turn on Connect Android / iOS/iPadOS / Windows devices to Defender for Endpoint; under App protection policy evaluation the Android and iOS/iPadOS toggles. Since August 2023 Intune no longer creates classic Conditional Access policies for this integration; legacy ones can be deleted.
4. The tenant connector page is also reachable at Tenant administration > Connectors and tokens > Microsoft Defender for Endpoint.

## Onboard by platform
- **Windows**: Endpoint security > Endpoint detection and response (EDR). Quick setup: EDR Onboarding Status tab > Deploy preconfigured policy (all devices, default scope tag). Custom: Summary tab > Create Policy > Windows > Endpoint detection and response, then choose the client configuration package type: **Auto from connector** (recommended) or **Onboard** (paste the onboarding blob, for no connector, multiple tenants or air-gapped environments). Sample sharing: All or None. Telemetry Reporting Frequency is deprecated and does not affect new devices. Assign to device groups (user groups need a sign-in first). Onboarding is one time per device.
- **macOS and Linux**: EDR profile with device tags (name and value pairs). macOS also needs the Defender app deployed and app configuration per Microsoft's macOS guide; Intune provides no automatic onboarding package for macOS.
- **Android and iOS/iPadOS**: deploy the Defender app and follow the platform guides. For supervised iOS/iPadOS, an app configuration policy (Apps > App configuration policies > Add > Managed devices, targeted app Microsoft Defender for Endpoint) with key `issupervised`, type String, value `{{issupervised}}`.
- **Windows Server 2012 R2 and later**: via Configuration Manager tenant attach (Windows (ConfigMgr) platform; assign to collections, not Entra groups) or Defender security settings management.
- Onboarding only starts telemetry; it does not configure ASR, firewall or antivirus policy. Do not mix EDR policy and device configuration policy for the same onboarding setting (conflicts).

## Check and troubleshoot
- Policy status: EDR policy > Device status. Fleet view: EDR Onboarding Status tab (Defender sensor state Active, Inactive, Impaired; onboarding status Onboarded, Not onboarded, Pending). Devices should appear in the Defender portal device inventory, typically after 15-30 minutes.
- Not appearing: check the device can reach the Defender service endpoints (for example `*.securitycenter.windows.com`), the policy status, and that the Defender service is running. "Auto from connector" missing: confirm the connection shows Connected, allow up to 15 minutes, and check permissions.
- Offboarding: download an offboarding package from Defender portal Settings > Endpoints > Device management > Offboarding (Mobile Device Management / Microsoft Intune); it expires seven days after download. It disables the sensor but does not remove the client; the device shows inactive after seven days, and history stays until retention expires.

## Risk-based access
Compliance policy (Android Enterprise, iOS/iPadOS, Windows): Microsoft Defender for Endpoint > Require the device to be at or under the machine risk score, with Clear, Low, Medium or High. The page recommends Low as a balance. Pair it with a Conditional Access policy requiring compliant devices; create it Report-only first and review sign-in logs after about 24 hours, and exclude break-glass accounts.

## Device control (removable storage and other peripherals)
- Scope: Defender device control applies to Windows 10 or 11 with anti-malware client 4.18.2103.3 or later (servers are not supported; macOS has its own device control). It can restrict Windows Portable Devices, removable media (a device that creates a disk), CD/DVDs and printers, by device, device type, operation (read, write, execute), user group, network location or file type. Managed with Intune, the Defender portal or Group Policy. Follow "Configure device control with Microsoft Intune" for the exact profile; the cited pages do not give the Intune menu path.
- From 4.18.2205 the default enforcement extends to printers: a default Deny also blocks printers, so create a custom allow rule for printers if you only mean to manage storage.
- Some physical devices create several entries (for example removable media and portable device): grant access to all of them.
- Windows device installation restrictions (by device ID, instance ID or setup class, via ADMX in Intune or Group Policy) are the coarser option; BitLocker can deny write unless the media is encrypted; Endpoint DLP controls copying by file sensitivity.
- Events (advanced hunting, `DeviceEvents`): `ActionType == "RemovableStoragePolicyTriggered"` for audited device control policy hits (policy, access, verdict, VID, PID, serial); `PnPDeviceBlocked` and `PnPDeviceAllowed` for installation restrictions.

## Verify
Devices show Onboarded in the EDR Onboarding Status report and appear in the Defender portal inventory; a test removable drive behaves per policy and the matching hunting event appears.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Intune pages advanced-threat-protection-configure and endpoint-security-edr-policy and the Defender device-control-overview (all read in full). Removed because the cited pages do not support them: the Sense service and registry OnboardingState check, macOS profile list details, the Attack surface reduction device control profile path and settings-group design, the "Removable Storage Access" template claim, the third-party AV passive-mode pitfall and the broad-class keyboard pitfall.
