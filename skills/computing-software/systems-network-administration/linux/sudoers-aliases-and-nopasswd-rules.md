---
id: computing-software.systems-network-administration.linux.sudoers-aliases-and-nopasswd-rules
name: sudoers-aliases-and-nopasswd-rules
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sudo, sudoers, sudo-aliases, cmnd-alias, user-alias, host-alias, runas-alias, nopasswd, sudoers-d, visudo, least-privilege, rhcsa, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Write least-privilege sudoers rules: User/Host/Runas/Cmnd_Alias, NOPASSWD only where justified, argument restrictions, sudoers.d drop-ins with visudo -c, and shell escapes."
sources:
  - https://github.com/sudo-project/sudo/blob/main/docs/sudoers.mdoc.in
  - https://github.com/sudo-project/sudo/blob/main/docs/visudo.mdoc.in
  - https://gtfobins.github.io/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# sudoers: aliases and NOPASSWD

**Goal:** give teams exactly the commands they need, readable enough to audit, without
accidental root shells.

## 1. Rule shape
`who  where = (as_whom)  [TAGS:] commands`
```sudoers
# /etc/sudoers.d/20-webops   (edit with: visudo -f /etc/sudoers.d/20-webops)
User_Alias   WEBOPS  = alice, bob, %webops
Host_Alias   WEB     = web01, web02, 10.0.20.0/24
Runas_Alias  APPUSR  = www-data, app
Cmnd_Alias   WEBSVC  = /usr/bin/systemctl restart nginx, /usr/bin/systemctl reload nginx, \
                       /usr/bin/systemctl --no-pager status nginx
Cmnd_Alias   LOGS    = /usr/bin/journalctl --no-pager -u nginx *

WEBOPS  WEB = (root) WEBSVC, LOGS
WEBOPS  WEB = (APPUSR) NOPASSWD: /opt/app/bin/deploy.sh
%wheel  ALL = (ALL:ALL) ALL
```
Alias names are UPPERCASE; `%group`; `ALL` matches everything. When several rules match, the last match is
used (not necessarily the most specific), so put broad rules first, specific overrides after.

## 2. NOPASSWD
Use for automation accounts and specific, harmless commands:
```sudoers
deploy  ALL = (root) NOPASSWD: /usr/bin/systemctl restart app.service
backup  ALL = (root) NOPASSWD: /usr/local/bin/run-backup.sh
```
Never `NOPASSWD: ALL` for humans on shared servers — a hijacked session becomes root silently.

## 3. Arguments and escapes
- Command with no args listed = **any args allowed**. `""` as args = no args allowed:
  `/usr/bin/apt update ""`.
- Wildcards in args are dangerous: in command line arguments `*` also matches `/` and white space, so
  `/bin/cat /var/log/*` permits `/var/log/../../etc/shadow`.
- Shell escapes: editors, pagers, `find -exec`, interpreters and similar programs can spawn shells — see GTFOBins.
  Mitigate with the `NOEXEC:` tag (see "Preventing shell escapes" in sudoers(5) for when it works),
  `--no-pager` in the allowed command line, and `sudoedit` instead of granting an editor:
```sudoers
WEBOPS ALL = (root) sudoedit /etc/nginx/conf.d/*.conf
WEBOPS ALL = (root) NOEXEC: /usr/bin/journalctl
```

## 4. Validate before saving
```bash
visudo -c                              # whole config
visudo -cf /etc/sudoers.d/20-webops    # syntax-check one file (the whole policy is only evaluated by `visudo -c`)
sudo -l -U alice                       # what alice may run
```
Files in `/etc/sudoers.d/` whose names contain `.` or end in `~` are skipped; the default file mode is 0440.

## Gotchas
- A syntax error in sudoers breaks sudo for everyone — always visudo; keep a root shell open.
- Use fully qualified command paths; relative paths cannot be matched.


## Verify
- [ ] `visudo -c` clean; `sudo -l -U <user>` shows exactly the intended commands.
- [ ] A forbidden command (e.g. `sudo -u root bash`) is denied and logged.

## Checked
Checked 2026-10-25 against the sudo-project/sudo sudoers and visudo manual sources (main branch).
Confirmed: rule shape and alias types (User_Alias, Host_Alias, Runas_Alias, Cmnd_Alias), last-match rule, tag names (NOPASSWD, NOEXEC, LOG_OUTPUT), the `sudoedit` built-in (no leading path), empty-argument `""` and no-argument semantics, wildcard matching of `/` and white space in arguments, `.`/`~` skip rule and 0440 default mode for included files, `visudo -c` and `-f`.
Removed as unconfirmed: the rsync server flag string, the group-membership login note and the claim that NOEXEC covers all programs.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container with sudo 1.9.16p2: every alias type and the example rules parsed by visudo -cf; visudo -c reading /etc/sudoers.d, skipping names with a dot or ending in ~; last matching rule winning (a later non-NOPASSWD rule asked for a password); unqualified command path rejected (expected a fully-qualified path name); "" argument rule; wildcard traversal; sudo -l -U; /etc/sudoers mode 0440. Not run: NOEXEC, LOG_OUTPUT, Host_Alias matching on real hostnames.
