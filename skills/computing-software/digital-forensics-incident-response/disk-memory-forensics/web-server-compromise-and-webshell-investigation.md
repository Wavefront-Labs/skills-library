---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.web-server-compromise-and-webshell-investigation
name: web-server-compromise-and-webshell-investigation
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [webshell, web-server-compromise, linux-forensics, iis, initial-access, dfir]
level: advanced
status: draft
description: "Investigate web server compromise and web shells on Linux and IIS: finding shells by time and content, worker-process children, access log correlation and scope."
sources: ["https://attack.mitre.org/techniques/T1505/003/", "https://media.defense.gov/2020/Jun/09/2002313081/-1/-1/0/CSI-DETECT-AND-PREVENT-WEB-SHELL-MALWARE-20200422.PDF", "https://github.com/nsacyber/Mitigating-Web-Shells"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Web server compromise and web shell investigation

**Goal:** find web shells, how they were planted, what the attacker did through them, and
whether they moved beyond the web server.

## Find candidate shells
- **Time**: files in web roots created/modified during the window:
  `find /var/www -type f -newermt "2026-09-01" ! -newermt "2026-09-15" -ls`;
  on IIS, $MFT timeline of `inetpub\wwwroot`, Exchange `FrontEnd\HttpProxy\owa\auth\`,
  `aspnet_client`.
- **Content**: `grep -rlE "eval\(|base64_decode\(|assert\(|system\(|passthru\(|shell_exec\(|Runtime\.getRuntime|ProcessStartInfo|Request\.Item" /var/www`;
  NSA Mitigating-Web-Shells scripts and YARA rules (e.g. Neo23x0 signature-base).
- **Integrity**: compare the web root to the deployment artefact/git (`git status`, `diff -r`),
  package verification for CMS core files (`wp core verify-checksums`).
- Memory-only shells (Java/.NET filters/servlets, IIS modules): check loaded modules
  (`appcmd list modules`), Tomcat `catalina` logs, process memory.

## What the attacker did
- Worker process children: `w3wp.exe`, `httpd`, `nginx`, `php-fpm`, `java` (Tomcat) spawning
  `cmd.exe`, `powershell`, `sh`, `bash`, `whoami`, `curl`, `wget` (EDR, auditd execve, 4688).
- Access log requests to the shell path: source IPs, timing, POST sizes (see access log
  skill); WAF logs for bodies.
- Files dropped by the worker user (`www-data`, `IIS APPPOOL\...`): tools, archives of data.

## Initial vector
Exploit of the application or a plugin (CVE), file upload flaw, stolen admin credentials
(CMS admin logins), exposed management (Tomcat manager).

## Scope beyond the server
Credentials in config files (`wp-config.php`, `web.config` connection strings) used
elsewhere; database access logs; lateral movement from the server.

## Verify
For each shell: creation time, planting request (log line), commands executed (process or log
evidence), and confirmation of removal and credential rotation.
