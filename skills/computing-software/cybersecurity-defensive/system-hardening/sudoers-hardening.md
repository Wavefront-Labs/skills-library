---
id: computing-software.cybersecurity-defensive.system-hardening.sudoers-hardening
name: sudoers-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, sudoers-hardening, sudo, least-privilege, visudo, sudo-logging, use-pty]
level: practitioner
status: docs-checked
description: "Harden sudo: least-privilege command rules via sudoers.d, visudo validation, no NOPASSWD ALL, use_pty and logging, and avoid shell escapes from allowed commands."
sources: ["https://github.com/sudo-project/sudo/blob/main/docs/sudoers.mdoc.in", "https://github.com/sudo-project/sudo/blob/main/docs/visudo.mdoc.in", "https://github.com/sudo-project/sudo/blob/main/docs/sudo.mdoc.in"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sudoers hardening

**Goal:** sudo grants only the commands each role needs, is logged, and cannot be trivially escaped to root shell.

## Defaults (`/etc/sudoers.d/00-defaults`, edit with `visudo -f`)
```
Defaults use_pty
Defaults logfile="/var/log/sudo.log"
Defaults log_input, log_output        # I/O logs are written under iolog_dir; replay with sudoreplay
Defaults timestamp_timeout=5
Defaults passwd_tries=3
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Defaults env_reset
```
`use_pty` stops background processes from injecting into the user's terminal after sudo exits.

## Rules
```
%webops ALL=(root) /usr/bin/systemctl restart nginx, /usr/bin/systemctl reload nginx
%dba    ALL=(postgres) /usr/bin/psql
```
- Full paths only; arguments listed explicitly restrict usage (an empty `""` argument list means no arguments).
- Avoid wildcards in arguments (`/usr/bin/cat /var/log/*` permits `/var/log/../../etc/shadow`).
- Never grant editors, pagers, interpreters or other programs that can spawn a shell or run commands (`vim`, `less`, `find`, `tar`, `git` and similar); use `sudoedit` for file editing.
- Avoid `NOPASSWD: ALL`; for automation accounts restrict to specific commands.
- Use the `NOEXEC:` tag for commands that should not spawn children; sudoers(5) says it prevents a dynamically linked executable from running further commands and describes where it does not work (see its section on preventing shell escapes).

## Hygiene
- Always edit via `visudo` (syntax check) - a broken sudoers file locks everyone out. `visudo -c` validates all files.
- Files in `/etc/sudoers.d/` with a `.` or ending in `~` are ignored.
- Central management: sudo rules via LDAP (sudoers(5) describes the LDAP source) or config management, not hand-edited per host.
- Audit: `grep -rE 'NOPASSWD|ALL=\(ALL' /etc/sudoers /etc/sudoers.d/`.

## Verify
- [ ] `sudo -l -U <user>` shows only intended commands.
- [ ] sudo events reach the SIEM (the syslog entries plus the `logfile` and I/O logs).
- [ ] `visudo -c` passes on all hosts.

## Checked
Checked 2026-10-25 against sudoers(5), visudo(8) and sudo(8) sources (sudo-project/sudo, docs directory, main branch). Confirmed: `use_pty` (runs the command in a pseudo-terminal so a malicious program cannot inject into or retain the user's terminal), `logfile`, `log_input`/`log_output` with `iolog_dir` and sudoreplay, `timestamp_timeout` (minutes), `passwd_tries`, `secure_path`, `env_reset`, `""` meaning no arguments, shell-style wildcard matching (a `*` matches any characters, including `/` and white space), the `NOEXEC` and `NOPASSWD` tags, `sudoedit`, `visudo -c` check-only mode, and that `/etc/sudoers.d` skips names ending in `~` or containing a `.`. Removed the unconfirmed GTFOBins reference and the fixed sudo-io path; the CIS benchmark was not read.

Method: documentation only; no commands were run.
