---
id: computing-software.cybersecurity-defensive.endpoint-security.wpd-mtp-device-control
name: wpd-mtp-device-control
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [wpd-device-control, mtp, portable-devices, phone-file-transfer, defender-device-control, removable-storage, device-control]
level: practitioner
status: draft
description: "Block or allow Windows Portable Devices (MTP/PTP phones, cameras) for file transfer: device control policies, WPD group policy, read-only modes and auditing."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/device-control-overview", "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage", "https://learn.microsoft.com/en-us/defender-endpoint/device-control-removable-storage-access-control"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WPD and MTP device control

Phones and cameras connect as Windows Portable Devices (MTP/PTP), not as USB mass storage - so a policy
blocking "removable disks" often lets users copy files to phones.

## Group Policy / Policy CSP (simple block)
- Computer Configuration -> Administrative Templates -> System -> Removable Storage Access:
  - "WPD Devices: Deny read access" / "Deny write access".
- Intune: Settings catalog -> Administrative Templates -> System -> Removable Storage Access (same settings), or `ADMX_RemovableStorage` CSP.
Charging still works when access is denied.

## Defender device control (granular)
- Groups using `PrimaryId` = `WpdDevices` plus vendor/product IDs or serials for approved corporate phones.
- Access masks: read (1), write (2), execute (4) - allow read-only for cameras in specific departments, deny write for everyone else.
- Audit entries (`AuditAllowed`, `AuditDenied`) for visibility.

```xml
<Group Id="{d8819053-24f4-444a-a0fb-9ce5a9e97862}">
  <MatchType>MatchAny</MatchType>
  <DescriptorIdList><PrimaryId>WpdDevices</PrimaryId></DescriptorIdList>
</Group>
<PolicyRule Id="{...}">
  <Name>Block write to portable devices</Name>
  <IncludedIdList><GroupId>{d8819053-24f4-444a-a0fb-9ce5a9e97862}</GroupId></IncludedIdList>
  <Entry><Type>Deny</Type><Options>0</Options><AccessMask>2</AccessMask></Entry>
  <Entry><Type>AuditDenied</Type><Options>3</Options><AccessMask>2</AccessMask></Entry>
</PolicyRule>
```

## Also consider
iPhones also expose Apple Mobile Device services (iTunes sync/backup); Bluetooth file transfer; network
transfers via phone apps - device control covers only the USB path.

## Verify
- [ ] Copying a file to a test phone fails; event `RemovableStoragePolicyTriggered` in advanced hunting.
- [ ] Approved exception devices work as designed.
