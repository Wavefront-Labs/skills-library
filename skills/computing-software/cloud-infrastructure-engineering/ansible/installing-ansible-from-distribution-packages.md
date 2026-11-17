---
id: computing-software.cloud-infrastructure-engineering.ansible.installing-ansible-from-distribution-packages
name: installing-ansible-from-distribution-packages
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, control-node, ansible-install, distro-packages, rhel-ansible-repo, apt-ansible-ppa, dnf, apt, ansible-core, aap-repo, epel, ubuntu-ppa, subscription-manager]
level: practitioner
status: docs-checked
description: "Install ansible or ansible-core from OS packages instead of pip: Fedora, EPEL, Ubuntu PPA, Debian, openSUSE, Arch; when to prefer pipx or pip."
sources: ["https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html", "https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Ansible from distribution packages

**Goal:** a control node whose Ansible is patched through the OS package manager. The Ansible
docs say these distro instructions come from the distribution communities; Ansible itself
maintains only the `pip install` instructions.

## Packages
- `ansible` is the full community package (many collections); `ansible-core` is the minimal
  runtime with only the built-in modules and plugins. Collections are then installed
  separately.
- Fedora: `sudo dnf install ansible` or `sudo dnf install ansible-core`. Several collections
  are packaged separately, for example `sudo dnf install ansible-collection-community-general`.
- CentOS Stream, AlmaLinux, Rocky and related: enable the community EPEL repository, then use
  the same `dnf` commands as Fedora.
- openSUSE Tumbleweed/Leap: `sudo zypper install ansible`.
- Arch Linux: `sudo pacman -S ansible` or `sudo pacman -S ansible-core`.
- Ubuntu: a PPA carries newer versions than the standard repositories:
  ```bash
  sudo apt update
  sudo apt install software-properties-common
  sudo add-apt-repository --yes --update ppa:ansible/ansible
  sudo apt install ansible
  ```
- Debian: the main repository has `ansible`, but it can be outdated. The docs describe adding
  the Ubuntu PPA with a keyring and an apt sources entry, mapping Debian 13 to `noble`,
  Debian 12 to `jammy` and Debian 11 to `focal`; follow the current page rather than
  `apt-key add`, which is deprecated.
- Windows cannot be an Ansible control node.

## Package vs pip
| Need | Use |
|---|---|
| OS-managed updates | distro package |
| Distro blocks `pip` (externally managed Python) | `pipx install --include-deps ansible` or `pipx install ansible-core` |
| Specific core version | `pipx install ansible-core==<version>` or `python3 -m pip install --user ansible-core==<version>` |

## Gotchas
- Package maintainers fix package issues, not Ansible: file bugs with the distribution
  (Fedora and EPEL in Red Hat Bugzilla; the Ubuntu PPA in its issue tracker).
- See the Ansible package release status table for which `ansible-core` version a given
  `ansible` release contains.
- Red Hat subscribers installing from the Ansible Automation Platform repository should follow
  the Red Hat documentation for their release; that site could not be read for this review.

## Verify
- [ ] `ansible --version` shows the expected core version.
- [ ] The installed package version (`rpm -q ansible-core` or `dpkg -l ansible-core`) matches the version in your change record.

## Checked
2026-11-09. Confirmed in the Ansible installation docs (distros page and installation intro):
all commands and package names above, the Debian to Ubuntu codename table, pipx and pip
commands, Windows not supported. Removed as unconfirmed: RHEL AppStream versions, the AAP
repository id and package list, EPEL package size and mixing advice, Debian/Ubuntu default
versions, Homebrew, Python-interpreter and dnf versionlock/apt-mark gotchas, the old 2.9 note,
and the docs.redhat.com source (unreadable).
Method: documentation only; no commands were run.
