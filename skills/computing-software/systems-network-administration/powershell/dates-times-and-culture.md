---
id: computing-software.systems-network-administration.powershell.dates-times-and-culture
name: dates-times-and-culture
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-data, get-date, datetime, timespan, datetimeoffset, culture, utc, filetime, parseexact]
level: practitioner
status: verified
description: "Handle dates correctly in PowerShell: Get-Date formats, UTC vs local, ParseExact, culture traps, TimeSpan math, AD FILETIME values and time zones."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-date
  - https://learn.microsoft.com/en-us/dotnet/standard/base-types/custom-date-and-time-format-strings
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dates, times and culture

## Formatting
```powershell
Get-Date -Format 'yyyy-MM-dd_HHmmss'      # file names: sortable, no colons
Get-Date -Format o                        # ISO 8601 round-trip: 2026-10-16T03:12:44.1234567+10:00
(Get-Date).ToUniversalTime().ToString('u')# 2026-10-16 17:12:44Z
Get-Date -UFormat %s                      # Unix epoch seconds as a STRING; 5.1 gives a decimal and is shifted by the local UTC offset (a +10:00 machine was 36000 s off), so prefer the next line
[DateTimeOffset]::Now.ToUnixTimeSeconds()
```
`MM` is month, `mm` is minutes; `HH` is 24-hour, `hh` 12-hour. `-Format` returns a **string**.

## Parsing: be explicit
```powershell
[datetime]::ParseExact('16/10/2026 14:05', 'dd/MM/yyyy HH:mm', [cultureinfo]::InvariantCulture)
[datetime]'2026-10-16'                    # cast always uses InvariantCulture (US order for 10/11/2026!)
Get-Date '16/10/2026'                     # uses the CURRENT culture - differs per server
```
- A PowerShell cast `[datetime]'10/11/2026'` is **October 11** regardless of locale. Cmdlet
  parameters and `Get-Date -Date` use current culture. Prefer ISO `yyyy-MM-dd` everywhere.
- `-lt`/`-gt` between a `[datetime]` and a string converts the string with invariant culture.

## UTC vs local
- Store and compare in UTC; display in local. `(Get-Date).ToUniversalTime()`, `[datetime]::UtcNow`.
- `[datetime]` has `.Kind` (Utc/Local/Unspecified); `[DateTimeOffset]` keeps the offset
  explicitly and is safer across DST changes and servers in different zones.
- Convert zones: `[TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([datetime]::UtcNow, 'AUS Eastern Standard Time')`.
  List IDs with `Get-TimeZone -ListAvailable`.

## TimeSpan arithmetic
```powershell
$age = (Get-Date) - $file.LastWriteTime        # TimeSpan
$age.TotalDays                                 # fractional; .Days is the whole-days component only
New-TimeSpan -Start $boot -End (Get-Date)
(Get-Date).AddDays(-90).Date                   # midnight 90 days ago
Measure-Command { ... } | Select-Object TotalSeconds
```

## AD and Windows timestamps
```powershell
[datetime]::FromFileTime($u.lastLogonTimestamp)      # FILETIME (100ns since 1601) -> local
[datetime]::FromFileTimeUtc($u.pwdLastSet)
(Get-Date).AddDays(-90).ToFileTime()                 # for LDAP filters: "lastLogonTimestamp<=$ft"
```
`accountExpires` of 0 or 9223372036854775807 means "never". `lastLogonTimestamp` replicates
with up to ~14 days lag; `lastLogon` is per-DC and does not replicate.

Run on 5.1 and 7.6.7 (en-US and en-GB): `-Format` returns a String; `o`, `u` and `ParseExact` outputs; `[datetime]'10/11/2026'` is 11 October under en-GB; `Get-Date '10/11/2026'` is 10 November under en-GB and `Get-Date '16/10/2026'` throws under en-US; comparing a datetime with `'17/10/2026'` throws (invariant); `AUS Eastern Standard Time` is a valid ID; `.Days` is 2 for 50 hours while `.TotalDays` is 2.083; `FromFileTime` gives Kind Local and `FromFileTimeUtc` Utc.

AD attribute facts (Microsoft Win32 AD schema pages): `accountExpires` 0 or 0x7FFFFFFFFFFFFFFF means never expires; `lastLogonTimestamp` is only updated when older than `msDS-LogonTimeSyncInterval` (initial update 14 days minus a random share of 5 days); `lastLogon` is not replicated. The FILETIME conversions were run on literal numbers, not on AD objects.

## Verify
- [ ] Scripts produce identical results on servers with en-US and en-GB regional settings.
- [ ] Logged timestamps include an offset or are UTC.
