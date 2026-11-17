---
id: computing-software.systems-network-administration.linux.sudo-l-listing-and-testing-privileges
name: sudo-l-listing-and-testing-privileges
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sudo, sudo-l, sudo-u, sudoers-audit, cvtsudoers, privilege-review]
level: practitioner
status: docs-checked
description: "Inspect what sudo allows: sudo -l and -ll for yourself, -l -U for another user, testing a command with sudo -l cmd, cvtsudoers for audits, and reading matching order."
sources:
  - https://github.com/sudo-project/sudo/blob/main/docs/sudo.mdoc.in
  - https://github.com/sudo-project/sudo/blob/main/docs/cvtsudoers.mdoc.in
  - https://github.com/sudo-project/sudo/blob/main/docs/sudoers.mdoc.in
  - https://github.com/SSSD/sssd/blob/master/src/man/sss_cache.8.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sudo -l: listing and testing privileges

## Commands
```bash
sudo -l                              # my rules on this host (may prompt for my password)
sudo -ll                             # long format: RunAs, options, tags per rule
sudo -l -U alice                     # root: alice's rules
sudo -l -U alice /usr/bin/systemctl restart nginx   # prints the full path if allowed, exits 1 if not
sudo -n true && echo "passwordless sudo available"   # -n never prompts
sudo -v                              # refresh credential timestamp; sudo -k invalidates it
```
## Running as other users/groups
`sudo -u postgres psql`, `sudo -g docker cmd`, `sudo -i` (login shell as the target user), `sudo -s` (shell), `sudo -E` (preserve the environment if the policy allows).

## Audits
```bash
cvtsudoers -f json /etc/sudoers > sudoers.json        # machine-readable JSON output
cvtsudoers -m user=alice -f sudoers /etc/sudoers      # only rules matching alice
cvtsudoers -f ldif /etc/sudoers                       # LDIF output (the default format) for LDAP
```
## Matching order matters
When several rules match, the **last** match is used (not necessarily the most specific). `alice ALL=(ALL) ALL` followed by `alice ALL=(ALL) !/bin/su` denies su,
but negations on commands are easy to bypass (for example by running a copy of the binary) — prefer explicit allow lists.
`Defaults` entries are applied in order, later entries overriding earlier ones; command-specific `Defaults!cmd` entries are applied later, once the command path is known (also `Defaults:alice` for users).

## Centrally managed sudo
Rules from a directory source (SSSD, LDAP) are listed by `sudo -l` as well; after rule changes `sss_cache -E` invalidates SSSD's cached entries; if `sudo -l` is slow, check SSSD health.

## Verify
- [ ] Quarterly review export (cvtsudoers) matches the access approval list; each admin's `sudo -l -U` has no unexpected ALL.

## Checked
Checked 2026-10-25 against the sudo-project/sudo manual sources and SSSD sss_cache(8).
Confirmed: `-l`, repeated `-l` for a longer list, `-U user` (restricted to root or users with the `list` privilege), the exit status 1 when a listed command is not allowed, `-n`, `-v`, `-k`, `-K`, cvtsudoers `-f json|ldif|sudoers` and `-m user=...`, last-match rule and Defaults ordering, `sss_cache -E`.
Removed as unconfirmed: the claim that cvtsudoers output includes expanded includes, and the nsswitch sudoers entry.

Method: documentation only; no commands were run.
