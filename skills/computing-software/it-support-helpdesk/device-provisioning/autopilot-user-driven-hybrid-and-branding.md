---
id: computing-software.it-support-helpdesk.device-provisioning.autopilot-user-driven-hybrid-and-branding
name: autopilot-user-driven-hybrid-and-branding
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, autopilot-user-driven, intune-connector-for-ad, oobe-company-branding, autopilot, hybrid-join, entra-branding]
level: practitioner
status: draft
description: "Set up Windows Autopilot user-driven mode for Entra join and hybrid join with the Intune Connector for AD, and brand the OOBE sign-in with company branding."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/user-driven"
  - "https://learn.microsoft.com/en-us/autopilot/windows-autopilot-hybrid"
  - "https://learn.microsoft.com/en-us/entra/fundamentals/how-to-customize-branding"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# autopilot-user-driven-hybrid-and-branding

## User-driven mode (Entra join)
- Flow: device powers on > connects to network > downloads Autopilot profile > tenant-
  branded sign-in > user signs in with MFA > Entra join + Intune enrollment > Enrollment
  Status Page (ESP) installs blocking apps/policies > desktop.
- Profile settings: deployment mode **User-driven**, join type **Microsoft Entra
  joined**, user account type Standard, hide EULA/privacy/change account options,
  device name template (e.g. `CON-%SERIAL%`, max 15 chars), language/region or
  "operating system default", "Convert all targeted devices to Autopilot" if wanted.
- ESP: keep blocking apps few (security agent, VPN, M365 Apps); a 60-minute timeout with
  20 apps means failures.

## Hybrid Entra join with the Intune Connector for AD
Microsoft recommends Entra join for new devices; hybrid only when on-premises
dependencies force it.
- Install the **Intune Connector for Active Directory** (current version uses a managed
  service account) on a domain-joined server with line of sight to a DC. Install two for
  redundancy. The connector creates computer objects in the OU named in the **Domain
  Join** configuration profile.
- Delegate the connector account rights to create computer objects in that OU.
- Autopilot profile: join type **Microsoft Entra hybrid joined**; optional "Skip AD
  connectivity check" when using VPN-at-OOBE solutions.
- The device must reach a DC during OOBE (on-premises network or a VPN that connects
  pre-logon); otherwise the first user sign-in fails.
- Troubleshoot: connector logs (Event Viewer > Applications and Services Logs >
  Microsoft > Intune > ODJConnectorService), ODJ blob errors, OU permissions, and device
  sync to Entra (Entra Connect must sync the OU).

## Company branding in OOBE
- Entra admin center > User experiences > **Company branding**: banner logo, square
  logo, background image, sign-in page text, username hint. Locale-specific branding.
- Autopilot shows the branding (and the "Welcome to <Organization>" page) only after the
  device is registered and the profile assigned; unbranded sign-in means profile not
  downloaded: check network and registration.
- Sign-in page text: a support phone number helps users stuck at OOBE.

## Verify
A registered device shows branded sign-in, completes ESP, and lands Entra joined (or
hybrid joined with the computer object in the right OU) with the expected name.
