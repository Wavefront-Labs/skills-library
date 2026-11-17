---
id: computing-software.systems-network-administration.active-directory.pdc-time-gpo-with-wmi-filter
name: pdc-time-gpo-with-wmi-filter
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, w32time, windows-time-service, time-gpo, pdc-wmi-filter, wmi-filter, domainrole-5, ntp-client-policy, group-policy, fsmo]
level: practitioner
status: docs-checked
description: "Make the external NTP config follow the PDC role: a GPO on the DC OU with a DomainRole=5 WMI filter, plus a fallback GPO resetting other DCs to NT5DS."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-time-service-tools-and-settings
  - https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-computersystem
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDC time GPO with a WMI filter

**Problem:** you configure NTP on the PDC manually, then move the PDC role (or seize it) and
the new holder still uses domain hierarchy; the old one is now an unauthorised time source.

## WMI filters
GPMC > WMI Filters > New `PDC emulator only`:
```text
Namespace: root\CIMv2
Query: Select * from Win32_ComputerSystem where DomainRole = 5
```
and `Other DCs`:
```text
Namespace: root\CIMv2
Query: Select * from Win32_ComputerSystem where DomainRole = 4
```
(Win32_ComputerSystem DomainRole: 5 = primary domain controller, 4 = backup domain controller; a DC that does not hold
the PDC emulator role is a backup domain controller.)

## GPO 1: "DC time - PDC" (linked to Domain Controllers OU, filter `PDC emulator only`)
*Computer Configuration > Policies > Administrative Templates > System > Windows Time Service > Time Providers*:
- **Configure Windows NTP Client**: Enabled; NtpServer `time1.example.net,0x8 time2.example.net,0x8`;
  Type `NTP`; SpecialPollInterval e.g. 3600.
- **Enable Windows NTP Client**: Enabled. **Enable Windows NTP Server**: Enabled.
- Also *Global Configuration Settings* > AnnounceFlags if you set it here. AnnounceFlags is a bit mask: 0x01 always time
  server, 0x02 automatic time server, 0x04 always reliable, 0x08 automatic reliable; 5 = 0x01 + 0x04 (always time
  server and always reliable). The Global Configuration default when enabled is 10 (0x02 + 0x08).

## GPO 2: "DC time - others" (linked to Domain Controllers OU, filter `Other DCs`)
- Configure Windows NTP Client: Enabled, Type **NT5DS**, NtpServer blank.
Because each GPO has its own filter, the result does not depend on link order.

Only the **forest root** domain's PDC should use external NTP; child domain PDCs use NT5DS. Link GPO 1 only in the
forest root domain.

## Apply and confirm
```cmd
gpupdate /force
w32tm /query /configuration | findstr /i "Type NtpServer AnnounceFlags"
w32tm /query /source
```

## Verify
- [ ] After a test FSMO transfer in a lab, the new PDC shows external NTP within one GPO refresh.
- [ ] Other DCs show Type NT5DS.

## Checked
2026-10-27. Documentation: Microsoft Learn Windows Time Service Tools and Settings and the Win32_ComputerSystem class
reference. Confirmed: DomainRole 4 = backup domain controller and 5 = primary domain controller; the policy names Global
Configuration Settings, Time Providers > Configure Windows NTP Client, Enable Windows NTP Client and Enable Windows NTP
Server; Type values NTP and NT5DS; the AnnounceFlags bit values and the default of 10 when enabled; SpecialPollInterval
and the `0x8` client flag. Changed: the draft relied on GPO link order to override the filtered GPO on the PDC (the
precedence rule could not be confirmed in readable documentation), so GPO 2 now has its own DomainRole = 4 filter.
Method: documentation only; no commands were run.
