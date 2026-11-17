---
id: computing-software.it-support-helpdesk.intune-mdm.byod-entra-registration-windows
name: byod-entra-registration-windows
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, entra-registered-byod, entra-registered, workplace-join, access-work-or-school, byod, windows-enrollment]
level: practitioner
status: docs-checked
description: "Support Windows BYOD Entra registration: registered vs joined, registration vs Intune enrollment, Company Portal enrollment steps and reading WorkplaceJoined in dsregcmd."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/devices/concept-device-registration"
  - "https://learn.microsoft.com/en-us/mem/intune/user-help/enroll-windows-10-device"
  - "https://learn.microsoft.com/en-us/entra/identity/devices/troubleshoot-device-dsregcmd"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# byod-entra-registration-windows

A personal Windows PC used for work is typically **Microsoft Entra registered** (also called
workplace joined), not joined. It is registered with Entra ID without needing a work account
to sign in to the device.

## Registered vs joined
| | Entra registered | Entra joined |
|---|---|---|
| Purpose | BYOD and mobile access to org resources | Organization-owned devices |
| Windows sign-in | A local account such as a Microsoft account; the work account is added for resources | Work account |
| Provisioning on Windows | Settings, or automatically when accessing a work app for the first time | Join flow |
| `dsregcmd /status` | `WorkplaceJoined : YES` in the **User State** section | `AzureAdJoined : YES` in Device State |

Capabilities of a registered device: single sign-on to cloud resources, Conditional Access
when the device is enrolled in Intune, Conditional Access through app protection policy, and
Authenticator phone sign-in. Device ownership can be user or organization.

## Registration is not enrollment
Registering does not enroll the device in MDM. If admins allow users to enroll, registered
devices can then be enrolled in Intune to enforce encryption, password and security software
requirements. Example scenario from Microsoft: a benefits tool requires a compliant device,
so the user registers the home PC and enrolls it in Intune; the policies then give access.
A registered device that is not enrolled cannot be compliant.

## Enrolling a Windows device (user steps)
Windows 10 version 1607 and later or Windows 11, via Company Portal (Windows 10 reached end of
support on 14 October 2025 but is still an allowed Intune version):
1. Open Company Portal and sign in with the work account, then **Next**.
2. **Connect**, sign in again with the work account.
3. On "Setting up your device", select **Go**; then back in Company Portal select **Next**
   and **Done**.
After enrolling, if work access has problems, run a device **Sync**. Microsoft points admins to
"Troubleshooting Windows device enrollment problems in Microsoft Intune" for error codes.

## Reading dsregcmd
- `dsregcmd /status` must run in the user's own context to give valid user state. The
  `WorkplaceJoined` value is YES when Entra registered accounts exist for the current user
  (NTUSER) context.
- Device Details and Tenant Details show only for joined or hybrid joined devices, not for
  registered ones.
- `AzureAdJoined`, `EnterpriseJoined` and `DomainJoined` together define the state:
  YES/NO/NO is Entra joined; YES/NO/YES is hybrid joined.

## Limits and housekeeping
- Entra registered devices do not support the Unified Write Filter.
- Related Microsoft guidance for removing old registrations is "Manage stale devices in
  Microsoft Entra ID".

## Checked
Date: 2026-11-08. Read in full: Entra "Microsoft Entra registered devices" (updated 2025-06-27), Intune user help "Enroll Windows devices in Intune" (updated 2026-04-08), and Entra "Troubleshoot devices by using the dsregcmd command". Removed as unconfirmed: the Office sign-in "Allow my organization to manage my device" checkbox, the MDM-only enrollment link, error codes 8018000a and 80180014, Windows Hello for Business scoping advice, enrollment restriction behaviour, and the Disconnect and stale-device deletion procedures.
Method: documentation only; no commands were run.
