---
id: computing-software.digital-forensics-incident-response.log-analysis.recognising-web-attack-patterns-in-logs
name: recognising-web-attack-patterns-in-logs
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [web-attack-detection, sql-injection, path-traversal, xss, command-injection, webshell, access-logs, dfir]
level: practitioner
status: draft
description: "Recognise SQL injection, XSS, traversal, command injection, scanners and webshell use in web server logs, and decide which requests actually succeeded."
sources: ["https://owasp.org/www-project-top-ten/", "https://owasp.org/www-community/attacks/", "https://httpd.apache.org/docs/2.4/logs.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recognising web attack patterns in logs

**Goal:** separate background scanning from targeted exploitation, and find the requests that
worked.

## Signatures (decode first)
URL-decode (sometimes twice) and normalise case before matching: `%27` = `'`, `%2e%2e%2f` =
`../`, `%3Cscript` = `<script`, `+` = space.
| Attack | Patterns |
|---|---|
| SQL injection | `' or 1=1`, `union select`, `order by 10--`, `sleep(5)`, `benchmark(`, `waitfor delay`, `information_schema`, `xp_cmdshell`, `0x` hex strings; sqlmap UA `sqlmap/1.x` |
| XSS | `<script`, `onerror=`, `javascript:`, `alert(`, `document.cookie`, `<svg/onload` |
| Path traversal / LFI | `../`, `..%2f`, `%252e%252e`, `/etc/passwd`, `win.ini`, `php://filter`, `file://` |
| Remote command injection | `;id`, pipe to `whoami`, `$(`, backticks, `wget http`, `curl http`, `/bin/sh`, `powershell -enc`, `nslookup <random>.oast.` |
| Template / expression injection | `${jndi:` (Log4Shell), `{{7*7}}`, `${7*7}`, `#{` |
| Deserialisation | `rO0AB` (Java serialized base64), `ysoserial`, `__VIEWSTATE` anomalies |
| Webshell use | repeated POSTs to one odd `.php/.aspx/.jsp` file with tiny responses, params like `cmd=`, `c=`, `z0=` (China Chopper), new files in upload dirs |
| Scanners | Nikto, Nuclei (`Nuclei - Open-source project`), `zgrab`, `masscan`, burst of 404s for admin paths |

## Did it succeed?
- **Status code and size:** 200 with response size different from the error baseline; time-based
  SQLi shows long `time-taken`/`%D` values matching the injected delay.
- **Sequence:** probing (404s/500s) -> one 200 -> follow-up requests from the same IP to new
  paths (webshell, admin pages).
- **Server-side effects:** new files in the webroot (compare mtimes), database logs, process
  creation from the web server user (`w3wp.exe`/`httpd`/`php-fpm` spawning `cmd.exe`/`sh`),
  outbound connections from the server.
- 500 errors right after injection attempts often indicate the payload reached the backend.

## Tooling
```bash
grep -Ei "union(%20|\+| )+select|sleep\(|%27|\.\./|<script|\$\{jndi" access.log
awk '$9==200' access.log | grep -Ei "cmd=|exec=|/uploads/.*\.(php|aspx|jsp)"
```
At scale: load into a SIEM or DuckDB and group by client IP, path and status; GoAccess for a
quick overview; WAF logs give rule IDs for blocked requests.

## Gotchas
- POST bodies are not in standard access logs: exploitation via POST shows only the path. Use
  WAF, application or reverse-proxy body logging if available.
- IPs behind CDNs/load balancers: use `X-Forwarded-For` fields.
- Encoded or chunked payloads evade naive grep.

## Self-check
For each attack class found you identified the source IPs, the first successful request (or
showed none succeeded), and server-side evidence supporting it.
