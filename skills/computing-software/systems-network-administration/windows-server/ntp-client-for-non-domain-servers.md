---
id: computing-software.systems-network-administration.windows-server.ntp-client-for-non-domain-servers
name: ntp-client-for-non-domain-servers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [w32time, ntp-client-windows, w32tm-config, time-skew, windows-time-service]
level: practitioner
status: docs-checked
description: "Configure Windows Time as an NTP client on workgroup, DMZ and edge servers: manual peers, flags, poll intervals, firewall and verification."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-time-service-tools-and-settings
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/configuring-systems-for-high-accuracy
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/configure-authoritative-time-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTP client for non-domain servers

Domain members follow the domain hierarchy. Workgroup machines (DMZ web servers, appliances on Windows, bastions)
default to `time.windows.com` with a SpecialPollInterval of 604800 s (weekly), which can drift.

## Configure
```cmd
w32tm /config /manualpeerlist:"ntp1.corp.example.com,0x8 ntp2.corp.example.com,0x8" /syncfromflags:manual /update
net stop w32time && net start w32time
w32tm /resync /rediscover
```
Flags: `0x1` = SpecialInterval (use SpecialPollInterval), `0x2` = UseAsFallbackOnly, `0x4` = SymmetricActive,
`0x8` = Client mode; combine by adding (`0x9` = SpecialInterval plus Client). Without `0x1` on a peer, some
authoritative-server procedures say the SpecialPollInterval change will not take effect.

With 0x1 set, polling uses `SpecialPollInterval` (seconds) under
`HKLM\SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpClient`; default on stand-alone is 604800 (1 week)
and 3600 on domain members. From build 1703 the value is bounded by Config MinPollInterval and MaxPollInterval, so
raise a low MaxPollInterval if needed. Example:
```cmd
reg add HKLM\SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpClient /v SpecialPollInterval /t REG_DWORD /d 3600 /f
```
Without 0x1, the client uses MinPollInterval/MaxPollInterval (log2 seconds; stand-alone defaults 10 and 15).

## Service start
Microsoft's high-accuracy guidance is to set the Windows Time service startup type to Automatic so it runs continuously:
```cmd
sc config w32time start= auto
```

## Firewall
UDP 123 outbound to the NTP servers (the NTP client needs UDP 123 as its source port).

## Hyper-V guests
Check which time source the guest reports with `w32tm /query /source`; a Hyper-V integration provider as the
source means NTP is not authoritative.

## Verify
```cmd
w32tm /query /status
w32tm /query /peers
w32tm /stripchart /computer:ntp1.corp.example.com /samples:5 /dataonly
```
- [ ] Source shows your NTP server (not Local CMOS Clock or a VM provider) and the stripchart offset is small.

## Checked

2026-10-27. Documentation release: windowsserverdocs Windows Time Service Tools and Settings (current), Configuring systems for high accuracy (2025-02-25) and the authoritative time server article. Confirmed: /config /manualpeerlist /syncfromflags /update syntax, /resync /rediscover, NtpServer flag bits, SpecialPollInterval defaults and the build 1703 bounding note, poll interval defaults, Automatic startup recommendation, UDP 123 source port. Removed the trigger-start claim, the quoted event text, the Hyper-V disable advice and the 100 ms threshold, which no fetched page covers.

Method: documentation only; no commands were run.
