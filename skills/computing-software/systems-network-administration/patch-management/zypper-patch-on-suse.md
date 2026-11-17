---
id: computing-software.systems-network-administration.patch-management.zypper-patch-on-suse
name: zypper-patch-on-suse
category: computing-software
field: systems-network-administration
product: patch-management
tags: [zypper-patch, zypper, sles, opensuse, linux-patching, needs-rebooting, transactional-update]
level: practitioner
status: docs-checked
description: "Patch SUSE Linux Enterprise and openSUSE with zypper patches: listing by category and severity, security-only runs, interactive patches, restart checks and transactional updates."
sources:
  - https://documentation.suse.com/sles/15-SP6/html/SLES-all/cha-sw-cl.html
  - https://manpages.opensuse.org/Tumbleweed/zypper/zypper.8.en.html
  - https://documentation.suse.com/sle-micro/6.0/html/Micro-transactional-updates/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zypper patch on SUSE

**Goal:** apply SUSE's tested patch sets (with metadata about severity and restarts) rather than blind package updates.

## Patches vs updates
- `zypper patch` installs **patches**: vendor-defined bundles with category (security, recommended, optional, feature), severity and restart flags. It updates the package manager stack first if a patch for it exists.
- `zypper update` (`up`) updates all packages to newest versions, including changes not delivered as patches.
On SLES servers, prefer `zypper patch` for routine patching.

## Commands
```bash
zypper refresh
zypper list-patches --category security --severity critical,important
zypper patch-check                       # counts needed patches; exit 100 = patches available, 101 = security patches available
zypper patch --category security -y
zypper patch --cve CVE-2026-12345        # a specific CVE
zypper info -t patch SUSE-SLE-Module-Basesystem-15-SP6-2026-1234
```

## Interactive and licence patches
Some patches need a reboot or licence acceptance and are skipped in non-interactive runs. Use:
```bash
zypper --non-interactive patch --with-interactive --auto-agree-with-licenses
```
only in automated windows where reboots are allowed. `--auto-agree-with-licenses` accepts the licences of all third-party software the command installs. Exit code 103 means a patch for the package manager itself was installed: run the command again.

## After patching
```bash
zypper needs-rebooting                  # exit code 102 = reboot suggested
zypper ps -s                            # processes still using deleted files (short table)
zypper ps -sss                          # only the names of services that may need a restart
```

## Transactional systems (SLE Micro, openSUSE MicroOS)
```bash
transactional-update patch               # checks for patches and installs them into a new snapshot
reboot                                   # new snapshot becomes active
transactional-update rollback            # sets the current snapshot as default; add a number or `last`, then reboot
```
Each `transactional-update` change creates a separate snapshot; reboot between runs to combine changes.

## Gotchas
- Systems registered to SUSE Manager/RMT receive only the channels/products enabled there; check `zypper lr` when patches seem missing.
- Locks (`zypper locks`) silently hold packages back.

## Verify
`zypper patch-check` reports 0 security patches needed, and `zypper needs-rebooting` is clean after the reboot.

## Checked

Checked 2026-10-27 against the zypper manual page (openSUSE) and the SUSE Linux Micro transactional-update guide (6.0).
- `zypper patch`/`list-patches` options `--category`, `--severity`, `--cve`, `--with-interactive`, `--auto-agree-with-licenses`: confirmed; interactive patches (reboot, message, licence) are skipped in non-interactive mode.
- `zypper patch-check` exit codes 100/101, `needs-rebooting` exit code 102, exit code 103 (package manager updated), `zypper ps -s/-sss`: confirmed.
- `transactional-update patch`, `rollback [number|last]`, reboot to activate the snapshot: confirmed in the SLE Micro guide.
- Locks (`/etc/zypp/locks`, `zypper locks`) hold packages back: confirmed.
Method: documentation only; no commands were run.
