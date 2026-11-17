---
id: computing-software.digital-forensics-incident-response.log-analysis.exchange-iis-owa-and-ecp-log-investigation
name: exchange-iis-owa-and-ecp-log-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [exchange-logs, web-server-logs, webshell, iis-logs, dfir]
level: advanced
status: draft
description: "Investigate Exchange Server exploitation (ProxyLogon, ProxyShell, ProxyNotShell) through IIS, HttpProxy, ECP and PowerShell logs, plus webshell and mailbox export traces."
sources: ["https://www.microsoft.com/en-us/security/blog/2021/03/02/hafnium-targeting-exchange-servers/", "https://github.com/microsoft/CSS-Exchange"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exchange IIS, OWA and ECP log investigation

**Goal:** on-premises Exchange is a frequent initial access point. Its logs record exploitation
attempts, webshell use and attacker mailbox exports.

## Log sources
| Log | Location (relative to Exchange install / IIS) | Use |
|---|---|---|
| IIS W3C logs | `inetpub\logs\LogFiles\W3SVC1` (front end) and `W3SVC2` (back end) | Requests to `/owa`, `/ecp`, `/autodiscover`, `/mapi`, `/EWS`, `/aspnet_client` |
| HttpProxy logs | `<ExchangeInstall>\Logging\HttpProxy\<protocol>\` | Back-end routing: `AnchorMailbox`, `TargetServer` - SSRF evidence (ProxyLogon) |
| ECP server logs | `<ExchangeInstall>\Logging\ECP\Server\` | `Set-OabVirtualDirectory` abuse (ProxyLogon webshell write) |
| PowerShell / CmdletInfra | `<ExchangeInstall>\Logging\CmdletInfra\` and MSExchange Management event log | `New-MailboxExportRequest`, `Set-*VirtualDirectory` |
| OAB generator / Application logs | Application event log, MSExchange events | Failed writes, crashes |

## Indicators
- **ProxyLogon (CVE-2021-26855 et al.)**: requests to `/ecp/<random>.js` or `/ecp/y.js` with `X-BEResource` cookie; HttpProxy logs with `AuthenticatedUser` empty and `AnchorMailbox` = `ServerInfo~<host>/...`.
- **ProxyShell**: `/autodiscover/autodiscover.json?@evil.com/mapi/nspi` or `.../powershell/?X-Rps-CAT=` patterns; `New-MailboxExportRequest` to `.aspx` paths (webshell via PST export).
- **ProxyNotShell**: autodiscover requests with `/powershell` in the path and an authenticated low-priv user.
- Webshells: new `.aspx` files in `inetpub\wwwroot\aspnet_client\`, `<ExchangeInstall>\FrontEnd\HttpProxy\owa\auth\`, `ecp\auth`; IIS requests to them (POST with 200).
- Mailbox exports: `MailboxExportRequest` cmdlets in logs, `.pst` files in web-accessible paths.

## Tools
- Microsoft CSS-Exchange scripts: `Test-ProxyLogon.ps1`, `Exchange On-premises Mitigation Tool`, `HealthChecker`.
- Hunt with Log Parser / Python over IIS logs; Velociraptor `Exchange.*` artifacts.

## Gotchas
- IIS logs are UTC; HttpProxy logs are CSV with many fields; keep all servers' logs (DAG members).
- Patching later does not remove webshells; scan for files created during exposure windows.

## Verify
Every webshell or export found is tied to the exploiting request and source IP in IIS/HttpProxy logs.
