---
id: computing-software.systems-network-administration.patch-management.noninteractive-apt-upgrades-and-conffiles
name: noninteractive-apt-upgrades-and-conffiles
category: computing-software
field: systems-network-administration
product: patch-management
tags: [dpkg-conffile, debian-frontend-noninteractive, apt-full-upgrade, linux-patching, ansible-patching, ubuntu]
level: practitioner
status: docs-checked
description: "Run apt upgrades unattended without hanging on prompts: DEBIAN_FRONTEND, dpkg --force-confdef/confold, needrestart and debconf prompts, and reviewing .dpkg-dist files after."
sources:
  - https://manpages.debian.org/stable/dpkg/dpkg.1.en.html
  - https://manpages.debian.org/stable/debconf-doc/debconf.7.en.html
  - https://manpages.debian.org/stable/apt/apt-get.8.en.html
  - https://github.com/liske/needrestart
  - https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/apt.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-interactive apt upgrades and conffile handling

Automation hangs forever when dpkg asks "Configuration file '/etc/ssh/sshd_config' ...
modified... What would you like to do?" or a debconf dialog appears.

## The command
```sh
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get -y \
  -o Dpkg::Options::=--force-confdef \
  -o Dpkg::Options::=--force-confold \
  upgrade            # or dist-upgrade when package removals/new dependencies are allowed
```
- `--force-confdef`: take the package default action when there is one (new file if you
  never modified it).
- `--force-confold`: when modified locally, **keep your version**; the maintainer's version
  is saved as `<file>.dpkg-dist`.
- `--force-confnew` installs the maintainer version and keeps yours as `.dpkg-old`; use only
  if config is fully managed by config management that will re-apply it.

## Other prompts
- **needrestart** (where installed) can show a service restart dialog: set
  `$nrconf{restart} = 'a';` in `/etc/needrestart/needrestart.conf` (automatic restarts, so plan
  for service interruptions) or `'l'` (list only), or set `NEEDRESTART_MODE=a` / `l`. If it is
  configured as interactive but runs non-interactively it falls back to list only. A non-empty
  `NEEDRESTART_SUSPEND` stops the apt hook from running needrestart at all.
- **debconf questions**: `DEBIAN_FRONTEND=noninteractive` makes debconf use the default answer for
  every question. If a package needs a non-default answer, preseed it (see debconf(7)).
  `DEBIAN_PRIORITY=critical` shows only critical questions when a frontend is in use.

## Ansible
```yaml
- ansible.builtin.apt:
    upgrade: dist
    update_cache: true
    dpkg_options: "force-confdef,force-confold"
  environment:
    DEBIAN_FRONTEND: noninteractive
    NEEDRESTART_MODE: a
```

## After the upgrade: review new defaults
```sh
find /etc -name '*.dpkg-dist' -o -name '*.dpkg-old' | sort
diff -u /etc/ssh/sshd_config /etc/ssh/sshd_config.dpkg-dist
```
Merge security-relevant changes into your managed config; delete the files when done.

## Gotchas
- `upgrade` never removes packages and never installs new ones, so updates that need new
  dependencies are held back; `dist-upgrade` may remove packages: review
  `apt-get -s dist-upgrade` first.
- Interrupted dpkg leaves unpacked but unconfigured packages: `dpkg --configure -a`
  configures them.

## Verify
Unattended run completes without TTY; no `.dpkg-dist` files older than one cycle;
`dpkg --audit` clean.

## Checked

Checked 2026-10-27 against the Debian stable manpages (dpkg, apt-get, debconf), the Ansible apt module source, and the needrestart manual page and sample config.
- dpkg --force-confdef/confold/confnew semantics, .dpkg-dist (kept old, new saved) and .dpkg-old (new installed, old saved), and `dpkg --configure -a`: confirmed.
- `apt-get upgrade` never removes packages or installs new ones; `dist-upgrade` may remove: confirmed.
- needrestart `$nrconf{restart}` modes, `NEEDRESTART_MODE`, `NEEDRESTART_SUSPEND`, interactive fallback to list only: confirmed.
- DEBIAN_FRONTEND=noninteractive uses defaults, DEBIAN_PRIORITY: confirmed. Ansible `apt` `upgrade: dist` and `dpkg_options` (defaults force-confdef,force-confold): confirmed.
- Removed unconfirmed: Ubuntu release gate for needrestart, grub-pc preseed example, `.dpkg-new`/`.ucf-dist` scan.
Method: documentation only; no commands were run.
