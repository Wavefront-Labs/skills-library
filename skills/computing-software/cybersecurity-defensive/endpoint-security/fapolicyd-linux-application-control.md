---
id: computing-software.cybersecurity-defensive.endpoint-security.fapolicyd-linux-application-control
name: fapolicyd-linux-application-control
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [application-control, fapolicyd, linux, rhel, file-access-policy, trust-database, rpm-trust, integrity-checking]
level: advanced
status: docs-checked
description: "Use fapolicyd on RHEL-family Linux to allow only trusted executables and libraries: trust sources, rules, permissive testing and troubleshooting denials."
sources: ["https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.conf.5", "https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.8", "https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd-cli.8", "https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.rules.5", "https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.trust.5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fapolicyd on Linux

**Goal:** on RHEL, Rocky, Alma and Fedora servers, only executables and libraries from trusted
packages or explicitly trusted files can run.

## How it works
fapolicyd is an application-whitelisting daemon that uses fanotify to make allow/deny decisions on
file access. Trust comes from the back-ends listed in the `trust` option of `fapolicyd.conf`:
`rpmdb` (files from the RPM database) and `file` (the `fapolicyd.trust` list); the default is
`rpmdb,file`. Rules live in `/etc/fapolicyd/rules.d/`; the daemon merges them into one compiled
rule set at startup.

## Set up
```
dnf install fapolicyd
systemctl enable --now fapolicyd
```

## Add trust for non-RPM software
```
fapolicyd-cli --file add /opt/vendorapp/bin/ --trust-file vendorapp
fapolicyd-cli --update
```
`--file` needs root. Package changes normally reach the daemon through the dnf plugin; manual
installs or direct edits to trust files need an explicit `--update`.

## Integrity checking
`integrity` in `fapolicyd.conf` is `none` (default), `size`, `ima` or `sha256`. `size` is fast but an
attacker can replace a file with one of the same size; `sha256` hashes the file and also checks size;
`ima` uses the IMA hash in extended attributes, so every file system holding executable code must
support xattrs.

## Test permissively
`permissive = 1` in `/etc/fapolicyd/fapolicyd.conf` makes the daemon always allow access even if
policy would block it; use it only for policy testing. To see would-be denials in the foreground:
```
systemctl stop fapolicyd
fapolicyd --debug-deny --permissive
```
Then turn permissive off and restart the service.

## Troubleshoot a denial
- With at least one audit rule loaded, denials appear as FANOTIFY audit events:
  `ausearch --start today -m fanotify -i`.
- Check trust: `fapolicyd-cli --check-trustdb` compares the trust database with files on disk;
  `fapolicyd-cli --dump-db` lists it (filter the output for your path).
- `fapolicyd-cli --check-config` parses `fapolicyd.conf`; `--check-rules --lint` checks rules.

## Gotchas
- Containers and language runtimes (Python virtualenvs, Java) load many untrusted files; trust directories carefully.
- A broken rule can stop services from starting: test changes in permissive mode on a staging host.
- `ignore_mounts` removes fanotify visibility for a mount; the mount must be `noexec` and data-only.

## Verify
- [ ] `systemctl status fapolicyd` active; a copied binary in /tmp is denied.
- [ ] Application smoke tests pass with enforcement on.

## Checked
2026-11-01 against the fapolicyd man pages in the upstream repository (fapolicyd.conf.5, fapolicyd.8, fapolicyd-cli.8, fapolicyd.rules.5, fapolicyd.trust.5): confirmed the `permissive`, `trust` (default `rpmdb,file`) and `integrity` options and their values, `--debug-deny`, `--permissive`, `ausearch --start today -m fanotify -i`, the `rules.d` directory, and the `fapolicyd-cli` options `--file add`, `--trust-file`, `--update`, `--check-trustdb`, `--dump-db`, `--check-config`, `--check-rules --lint`. Removed: the description of default rule contents (including /tmp and home), the CPU-cost claim for sha256, the claim that the database refreshes automatically after rpm updates (replaced by the documented dnf plugin), `ausearch -m FANOTIFY -ts recent`, and the CIS and RHEL guide citations (not fetched).
Method: documentation only; no commands were run.
