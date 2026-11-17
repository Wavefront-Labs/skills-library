---
id: computing-software.systems-network-administration.nagios-core.security-best-practices
name: security-best-practices
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, security, nagios-user, nagios-group, resource-file, command-file-permissions, check-result-path, remote-agents, hardening]
level: practitioner
status: docs-checked
description: "The eleven Nagios Core security practices: dedicated server, non-root user, locked check-result and command-file paths, CGI auth, full paths, USERn secrets, macro cleansing."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security checklist

1. **Dedicated server**: few services, TCP wrappers/firewall, no user logins.
2. **Not root**: set `nagios_user` and `nagios_group`; use sudo for handlers/plugins needing root.
3. **Check result directory** (`check_result_path`): only the nagios user (or root) may read/write; otherwise fake results can be injected.
4. **Command file directory** (`/usr/local/nagios/var/rw`): writable only by the nagios and web server users; consider CGIWrap on multi-user hosts.
5. **CGI authentication** required; extra rights only to chosen contacts. With `use_authentication` off, cmd.cgi refuses commands.
6. **Enhanced CGI security** (`computing-software.systems-network-administration.nagios-core.cgi-security-hardening`).
7. **Full paths** to scripts and binaries in command definitions.
8. **`$USERn$` macros** hold usernames/passwords in resource files (mode 600/660; CGIs don't read them).
9. **`illegal_macro_output_chars`** strips dangerous characters (backticks) from output macros.
10. **Remote agents** (NRPE, NSClient, SNMP): restrict with firewalls and access lists.
11. **Encrypt** traffic between Nagios servers and agents where possible.

Related: `computing-software.systems-network-administration.nagios-core.macro-sanitization-environment`.

## Checked

2026-11-04. Confirmed all eleven practices against the Security Considerations page (dedicated box, nagios_user and nagios_group with sudo, check result directory, command file directory and CGIWrap, CGI authentication and use_authentication, enhanced CGI security, full paths, $USERn$ with 600 or 660, illegal_macro_output_chars, remote agent lockdown, encrypted channels).

Method: documentation only; no commands were run.
