---
id: computing-software.systems-network-administration.windows-server.w32time-registry-tuning
name: w32time-registry-tuning
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, time-service, maxposphasecorrection, w32time, ntp, time-accuracy]
level: advanced
status: docs-checked
description: "Tune W32Time registry values: MaxPos/MaxNegPhaseCorrection, SpecialPollInterval, MinPollInterval and AnnounceFlags, for accurate time and safe big jumps."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-time-service-tools-and-settings
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/configuring-systems-for-high-accuracy
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/configure-authoritative-time-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# W32Time registry tuning

Key: `HKLM\SYSTEM\CurrentControlSet\Services\W32Time` (`\Config`, `\Parameters`, `\TimeProviders\NtpClient`).
Prefer Group Policy (Admin Templates > System > Windows Time Service) for domain machines; GPO values land under
`HKLM\SOFTWARE\Policies\Microsoft\W32Time` and win.

## Values that matter
| Value | Default (domain member) | Meaning |
|---|---|---|
| Config\MaxPosPhaseCorrection / MaxNegPhaseCorrection | 0xFFFFFFFF (member, always correct); 172800 s (DC); 54000 s (stand-alone) | a larger required change is logged as an event instead of applied |
| Config\MinPollInterval / MaxPollInterval | DC 6 / 10; member 10 / 15; stand-alone 10 / 15 (log2 seconds) | poll range; lower = more accurate, more traffic |
| Config\AnnounceFlags | 10 (0xA, default); 5 for the forest-root PDC with external NTP | 0x1 always time server, 0x2 automatic, 0x4 always reliable, 0x8 automatic reliable |
| Config\FrequencyCorrectRate | 4 (0 invalid) | clock correction rate |
| Config\UpdateInterval | DC 100; member 30000; stand-alone 360000 (10 ms units) | interval between phase corrections |
| Parameters\Type | NT5DS (member), NTP (stand-alone); also NoSync, AllSync | sync source type |
| Parameters\NtpServer | stand-alone default `time.windows.com,0x1`; none on members | flags 0x1 SpecialInterval, 0x2 UseAsFallbackOnly, 0x4 SymmetricActive, 0x8 Client |
| NtpClient\SpecialPollInterval | 3600 (member) / 604800 (stand-alone) | poll interval when the 0x1 flag is used; from build 1703 it is bounded by Min/MaxPollInterval |

## High accuracy (1 ms target on Windows 10 / Server 2016 or later)
Microsoft's high-accuracy article lists MinPollInterval 6, MaxPollInterval 6, UpdateInterval 100,
SpecialPollInterval 64 (NtpClient, with the 0x1 flag), FrequencyCorrectRate 2 and UtilizeSslTimeData 0, set W32Time
to start Automatic, and requires every device in the time topology (including Hyper-V hosts) to be Windows 10 or
Server 2016 or later, within the documented support boundary for network latency. UtilizeSslTimeData changes need
a restart.

## Apply
```cmd
reg add HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config /v MaxPosPhaseCorrection /t REG_DWORD /d 3600 /f
w32tm /config /update
w32tm /resync /rediscover
w32tm /query /configuration         REM shows value and source (Local or Policy)
```

## Gotchas
- Large correction limits let a bad NTP source move time a long way; on the PDC root Microsoft suggests a limit
  such as 3600 or 1800 seconds, chosen to suit poll interval, network and source. If the PDC syncs at a fixed
  SpecialPollInterval or has an unreliable upstream link, Microsoft advises AnnounceFlags 0xA rather than 0x5.
- Secure Time Seeding can set huge jumps on boot; see secure-time-seeding.

## Verify
- [ ] `w32tm /query /status` shows the right source and `w32tm /stripchart /computer:<ref> /samples:5 /dataonly` offset is small.

## Checked

2026-10-27. Documentation release: windowsserverdocs Windows Time Service Tools and Settings (current) and Configuring systems for high accuracy (dated 2025-02-25); authoritative time server article (Support Articles). Confirmed per-role defaults for phase correction, poll intervals, UpdateInterval, SpecialPollInterval, NtpServer flags and Type values, AnnounceFlags bits and the 0x5 versus 0xA caveat, and the high-accuracy values. Corrected: the earlier defaults (48 h, 6/10 and UpdateInterval 100 for every role), the 'refused (event 50/52)' wording, the 1 s / 50 ms targets and the Hyper-V claim (removed).

Method: documentation only; no commands were run.
