---
id: computing-software.cybersecurity-defensive.security-operations.web-shell-hunting
name: web-shell-hunting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [web-shell-hunting, threat-hunting, web-shells, iis, apache, sysmon, access-log-analysis]
level: practitioner
status: draft
description: "Hunt for web shells: web server process spawning shells, new script files in web roots, anomalous POST patterns in access logs, and file integrity baselines."
sources: ["https://attack.mitre.org/techniques/T1505/003/", "https://media.defense.gov/2020/Jun/09/2002313081/-1/-1/0/CSI-DETECT-AND-PREVENT-WEB-SHELL-MALWARE-20200422.PDF", "https://github.com/nsacyber/Mitigating-Web-Shells"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Web shell hunting (T1505.003)

## Process lineage (best signal)
Web server worker processes (`w3wp.exe`, `httpd`, `nginx`, `php-fpm`, `java`/Tomcat, `node`)
spawning `cmd.exe`, `powershell.exe`, `sh`, `bash`, `whoami`, `net.exe`, `certutil`, `curl`.
```kql
DeviceProcessEvents
| where InitiatingProcessFileName in~ ("w3wp.exe","httpd.exe","tomcat9.exe","php-cgi.exe")
| where FileName in~ ("cmd.exe","powershell.exe","whoami.exe","net.exe","certutil.exe","rundll32.exe")
| summarize count(), make_set(ProcessCommandLine) by DeviceName, InitiatingProcessFileName
```
Exchange: `w3wp.exe` with `MSExchangeOWAAppPool` spawning children is almost always malicious.

## File system
- New or modified `.aspx`, `.ashx`, `.asmx`, `.jsp`, `.jspx`, `.php` files in web roots, especially
  outside deployment windows or not in source control.
- Compare against a known-good deployment hash list; NSA's `dirChecker.ps1` / file integrity tools.
- Indicators in content: `eval(`, `base64_decode`, `Request.Form` with `Process.Start`, China Chopper
  one-liners; scan with YARA (e.g. Neo23x0 web shell rules).

## Access logs
- Requests to rare URIs (requested by one or few client IPs) with POST and 200 responses.
- Pages with few distinct user agents/referrers but many requests.
```spl
index=iis cs_method=POST sc_status=200 | stats dc(c_ip) as clients count by cs_uri_stem
| where clients <= 2 AND count > 20
```

## Network
Outbound connections from web servers to the internet (they should rarely initiate).

## Gotchas
- Memory-only web shells (e.g. injected .NET modules, Java agents) leave no files; rely on
  process lineage and memory analysis.
- Legitimate admin consoles also spawn processes; allowlist by exact command line.

## Verify
Every web-facing server checked against deployment baseline; findings either explained by change
records or escalated to web shell incident response.
