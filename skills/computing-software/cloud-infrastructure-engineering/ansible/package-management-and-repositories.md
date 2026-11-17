---
id: computing-software.cloud-infrastructure-engineering.ansible.package-management-and-repositories
name: package-management-and-repositories
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, package-management, package-module, dnf, yum, yum-repository, apt, apt-repository, deb822-repository, apt-key, rpm-key, package-facts, pip, dnf-versionlock, epel, gpg-keys, update-cache, patching, security-updates, autoremove, rhsm, redhat-subscription]
level: practitioner
status: docs-checked
description: "Install and pin packages across distros with Ansible: dnf/apt/package modules, repository and GPG key setup, package_facts for conditionals, version locks, security-only patching and cache handling."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/dnf_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/apt_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/deb822_repository_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yum_repository_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_facts_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/reboot_module.html", "https://github.com/rpm-software-management/dnf-plugins-core/blob/master/doc/needs_restarting.rst", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/dnf_versionlock.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package management and repositories

**Goal:** the right packages at the right versions on every distro, from repos you
control, with no `shell: yum install` and no surprise upgrades.

## 1. Choose the module
- `ansible.builtin.dnf` (with `ansible.builtin.dnf5` as a separate backend selectable through `use_backend`), `ansible.builtin.apt`, `community.general.zypper`, `ansible.builtin.package` (generic; calls the manager module for the discovered OS, but package *names* still differ and are not translated).
- Pattern: `package` for common names (`git`, `curl`), per-manager tasks with `when: ansible_facts.pkg_mgr == 'apt'` where names or options differ, or an OS-keyed var map:
```yaml
pkgs:
  RedHat: [httpd, mod_ssl]
  Debian: [apache2]
- ansible.builtin.package: {name: "{{ pkgs[ansible_facts.os_family] }}", state: present}
```

## 2. Repositories and keys
```yaml
- ansible.builtin.rpm_key: {key: https://repo.example/RPM-GPG-KEY, state: present}
- ansible.builtin.yum_repository:
    name: internal
    description: Internal mirror
    baseurl: https://repo.example/rhel/$releasever/$basearch
    gpgcheck: true
    gpgkey: https://repo.example/RPM-GPG-KEY
    enabled: true
# Debian-family: deb822_repository replaces the deprecated apt_key module
- ansible.builtin.deb822_repository:
    name: docker
    types: deb
    uris: https://download.docker.com/linux/ubuntu
    suites: "{{ ansible_facts.distribution_release }}"
    components: stable
    signed_by: https://download.docker.com/linux/ubuntu/gpg
- ansible.builtin.apt: {update_cache: true, cache_valid_time: 3600}
```
`deb822_repository` `signed_by` accepts a URL to a GPG key, an absolute keyring path, or key fingerprints. For RHEL subscriptions see
`community.general.redhat_subscription` and `community.general.rhsm_repository`.

## 3. Install, pin, upgrade
```yaml
- ansible.builtin.dnf: {name: ["nginx-1.24*", "postgresql16-server"], state: present}   # name-version specifiers; globs are mentioned in the docs for package names
- ansible.builtin.apt: {name: "nginx=1.24.*", state: present, allow_downgrade: true}
- community.general.dnf_versionlock: {name: kernel*, state: present}      # states: present, absent, excluded, clean
- ansible.builtin.dpkg_selections: {name: nginx, selection: hold}          # install, hold, deinstall, purge
- ansible.builtin.dnf: {name: "*", state: latest, security: true, exclude: "kernel*"}  # security-only patch
- ansible.builtin.apt: {upgrade: safe, autoremove: true}                  # upgrade: dist, full, no, safe, yes
- ansible.builtin.dnf: {name: "@Development tools", state: present}        # package groups
```
`state: latest` is a floating version: fine for ad hoc patch runs, wrong in a role that
promises repeatability. `state: present` + explicit version where it matters.

## 4. Decide with package_facts
```yaml
- ansible.builtin.package_facts: {manager: auto}
- ansible.builtin.debug: {msg: "{{ ansible_facts.packages['openssl'][0].version }}"}
  when: "'openssl' in ansible_facts.packages"
```
Reports installed versions; the dnf module docs recommend `package_facts` over its `list` option.

## 5. Reboots after kernel/glibc
```yaml
- ansible.builtin.dnf: {name: "*", state: latest}
  register: upd
- ansible.builtin.command: needs-restarting -r     # RHEL family: exit code 1 means a reboot is required
  register: nr
  failed_when: nr.rc not in [0, 1]
  changed_when: nr.rc == 1
- ansible.builtin.reboot: {reboot_timeout: 900}
  when: nr.rc == 1
```

## Gotchas
- `update_cache: true` refreshes the apt cache; `cache_valid_time` skips the refresh when the cache is younger than that many seconds.
- `apt` has `lock_timeout` (default 60 seconds, since 2.12) and `dnf` has `lock_timeout` (default 30) for waiting on the package lock.
- `dnf` `name: "*"` with `state: latest` upgrades every package, including the kernel unless `exclude` covers it; pair with the reboot block.
- `apt_key` is deprecated in favour of `deb822_repository` (module docs).
- `package` passes all arguments to the underlying module, but its own documentation covers only the common ones; use the specific module for manager-specific options.
- `enablerepo`/`disablerepo` on `dnf` apply to that transaction only.

## Verify
- [ ] Second run reports `changed=0` for every repo/key/package task.
- [ ] `ansible all -m package_facts` followed by a `debug` confirms the expected version on each OS family.
- [ ] The repository definitions on the host list only the intended repos with GPG checking on.

## Checked
Checked 2026-10-26 against ansible-core devel `dnf.py`, `apt.py`, `package.py`, `package_facts.py`, `reboot.py`, `apt_key.py`,
`deb822_repository.py`, `yum_repository.py`, `dpkg_selections.py`, community.general `dnf_versionlock.py`, and dnf-plugins-core
`needs_restarting.rst`. Confirmed: option names and states used above, `signed_by` forms, `apt_key` deprecation, lock timeouts,
`needs-restarting -r` exit code 1, `package_facts` recommendation. Removed unconfirmed claims: Fedora 41 dnf5 date, EPEL URL,
Debian/Ubuntu version cut-offs, `/var/run/reboot-required`, apt "no candidate" behaviour, `pip` pin example and the
`dnf-utils` package name.
Method: documentation only; no commands were run.
