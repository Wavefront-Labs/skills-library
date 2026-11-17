---
id: computing-software.it-support-helpdesk.intune-mdm.configmgr-co-management-workloads
name: configmgr-co-management-workloads
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, co-management, co-management-workloads, configuration-manager, configmgr, sccm, workload-sliders, pilot-collection, cloud-attach]
level: advanced
status: docs-checked
description: "Support ConfigMgr co-management: prerequisites, the seven workloads, the Configuration Manager / Pilot Intune / Intune sliders, pilot collections, and workload side effects."
sources:
  - "https://learn.microsoft.com/en-us/mem/configmgr/comanage/overview"
  - "https://learn.microsoft.com/en-us/mem/configmgr/comanage/workloads"
  - "https://learn.microsoft.com/en-us/mem/configmgr/comanage/how-to-switch-workloads"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# configmgr-co-management-workloads

Co-management means a Windows device with the Configuration Manager client is also
enrolled in Intune. You choose per **workload** which tool is authoritative; ConfigMgr
keeps managing every workload you do not switch, plus features co-management does not
support. Managing with ConfigMgr plus a third-party MDM is "coexistence", not co-management.

## Prerequisites (overview page)
- Microsoft Entra ID P1 or P2 (an EMS subscription includes it and Intune), and an Intune
  licence on the admin account that signs in to the Intune admin center.
- A supported Configuration Manager current branch; several instances can connect to one
  Intune tenant.
- Devices must be Microsoft Entra hybrid joined or Entra joined only. Devices that are
  only Entra registered (workplace joined) are not supported.
- Intune set up and Windows automatic enrollment enabled; an Intune-supported Windows
  version.
- Roles: enabling co-management needs a Microsoft Entra user who is a Configuration
  Manager Full Administrator with All scope rights; creating Entra apps from ConfigMgr
  needs Global Administrator; a cloud management gateway (needed for internet-based
  clients, not for co-management itself) needs an Azure Subscription Manager.

## Workloads
Supported: compliance policies, Windows Update policies, resource access policies,
Endpoint Protection, device configuration, Office Click-to-Run apps, client apps.
- **Compliance policies**: define what makes a device compliant for Conditional Access;
  can include custom configuration baselines as an assessment rule.
- **Windows Update policies**: after moving, adjust ConfigMgr client settings manually
  (modify or create a custom client setting that disables the software update workflow).
  Windows Autopatch needs this workload in Intune with the Software Updates client setting
  set to "No".
- **Resource access policies** (VPN, Wi-Fi, email, certificates): the ConfigMgr feature and
  workload stopped being supported from version 2203; the policies follow the Device
  Configuration slider, and from version 2403 the node is removed from the console and the
  slider is fixed to Intune.
- **Endpoint Protection**: Defender suite including Antivirus, SmartScreen, Firewall and
  BitLocker. ConfigMgr policies stay on the device until Intune policies overwrite them.
  Defender Antivirus settings in the Device restrictions profile are outside this slider;
  use Endpoint security > Antivirus policy.
- **Device configuration**: switching it also moves Resource Access and Endpoint
  Protection. A settings catalog policy follows this slider whatever it contains. A
  ConfigMgr baseline can still apply with "Always apply this baseline even for co-managed
  clients". Removing Endpoint Protection settings needs this workload switched too.
- **Office Click-to-Run apps**: apps show in the Company Portal after the move; Office
  updates may take about 24 hours to show unless devices restart. A global condition on new
  Microsoft 365 apps (version 2111+: "Microsoft 365 apps managed by Microsoft Intune")
  stops ConfigMgr installs on co-managed clients after transition.
- **Client apps**: Intune apps appear in the Company Portal, ConfigMgr apps in Software
  Center. On Windows 10 1903+ PowerShell scripts still run even if this workload is not
  switched. Deploying winget Store apps through Intune needs this workload switched.

## Switching
ConfigMgr console > Administration > Cloud Services > **Cloud Attach** (the
**Co-management** node in version 2103 and earlier) > select the object > Properties >
**Workloads** tab. By default all sliders are at Configuration Manager.
- **Configuration Manager**: ConfigMgr manages it.
- **Pilot Intune**: only devices in that workload's pilot collection switch; set the
  collections on the **Staging** tab (a different collection per workload is allowed).
- **Intune**: all Windows devices enrolled in co-management.
- With Pilot Intune on Endpoint Protection or Device Configuration, Intune deploys
  policies but does not remove them on unassignment; policy removal needs the full
  Intune setting.
- Configure and deploy the workload in Intune before switching, so each workload always
  has a manager. Switching triggers an MDM policy sync. A workload can be switched back,
  though Windows or Office versions installed by Intune stay at the later version.

## Support triage: which tool owns this?
Check the slider for that workload, the device's pilot collection membership, and whether
the device is in the co-management dashboard before editing either tool's policy.
Co-management does not manage remotely connected PCs by itself; the client still needs to
reach its site (a cloud management gateway helps).

## Checked
Date: 2026-11-07. Read in full: co-management overview (prerequisites, roles, workloads), co-management workloads page, and
"How to switch Configuration Manager workloads to Intune". Removed as unconfirmed or contradicted: the claim that resource access
is "folded into device configuration in current builds" without the 2203/2403 detail, the slider table's one-line consequences, the
"Automatic enrollment in Intune: Pilot or All" step, `CoManagementHandler.log`, the Configuration Manager control panel applet
path, the "Pilot collections must contain the device, not the user" and "Co-management: enrolled ConfigMgr only" claims, the
tenant attach note, the lingering-settings claim for sliders in general (kept only for Endpoint Protection), and the Verify step.
Method: documentation only; no commands were run.
