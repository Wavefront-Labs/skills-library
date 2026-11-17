---
id: computing-software.systems-network-administration.active-directory.pdc-emulator-time-and-password-role
name: pdc-emulator-time-and-password-role
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, fsmo-roles, pdc-emulator, pdc-time-source, w32time, ntp, ntp-source, w32tm-config, urgent-replication, badpwdcount, account-lockout, avoidpdconwan, gpmc-default-dc]
level: practitioner
status: docs-checked
description: "What the PDC emulator does and how to run it: forest time root with external NTP, password-change forwarding, lockout and bad-password counting, GPMC target."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/how-the-windows-time-service-works
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/fsmo-roles
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/password-change-processing-conflict-resolution-function
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDC emulator: time root and password authority

## Duties
1. **Time:** the PDC emulator of the forest root domain is authoritative for the enterprise and should be configured
   to gather time from an external source. All PDC emulators follow the domain hierarchy in choosing their inbound
   time partner; other DCs and clients sync via NT5DS.
2. **Password changes:** password changes made on other DCs are replicated preferentially to the PDC emulator, and
   when authentication fails on a DC because of an incorrect password the failure is forwarded to the PDC emulator
   before a bad-password error is reported, so a just-changed password works everywhere.
3. **Lockout:** account lockout is processed on the PDC emulator (event 4740, "A user account was locked out").
4. It also does what an NT4 PDC did for NT4-era clients.

## Configure time on the forest-root PDC
```cmd
w32tm /config /manualpeerlist:"time1.example.net,0x8 time2.example.net,0x8" /syncfromflags:manual /reliable:yes /update
net stop w32time & net start w32time
w32tm /resync /rediscover
w32tm /query /status
w32tm /query /source
```
- Use several reliable time sources; the `0x8` flag in a peer entry means client mode.
- On a **virtual** PDC, make sure the hypervisor's time-synchronization integration service is disabled
  (Hyper-V: `Disable-VMIntegrationService`; list the service names with `Get-VMIntegrationService`) so the host clock
  does not override NTP.
- Make it role-follow with a GPO linked to the Domain Controllers OU and a WMI filter
  `Select * from Win32_ComputerSystem where DomainRole = 5` (5 = primary domain controller); see the PDC time GPO skill.

All other DCs: `w32tm /config /syncfromflags:domhier /update` (the default, type NT5DS).

## Password forwarding over WAN
`AvoidPdcOnWan` (`HKLM\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters`, REG_DWORD, 1 = enabled, absent = disabled)
stops a DC from forwarding password changes and failed logons to a PDC emulator in another site. Trade-off: a changed
password is then spread only by normal replication, so a logon that uses it at a branch DC may be denied until
replication delivers it. If the PDC is in the same site the value is not used.

## Verify
- [ ] `w32tm /monitor /domain:<domain>` shows all DCs within your tolerance of the PDC.
- [ ] `w32tm /query /source` on the PDC shows your external peers, not a virtual-machine provider or the local clock.
- [ ] After a password change at one DC, logon at a remote DC works immediately.

## Checked
2026-10-27. Documentation: Microsoft Learn FSMO roles, Windows Time Service (how it works, tools and settings) and
password-change processing articles, plus Appendix L. Confirmed: forest-root PDC emulator is the authoritative time source
and should use an external source; PDC emulator password replication, failure forwarding and lockout duties; `w32tm /config
/manualpeerlist /syncfromflags:manual /reliable:(YES|NO) /update`, `/resync /rediscover`, `/query`, `0x8` client flag;
`AvoidPdcOnWan` is a REG_DWORD (1 = true, absent = false) under Netlogon Parameters and its effect; event 4740; DomainRole 5 is
the primary domain controller (Win32_ComputerSystem). Removed as unconfirmed: the Kerberos five-minute statement here,
the GPMC-targets-the-PDC duty, the browse-master remark, the exact Hyper-V service name and the VM IC provider string.
Method: documentation only; no commands were run.
