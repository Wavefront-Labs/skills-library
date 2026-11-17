---
id: computing-software.systems-network-administration.active-directory.domain-time-hierarchy-nt5ds
name: domain-time-hierarchy-nt5ds
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, w32time, windows-time-service, nt5ds, w32tm-monitor, domhier, time-hierarchy, w32tm-query, specialpollinterval, member-server-time]
level: practitioner
status: docs-checked
description: "How domain members get time (NT5DS hierarchy), checking every DC with w32tm /monitor and /query, fixing machines that drifted to manual sources, and poll intervals."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/how-the-windows-time-service-works
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-time-service-tools-and-settings
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/maximum-tolerance-for-computer-clock-synchronization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain time hierarchy (NT5DS)

## The chain
The PDC emulator of the forest root domain is the authoritative time source for the forest and should be configured to
gather time from an external source. PDC emulators of other domains, DCs and members follow the domain hierarchy to
choose an inbound time partner. Domain members and DCs use type **NT5DS** (`/syncfromflags:domhier`), which is the
default on domain members. Nobody but the forest-root PDC should have a manual peer list.

## Check the estate
```cmd
w32tm /monitor /domain:ad.example.com /threads:5    :: every DC in the domain
w32tm /query /status /verbose                       :: on a host: source, stratum, last sync, poll
w32tm /query /source
w32tm /query /configuration                         :: Type (NT5DS/NTP), providers
w32tm /stripchart /computer:dc01 /samples:5 /dataonly
```

## Fix a member that drifted to a manual source
```cmd
w32tm /config /syncfromflags:domhier /update
net stop w32time & net start w32time
w32tm /resync /rediscover
```
If config does not stick, a GPO is setting it: check *Administrative Templates > System > Windows Time Service >
Time Providers > Configure Windows NTP Client* in `gpresult`.

## Accuracy notes
- Kerberos tolerates clock skew up to the policy *Maximum tolerance for computer clock synchronization*; Microsoft
  advises 5 minutes. That is the default accuracy target, not milliseconds.
- For tighter accuracy needs, follow Microsoft's "Configuring systems for high accuracy" guidance; virtual DCs need
  their host time integration handled (see the virtual DC time skill).
- Stand-alone (workgroup) machines default to type NTP with `time.windows.com`.

## Verify
- [ ] `w32tm /monitor` lists every DC with an offset inside your tolerance and none in error.
- [ ] Sample members report a DC as source (`w32tm /query /source`), not a manual peer.

## Checked
2026-10-27. Documentation: Microsoft Learn How the Windows Time Service Works, Windows Time Service Tools and
Settings, FSMO roles article and the Kerberos clock-skew policy page. Confirmed: forest-root PDC emulator is the
authoritative source and should use an external source; all PDC emulators follow the domain hierarchy; default type on
domain members is NT5DS and NTP on stand-alone machines (`time.windows.com`); `w32tm /monitor [/domain /computers
/threads]`, `/query {/source|/configuration|/peers|/status} [/verbose]`, `/stripchart`, `/config /syncfromflags`, `/resync
/rediscover`; the Configure Windows NTP Client policy path; 5 minutes advised for Kerberos clock tolerance. Removed as
unconfirmed: the 45-minute poll statement, the 1 s/50 ms targets and the Local CMOS and free-running clock strings.
Method: documentation only; no commands were run.
