---
id: computing-software.it-support-helpdesk.intune-mdm.bulk-enrollment-with-provisioning-packages
name: bulk-enrollment-with-provisioning-packages
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, provisioning-package, windows-configuration-designer, ppkg, bulk-enrollment, bulk-token, shared-devices, windows-enrollment]
level: practitioner
status: docs-checked
description: "Bulk-enroll Windows devices in Intune with a Windows Configuration Designer provisioning package: bulk token, roles, applying in OOBE or Settings, and failure points."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/windows-bulk-enroll"
  - "https://learn.microsoft.com/en-us/windows/configuration/provisioning-packages/provisioning-packages"
  - "https://learn.microsoft.com/en-us/windows/configuration/provisioning-packages/provisioning-apply-package"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bulk-enrollment-with-provisioning-packages

Bulk enrollment joins corporate-owned Windows devices to Microsoft Entra ID and enrolls
them in Intune using a **provisioning package** (`.ppkg`) made in **Windows Configuration
Designer** (WCD, from the Microsoft Store). Once applied, the device is ready for Entra
users to sign in; they are standard users and receive assigned Intune policies and
required apps.

## Tenant prerequisites
- Windows automatic enrollment is enabled.
- The service principal for Microsoft.Azure.SyncFabric (AppID
  `00000014-0000-0000-c000-000000000000`) exists in the tenant. Without it WCD cannot
  retrieve the bulk enrollment token and errors. Check with
  `Get-MgServicePrincipal -Filter "AppId eq '00000014-0000-0000-c000-000000000000'"`;
  register with `New-MgServicePrincipal -AppId "00000014-0000-0000-c000-000000000000"`.
- The account that requests the token holds Cloud Device Administrator, Intune
  Administrator or Password Administrator, and is not scoped to an administrative unit.
- That account is in the MDM user scope in Entra; removing it from the scoped group stops
  bulk enrollment working.

## Build the package
1. Install WCD and choose **Provision desktop devices**; name the project.
2. Set a unique device name (can include `%SERIAL%` or random characters); optionally a
   product key, shared use, and removal of pre-installed software.
3. Optionally configure Wi-Fi. Without it, a wired connection is needed at first start.
4. Select **Enroll in Azure AD**, enter a **Bulk Token Expiry** date, select **Get Bulk
   Token**. The page states the token validity period is 90 days.
5. Sign in by password or certificate-based authentication only; other methods are not
   supported by the app for this operation. Bulk token retrieval does not work for
   federated accounts enabled for staged rollouts.
6. At "Stay signed in to all your apps" choose **No, sign in to this app only**; otherwise
   the device you are using becomes managed.
7. Optionally add applications and certificates, and password-protect the package, then
   **Create**.

## Apply
- **Initial setup (OOBE)**: insert the USB drive at the initial setup screen; if nothing
  happens, press the Windows key five times. With several packages on the drive, choose
  **Install provisioning package**. If the device is past that screen, reset it first.
- **After setup**: Settings > Accounts > Access work or school > Add or remove a
  provisioning package > Add a package; or double-click the `.ppkg`. Both need
  administrator rights and a UAC prompt, then confirm the package is trusted.
- The device restarts automatically after one minute, then connects to Entra ID and
  enrolls in Intune. `Install-ProvisioningPackage` accepts `-LogsDirectoryPath` to capture
  logs for the operation.

## Behaviour and failure points
- Revoke a package before expiry by removing its `package_{GUID}` user account from Entra.
- That account cannot do MFA: tenants with Conditional Access requiring MFA must exclude
  it or disable MFA for this process.
- Bulk enrollment is userless, so only the **Default** enrollment restriction applies;
  Windows must be allowed there or enrollment fails.
- Conditional Access is available for bulk-enrolled Windows 11 and Windows 10 1803+.
- On a non-open Wi-Fi network use device-level certificates; bulk-enrolled devices cannot
  use user-targeted certificates for network access.
- Provisioning suits new devices. A package that joins a domain or tenant without creating
  a local account can leave the device unreachable if the join fails for lack of network.
  Package scripts run in system context; a bad script may need a wipe or reimage.
- Per-setting success or failure is in the Provisioning-Diagnostics-Provider Admin log in
  Event Viewer. Pressing ESC interrupts a long-running provisioning.

## Checked
Date: 2026-11-07. Read in full: Intune "Bulk enrollment for Windows devices" (requirements, create package, provision,
troubleshooting), "Provisioning packages for Windows" and "Apply a provisioning package". Removed as unconfirmed: the
180-day maximum token validity (page says 90 days), the claim that devices have no primary user and user-targeted policies
do not apply (page says Entra users get assigned policies and apps), the claim that the join quota does not apply,
`-QuietInstall`, the `<WINDIR>\Provisioning\Logs` path, "Company Portal shows no user" (page says Company Portal can
install apps), the `dsregcmd` Verify step and the "Bulk enrollment" enrollment-type label. Added the service principal,
role and MDM user scope prerequisites.
Method: documentation only; no commands were run.
