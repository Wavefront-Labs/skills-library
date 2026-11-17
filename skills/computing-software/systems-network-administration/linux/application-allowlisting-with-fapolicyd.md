---
id: computing-software.systems-network-administration.linux.application-allowlisting-with-fapolicyd
name: application-allowlisting-with-fapolicyd
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fapolicyd, application-allowlisting, trust-database, file-access-policy, integrity, rhel-hardening]
level: practitioner
status: docs-checked
description: "Enforce application allowlisting on RHEL with fapolicyd: rules and trust sources, adding trusted files, permissive mode for rollout, debugging denials and integrity options."
sources:
  - https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.8
  - https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.conf.5
  - https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.rules.5
  - https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd-cli.8
  - https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.trust.5
  - https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fagenrules.8
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Application allowlisting with fapolicyd

fapolicyd is a userspace daemon that decides file access from a trust database and file or process attributes. Trust comes from the package database backend (rpmdb on RPM systems) plus a local file trust list.

## Install and roll out in permissive mode
```bash
# install the fapolicyd package, then in /etc/fapolicyd/fapolicyd.conf set:
#   permissive = 1        (default 0; 1 = always allow, for policy testing only)
systemctl enable --now fapolicyd
# run the workload for days, then collect the denials the rules audited:
ausearch --start today -m fanotify -i
fapolicyd-cli --list            # prints the active rules with rule numbers, to match against debug output
```
Denials only reach the audit log when auditing is enabled and at least one audit rule is loaded. Switch back to `permissive = 0` only when no legitimate denials remain.

## Rules
Rules live in `/etc/fapolicyd/rules.d/*.rules` and are merged into `/etc/fapolicyd/compiled.rules` by `fagenrules` (`fagenrules --load` also loads them). The format is `decision perm subject : object`, evaluated top to bottom, first match wins; the colon is mandatory.
```
# trust-based execute policy; the final deny_audit is the terminal rule
allow perm=execute gid=appadmins : dir=/opt/inhouse/bin/ trust=1
allow perm=execute all : trust=1
deny_audit perm=execute all : all
```
`trust=1` on an object means it is in the trust database; how strictly that is verified depends on the `integrity` setting. Put narrower allow rules above broader ones. `fapolicyd-cli --check-rules` (or `--lint`) checks a ruleset.

## Trust in-house software
```bash
fapolicyd-cli --file add /opt/inhouse/bin/            # adds size and SHA256 to the file trust database (end directories with /)
fapolicyd-cli --file add /opt/tool --trust-file tool  # use a single trust file named tool inside trust.d/
fapolicyd-cli --file update /opt/inhouse/bin/         # refresh size and hash after a new version is deployed
fapolicyd-cli --update                                # notify the daemon to update the trust database
fapolicyd-cli --check-trustdb                         # mismatches between the trust database and files on disk
```
Software known to the package database backend is trusted automatically; files installed any other way need an entry in the file trust database, and entries need refreshing after a file changes (`--file update`) or the hash no longer matches when `integrity` is `sha256` or `ima`.

## Integrity
`integrity = none | size | sha256 | ima` in `fapolicyd.conf`; `none` is the default. `size` compares file size only (fast, but a same-size replacement is not detected); `sha256` compares the hash; `ima` uses the hash IMA stores in extended attributes in addition to the size check, so every filesystem holding executable code must support xattrs.

## Debugging a denial
```bash
systemctl stop fapolicyd && fapolicyd --debug-deny
# runs in the foreground and writes only deny decisions to stderr; compare with the rule numbers from fapolicyd-cli --list
```
`--debug` shows all decisions. Never attach a debugger to fapolicyd with ptrace: the SIGSTOP can deadlock the system. Filesystems that should not be policed are controlled with `watch_fs` (and `ignore_mounts`) in `fapolicyd.conf`.

## Verify
- [ ] A copy of a system binary in an untrusted location fails to execute and the denial appears in `ausearch -m fanotify -i`.
- [ ] All production services start after a reboot in enforcing mode.

## Checked
Checked 2026-10-25 against the fapolicyd man page sources (linux-application-whitelisting/fapolicyd doc/, main, last commit 2026-10-14; fapolicyd.8 dated March 2026). Confirmed: `permissive` (default 0), `integrity` values and default `none`, `watch_fs`, `fagenrules` and `compiled.rules`, rule grammar `decision perm subject : object`, first match wins, `trust=`, `deny_audit`, `gid`/`dir` fields, `fapolicyd-cli` options `--list` (prints rules, not denials), `--file add|delete|update`, `--trust-file`, `--update`, `--check-trustdb`, `--check-rules`/`--lint`, daemon `--debug`/`--debug-deny`/`--permissive`, ptrace warning, audit event requirements and the `ausearch -m fanotify` command. Fixed: `fapolicyd-cli --list` was presented as a way to collect denials, and `journalctl ... dec=deny` is not documented. Removed unconfirmed claims: the shipped `10-languages.rules` contents, Python bytecode and overlay-path causes, the exact error text and the `dnf` command.

Method: documentation only; no commands were run.
