---
id: computing-software.cloud-infrastructure-engineering.ansible.zypper-pacman-and-homebrew-package-modules
name: zypper-pacman-and-homebrew-package-modules
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, packages-repos, zypper, pacman, homebrew, apk, package-module, cross-distro]
level: practitioner
status: docs-checked
description: "Manage packages on SUSE, Arch, Alpine and macOS with community.general zypper, pacman, apk and homebrew, and write cross-distro roles with package and os_family maps."
sources: ["https://github.com/ansible-collections/community.general/blob/main/plugins/modules/zypper.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/zypper_repository.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/pacman.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/apk.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/homebrew.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/homebrew_cask.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/homebrew_tap.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/facts/system/distribution.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zypper, pacman, apk and homebrew

## SUSE: zypper
```yaml
- community.general.zypper_repository:
    name: monitoring
    repo: https://download.opensuse.org/repositories/server:/monitoring/15.6/
    auto_import_keys: true
- community.general.zypper:
    name: [prometheus, "nginx>=1.24"]
    state: present
    type: package        # also pattern, patch, product, srcpackage, application
- community.general.zypper: {name: '*', state: latest}     # update all installed packages (state: dist-upgrade also exists; name should be '*')
```

## Arch: pacman
```yaml
- community.general.pacman:
    update_cache: true
    upgrade: true          # upgrade the whole system; cannot be combined with name
- community.general.pacman:
    name: [nginx, git]
    state: present
```
The module can use an AUR helper through `executable`, but its documentation says helpers can behave unexpectedly and are not recommended, and `yay` failed in its tests.

## Alpine: apk
```yaml
- community.general.apk:
    name: [curl, bash]
    update_cache: true
    no_cache: true         # container images
```

## macOS: homebrew
```yaml
- community.general.homebrew:
    name: [jq, wget]
    state: present
    update_homebrew: true
  become: false            # run as the user who owns the Homebrew install
- community.general.homebrew_cask:
    name: [iterm2]
- community.general.homebrew_tap:
    name: hashicorp/tap
```
The module's `path` option defaults to `/usr/local/bin:/opt/homebrew/bin` plus the default Linuxbrew bin directory; set it if brew lives elsewhere.

## Cross-distro roles
`ansible.builtin.package` dispatches to the detected manager (`ansible_facts.pkg_mgr`) for simple
install/remove, but names differ:
```yaml
# vars/main.yml
web_pkg:
  RedHat: httpd
  Debian: apache2
  Suse: apache2
  Archlinux: apache
# tasks
- ansible.builtin.package:
    name: "{{ web_pkg[ansible_facts.os_family] }}"
```
Use the specific module when you need repo/cache/upgrade options.

## Gotchas
- `os_family` for openSUSE/SLES is `Suse`; for Arch `Archlinux`; Alpine `Alpine`; macOS `Darwin`.
- Targets need Python for these modules; minimal images may need it installed first.

## Verify
- [ ] `ansible all -m package_facts` then check `ansible_facts.packages` contains the names on each family.

## Checked

Checked 2026-10-26 against the community.general module sources and the ansible-core distribution facts source (main / devel). Confirmed: `zypper` `type` choices package, patch, pattern, product, srcpackage, application; `name: '*'` with `state: latest`, and `dist-upgrade`; `zypper_repository` `auto_import_keys`; `pacman` `update_cache`, `upgrade` (not with `name`) and the AUR-helper warning; `apk` `update_cache` and `no_cache`; `homebrew` `update_homebrew` and the default `path`; `homebrew_cask` and `homebrew_tap` names; `os_family` values Suse, Archlinux, Alpine and Darwin. Removed the SUSEConnect, kewlfft.aur and brew-root claims, which no module page confirms.

Method: documentation only; no commands were run.
