---
id: computing-software.systems-network-administration.dns-dhcp.windows-dns-debug-and-analytic-logging
name: windows-dns-debug-and-analytic-logging
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, windows-dns, dns-debug-logging, dns-analytic-log, etw, dnsserver-powershell]
level: practitioner
status: docs-checked
description: "Enable Windows DNS Server debug logging and the ETW analytical log to see queries, responses and updates, with audit events and rollover."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/dns-logging-and-diagnostics
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverdiagnostics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS debug and analytic logging

The Learn article covers Windows Server 2016, 2019, 2022 and 2025. Three logs exist: audit (on by default), analytical (off by default) and the legacy debug text log.

## Audit log
Event Viewer > Applications and Services > Logs > Microsoft > Windows > DNS-Server > Audit. An audit event is logged each time server, zone or resource record settings change. Useful IDs: 515 record create, 516 record delete, 519 and 520 record create/delete via dynamic update (event text includes the source IP address), 521 record scavenge. That answers "who or what deleted this record".

## Analytical (ETW) log
Not enabled by default. Microsoft states it typically only affects performance at high query rates (its example: about 5% degradation at 100,000 queries per second, none apparent at 50,000 or lower) and recommends monitoring performance whenever logging is on.
- In Event Viewer, right-click DNS-Server > View > Show Analytic and Debug Logs, open Analytical > Properties.
- To read events in Event Viewer, choose "Do not overwrite events (Clear logs manually)" then tick Enable logging. For circular logging choose "Overwrite as needed (oldest events first)"; a query error is then shown but logging still happens, you just cannot view the live events there.
- The default file is `%SystemRoot%\System32\Winevt\Logs\Microsoft-Windows-DNSServer%4Analytical.etl`.
- Analytic events include 257 response success, 258 response failure, 259 ignored query, 260 recursive query out, 261 recursive response in, 262 recursive query timeout, 263 and 264 dynamic update in/response, and 265-276 zone transfer events.
- The logs work with ETW consumers such as logman and tracelog; the DNS provider GUID is given on the Learn page.

## Debug log (legacy text)
By default all debug options are disabled. It can be resource intensive and use disk space, so use it temporarily. The default file is `dns.log` in `%windir%\system32\dns`.
```powershell
Get-DnsServerDiagnostics
Set-DnsServerDiagnostics -Queries $true -Answers $true -SendPackets $true -ReceivePackets $true -TcpPackets $true -UdpPackets $true
Set-DnsServerDiagnostics -EnableLogFileRollover $true
```
- `Set-DnsServerDiagnostics -All $true` turns every diagnostic event on and implicitly sets `-EnableLogFileRollover` to true, so a new file is started at maximum size instead of overwriting; many files can accumulate and fill the disk. Prefer enabling individual events.
- `-LogFilePath` sets the file and `-MaxMBFileSize` its maximum size (relevant with rollover and file logging enabled).
- In DNS Manager (server Properties > Debug Logging) you can also filter by IP address, direction, packet content, transport and request/response.
- Without rollover, the server overwrites the oldest packet information when the maximum size is reached.

## Verify
- [ ] A test query from a known client appears in the enabled log (analytical event 257 or `dns.log`) within seconds, and disk use is being watched.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Enable DNS Logging and Diagnostics article in full and the Set-DnsServerDiagnostics parameter list. Removed as unsupported: 2012 R2 hotfix, event 256 and 519-522 as zone transfer, the wevtutil 1 GB command, Get-WinEvent filter, FilterIPAddressList cmdlet use, the sample dns.log line, the claim that the analytic log stops when full (the page offers both modes) and the WEF/forwarder advice.
