---
id: computing-software.it-support-helpdesk.device-provisioning.autopilot-pre-provisioning-technician-flow
name: autopilot-pre-provisioning-technician-flow
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, autopilot-pre-provisioning, white-glove, autopilot, tpm-attestation, esp]
level: practitioner
status: draft
description: "Run Autopilot pre-provisioning on the bench: requirements, the five-Windows-key flow, what installs in the technician phase, reading green/red results, and resealing for the user."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/pre-provision"
  - "https://learn.microsoft.com/en-us/autopilot/requirements"
  - "https://learn.microsoft.com/en-us/autopilot/troubleshooting-faq"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# autopilot-pre-provisioning-technician-flow

## Requirements
- Device registered in Autopilot with a user-driven profile that has "Allow
  pre-provisioned deployment" = Yes.
- TPM 2.0 with attestation support (physical devices; VMs do not work), wired network
  preferred, and access to the TPM attestation endpoints.
- ESP configured; apps and policies meant for the bench phase assigned to **devices**.

## Technician flow
1. Power on to OOBE (first screen). Press the **Windows key 5 times**.
2. Choose **Pre-provision with Windows Autopilot**, Next. The screen shows the profile,
   group tag, assigned user, and a QR code; confirm they are right.
3. **Provision**. Device joins Entra (or hybrid), enrols, and installs device-targeted
   policies, certificates and apps under ESP.
4. **Green screen**: success. Click **Reseal**; the device shuts down, ready to ship.
   **Red screen**: failure; View diagnostics, or Reset to start again.

## User phase
User powers on, signs in, and only user-targeted apps and policies install, so first
logon is short.

## Troubleshooting
- Red screen with TPM attestation error: update firmware/TPM, check the clock, and allow
  network access to the attestation service.
- ESP timeouts: an app that waits for a user, a large app over slow network, or a Win32 app
  with a broken detection rule. Logs: `mdmdiagnosticstool.exe -area Autopilot -cab
  <file>.cab` and the IME log (see intune-management-extension-logs).
- Hybrid join pre-provisioning needs line of sight to a DC and the Intune Connector for AD.

## Gotchas
- User-targeted required apps do not install in the technician phase; target device
  groups for what must be there on day one.
- Apps that require a user context in their installer fail in the system phase.
- Reseal only after the green screen; powering off mid-flow means starting again.

## Verify
Green screen, Reseal completed, device shows as enrolled in Intune with no primary user
yet, and the user's first sign-in finishes within the ESP user phase timeout.
