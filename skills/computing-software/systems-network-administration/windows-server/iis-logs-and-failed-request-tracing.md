---
id: computing-software.systems-network-administration.windows-server.iis-logs-and-failed-request-tracing
name: iis-logs-and-failed-request-tracing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iis, iis-administration, iis-logs, failed-request-tracing, freb, w3c-logging, httperr, log-parser]
level: practitioner
status: docs-checked
description: "Troubleshoot IIS with W3C logs (sc-status, substatus, win32-status, time-taken), HTTPERR logs, Failed Request Tracing rules and log retention."
sources:
  - https://learn.microsoft.com/en-us/iis/troubleshoot/using-failed-request-tracing/troubleshooting-failed-requests-using-tracing-in-iis
  - https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/iis/health-diagnostic-performance/http-status-code
  - https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/sitedefaults/logfile/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIS logs and Failed Request Tracing

## W3C logs
Default directory `%SystemDrive%\inetpub\logs\LogFiles` (one `W3SVC<siteID>` folder per site, set in
`siteDefaults.logFile.directory`). W3C records are handled by HTTP.sys; every record's time stamp is UTC.
Fields you set in `logExtFileFlags` include status, substatus, win32 status, `time-taken` (milliseconds, from first
byte received to last send completion, so it excludes network time), URI stem and client IP.
```powershell
Get-Content (Get-ChildItem "$env:SystemDrive\inetpub\logs\LogFiles\W3SVC2" | Sort-Object LastWriteTime | Select-Object -Last 1).FullName -Tail 50
```
Status and substatus (Microsoft HTTP status code page): 401.1 logon failed (bad user name or password), 401.2
logon failed due to server configuration (authentication settings), 403.14 no directory listing and no default
document, 404.0 not found, 500.19 problem in applicationHost.config or web.config, 502.3 forwarder connection error
(ARR) and 503.0 application pool unavailable (stopped or disabled; also 503.2 concurrent request limit exceeded).

## Failed Request Tracing (FREB)
Enable the Tracing role service, then IIS Manager > site > Failed Request Tracing Rules > Add: content `*`, the
status codes or time taken that define a failure, providers and verbosity (Verbose to start), then enable tracing at
site level (Actions > Edit Site Tracing). IIS writes one XML file per failed request, plus one `freb.xsl` style
sheet per directory, under `%SystemDrive%\inetpub\logs\FailedReqLogFiles\W3SVC<id>`; open the XML in a browser. The
style sheet highlights errors and warnings. Disable tracing again afterwards.

## Retention
Move the log directory off the system drive in the site Logging settings (`logFile.directory`) and schedule your own
cleanup or shipping to a SIEM, for example:
```powershell
Get-ChildItem "$env:SystemDrive\inetpub\logs\LogFiles" -Recurse -Filter *.log | Where-Object LastWriteTime -lt (Get-Date).AddDays(-30) | Remove-Item
```
Review a `-WhatIf` run before deleting.

## Verify
- [ ] Failing request reproduced, FREB trace pinpoints the failing module; tracing disabled again.

## Checked
Date 2026-10-27. Documentation: IIS logFile reference, Failed Request Tracing walkthrough, Microsoft HTTP status code
page. Confirmed: default directory, UTC time stamps, time-taken meaning, FREB output folder and freb.xsl, status and
substatus meanings. HTTP.sys error log (HTTPERR) details and win32 status codes are not covered here.
Method: documentation only; no commands were run.
