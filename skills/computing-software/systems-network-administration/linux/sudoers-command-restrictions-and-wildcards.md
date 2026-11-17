---
id: computing-software.systems-network-administration.linux.sudoers-command-restrictions-and-wildcards
name: sudoers-command-restrictions-and-wildcards
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sudo, sudo-wildcards, sudo-command-restriction, sudoers, sudoedit, noexec, privilege-escalation]
level: advanced
status: verified
description: "Write sudoers command rules that actually restrict: argument matching, wildcard escapes, shell-escape-capable programs, sudoedit instead of editors, NOEXEC and digest checks."
sources:
  - https://github.com/sudo-project/sudo/blob/main/docs/sudoers.mdoc.in
  - https://github.com/sudo-project/sudo/blob/main/docs/sudo.mdoc.in
  - https://gtfobins.github.io/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# sudoers command restrictions and wildcard pitfalls

## Arguments
```
alice ALL=(root) /usr/bin/systemctl restart nginx       # exactly these args
alice ALL=(root) /usr/bin/systemctl restart nginx ""    # "" = no extra args allowed
alice ALL=(root) /usr/bin/journalctl                    # no args specified = ANY args allowed
```
## Wildcards are dangerous
```
alice ALL=(root) /usr/bin/cat /var/log/*        # alice runs: sudo cat /var/log/../../etc/shadow
alice ALL=(root) /usr/bin/systemctl * nginx     # 'systemctl edit --full x nginx' style abuse; * matches spaces
```
In command line arguments `*` matches any characters, including `/` and white space. Use exact commands, a wrapper script (root-owned, not writable,
validating its arguments), or regular expressions (sudo 1.9.10 and later; they must start with `^` and end with `$`):
`/usr/bin/systemctl ^(start|stop|restart) nginx$`.

## Programs that are root shells in disguise
Editors, pagers, `find -exec`, interpreters, `git`, container runtimes and similar programs can spawn shells or
read arbitrary files. See GTFOBins.
Mitigations: the `NOEXEC:` tag (see "Preventing shell escapes" in sudoers(5) for how it works and where it does not),
`--no-pager` on journalctl and systemctl commands, or don't grant them.

## Editing files: sudoedit
```
%webadmins ALL=(root) sudoedit /etc/nginx/conf.d/*.conf
```
User runs `sudoedit /etc/nginx/conf.d/site.conf` → edits a temporary copy as themselves with the editor named by
`SUDO_EDITOR`, `VISUAL` or `EDITOR` (in that order), and sudo copies it back. Since 1.8.15 sudoedit does not open
symbolic links unless `sudoedit_follow` is enabled (the `FOLLOW`/`NOFOLLOW` tags override it); `sudoedit_checkdir`
refuses files in directories the invoking user can write. Do not use wildcards loosely in sudoedit rules.

## Integrity
`Cmnd_Alias DEPLOY = sha256:<digest> /usr/local/bin/deploy` — runs only if the binary matches the SHA-2 digest (hex or base64; sha224, sha256, sha384, sha512).

## Verify
- [ ] `sudo -l -U alice` shows only intended commands; attempts like `../` paths and shell escapes fail in testing.

## Checked
Checked 2026-10-25 against the sudo-project/sudo manual sources (sudoers, sudo).
Confirmed: argument and `""` semantics, wildcard behaviour in arguments, regular expressions from 1.9.10 (must start with `^` and end with `$`), NOEXEC tag, sudoedit editor variable order, sudoedit_follow (since 1.8.15) and sudoedit_checkdir, digest syntax and algorithms.
Corrected: the symlink restriction for sudoedit dates from 1.8.15, not 1.9. Removed as unconfirmed: the env_keep PAGER example and the SYSTEMD_PAGER advice.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container with sudo 1.9.16p2: visudo -cf and -c, regex rule with ^...$ (extra argument refused), no-argument rule allowing any arguments, "" rule refusing extra arguments, wildcard rule allowing /var/log/../../etc/hostname, sudoedit rule and sudoedit_follow/sudoedit_checkdir listed by sudo -V, sha256 digest rule parsing. Not run: NOEXEC behaviour, sudoedit editing, a matching digest.
