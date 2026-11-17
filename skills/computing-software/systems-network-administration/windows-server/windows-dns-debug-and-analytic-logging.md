---
id: computing-software.systems-network-administration.windows-server.windows-dns-debug-and-analytic-logging
name: windows-dns-debug-and-analytic-logging
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-dns-server, dnsserver-module, dns-debug-logging, dns-analytic-log, dns-audit-log, set-dnsserverdiagnostics, etw, query-logging, threat-hunting]
level: practitioner
status: docs-checked
description: "Log DNS queries on Windows DNS Server: Audit and Analytic ETW channels (low overhead) vs legacy debug logging, enabling, sizing, parsing and shipping to a SIEM."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/dns-logging-and-diagnostics
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverdiagnostics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows DNS debug and analytic logging

## Three sources
1. **Audit log** (`Microsoft-Windows-DNSServer/Audit`, enabled by default): changes to
   zones, records, settings. Who deleted that record lives here.
2. **Analytic log** (`Microsoft-Windows-DNSServer/Analytical`, ETW): every query/response
   with client IP, low overhead. Off by default; enable for query visibility.
3. **Debug logging** (legacy, text file): packet-level detail, high overhead, for short
   troubleshooting sessions.

## Analytic log
```powershell
tracelog.exe -start Dns -guid #{EB79061A-A566-4698-9119-3ED2807060E7} -level 5 -matchanykw 0x7FFFF -f <TRACE_DIR>\analytic.etl
tracelog.exe -stop Dns
```
In Event Viewer: Applications and Services Logs > Microsoft > Windows > DNS-Server, View > Show Analytic and Debug Logs, then Analytical > Properties > Enable logging. The default file is `%SystemRoot%\System32\Winevt\Logs\Microsoft-Windows-DNSServer%4Analytical.etl`.
Analytic event IDs include 256 query received, 257 response success, 258 response failure, 259 ignored query, 260 recursive query out.
The ETW provider GUID `{EB79061A-A566-4698-9119-3ED2807060E7}` covers both audit and analytic events for any ETW consumer. Analytic logging usually affects performance only at high query rates (the article cites 100,000 queries per second).

## Debug logging (short sessions)
```powershell
Set-DnsServerDiagnostics -EnableLoggingForLocalLookupEvent $true -Queries $true -Answers $true `
  -ReceivePackets $true -SendPackets $true -UdpPackets $true -TcpPackets $true `
  -EnableLogFileRollover $true -LogFilePath '<LOG_DIR>\dns.log' -MaxMBFileSize 500000000
Set-DnsServerDiagnostics -All $false    # turn off afterwards
```
Filter by IP with `-IPFilterList` (shown as `FilterIPAddressList` in `Get-DnsServerDiagnostics` output). `Set-DnsServerDiagnostics -All $true` also turns on log-file rollover.

## Uses
- Find clients still querying a decommissioned DC/server name before removal.
- Threat hunting: queries to newly registered/suspicious domains, DGA patterns, tunnelling (very long labels, TXT volume).

## Verify
- [ ] Analytic events 256/257 visible in the SIEM per DNS server.
- [ ] Debug logging off on all servers (`Get-DnsServerDiagnostics`) outside troubleshooting.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DnsServer/DhcpServer/DnsClient modules) repositories, latest commit 2026-10-23. Confirmed: Audit log enabled by default; analytic log off by default; events 256-260; default .etl path; provider GUID; tracelog commands copied from the article; `Set-DnsServerDiagnostics` parameters (`-Queries`, `-Answers`, `-ReceivePackets`, `-SendPackets`, `-UdpPackets`, `-TcpPackets`, `-EnableLogFileRollover`, `-LogFilePath`, `-MaxMBFileSize`, `-IPFilterList`, `-All`). Replaced the undocumented wevtutil command and removed the Sentinel/Splunk connector remark; fixed the filter parameter name.

Method: documentation only; no commands were run.
