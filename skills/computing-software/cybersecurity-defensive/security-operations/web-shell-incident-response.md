---
id: computing-software.cybersecurity-defensive.security-operations.web-shell-incident-response
name: web-shell-incident-response
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, web-shell-response, web-server-compromise, iis, apache, exchange, file-integrity, persistence-removal]
level: advanced
status: draft
description: "Respond to a web server compromise with a web shell: confirm and preserve, find all shells and entry vulnerability, scope lateral movement, rebuild, and harden."
sources: ["https://media.defense.gov/2020/Jun/09/2002313081/-1/-1/0/CSI-DETECT-AND-PREVENT-WEB-SHELL-MALWARE-20200422.PDF", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-062a", "https://learn.microsoft.com/en-us/defender-endpoint/web-shells-threat-hunting"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Web shell incident response

## Confirm
Typical signals: EDR alert `w3wp.exe`/`httpd`/`java` spawning `cmd.exe`, `powershell`, `whoami`,
`net`; a new `.aspx`/`.jsp`/`.php` file in the web root; WAF or access log hits on an odd file
with POSTs from few IPs. Look at the file content (from a copy): `eval(`, `Request.Form` passed to
execution, base64 blobs, `ProcessStartInfo`, China Chopper one-liners.

## Preserve before cleaning
- Copy the web root (with timestamps), web server logs, application logs, EDR timeline, and a
  memory image if the shell may be memory-resident (e.g. IIS modules, Java agents, .NET in-memory).
- Snapshot the VM.
Don't delete the shell first: it tips the attacker and destroys evidence.

## Find the entry point and all shells
- Access logs: first request to the shell; requests just before it from the same IP (exploit of
  upload function, deserialisation, known CVE such as Exchange ProxyShell, MOVEit, Confluence).
- File system: files created/modified around that time anywhere under web roots and temp dirs
  (`find /var/www -newer <ref> -type f`; on Windows MFT/USN timeline).
- Compare against a known-good deployment (hash comparison with the release artefact).
- Check for config persistence: IIS modules (`appcmd list modules`), `web.config` handlers,
  Apache `LoadModule`, Tomcat valves, scheduled tasks, new local accounts.

## Scope beyond the server
The web server's identity (app pool account, service account, database credentials in config
files, cloud instance role) is now the attacker's. Hunt for its use elsewhere; check outbound
connections and lateral movement (SMB/RDP from the server, which normally never happens).

## Eradicate and recover
- Rebuild the server from a clean image and redeploy the application from source control; do not
  just delete shells.
- Patch or fix the exploited vulnerability before exposure; rotate every secret the server held.
- Restore content data only after scanning it.

## Harden
Web root not writable by the app identity except specific upload dirs; uploads served from
non-executable storage; FIM on web roots; EDR rule for web server processes spawning shells;
WAF virtual patch while fixing code.

## Gotchas
- Multiple shells are the norm; attackers plant backups.
- Load-balanced farms: every node may be compromised.
- Logs on the box may be tampered with; prefer load balancer/WAF/central logs.

## Verify
After rebuild: FIM baseline clean, no requests to former shell paths succeed (404 and alerting),
and no further anomalous child processes from the web server for the monitoring period.
