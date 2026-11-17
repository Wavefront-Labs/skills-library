---
id: computing-software.cloud-infrastructure-engineering.ansible.generic-package-module-and-cross-distro-names
name: generic-package-module-and-cross-distro-names
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, packages-repos, generic-package, package-module, os-family]
level: intro
status: docs-checked
description: "Use ansible.builtin.package for cross-distro roles, map differing package names per OS family with vars files, and know when to switch to dnf or apt."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/package.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/config/ansible_builtin_runtime.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The generic package module

`ansible.builtin.package` calls the package manager module for the operating system discovered by `ansible.builtin.setup` (`ansible_facts['pkg_mgr']`) and runs `setup` itself if facts are missing.

```yaml
- name: Install web server (any distro)
  ansible.builtin.package:
    name: "{{ web_packages }}"
    state: present
```

## Different names per family
```yaml
# roles/web/vars/RedHat.yml
web_packages: [httpd, mod_ssl]
web_service: httpd
# roles/web/vars/Debian.yml
web_packages: [apache2]
web_service: apache2
```
```yaml
# roles/web/tasks/main.yml
- name: Load OS-specific vars
  ansible.builtin.include_vars: "{{ lookup('ansible.builtin.first_found', params) }}"
  vars:
    params:
      files:
        - "{{ ansible_facts['distribution'] }}-{{ ansible_facts['distribution_major_version'] }}.yml"
        - "{{ ansible_facts['os_family'] }}.yml"
      paths: [vars]
```

## Limits
`package` is a proxy: all arguments are passed to the underlying module, but its documentation covers only the minimum
intersection that all package modules support (`name`, `state`, `use`). Need more? Use the specific module:
- `update_cache`, `cache_valid_time` → apt.
- `enablerepo`, `disable_gpg_check`, `exclude`, `security`, `autoremove` → dnf.
- Name syntax varies with the manager (the docs give `name-1.0` versus `name=1.0`), and package names differ per distribution; the module does not translate them.
- `state: latest` works only where the underlying module supports it.

`use:` forces a backend (`use: dnf`; default `auto`). Since 2.17 the `ansible_package_use` variable can override detection, but `use` takes precedence.

## Gotchas
- If facts have not been gathered, `package` runs the `setup` module itself.
- `name` accepts a list (or comma-separated string, depending on the backend); a list lets the backend handle all packages in one call, a loop makes one call per item.
- In ansible-core's runtime configuration `yum` redirects to `ansible.builtin.dnf`; there is no separate yum module in core.

## Verify
- [ ] `ansible_facts['pkg_mgr']` on each host names the backend you expect.

## Checked
Checked 2026-10-26 against ansible-core devel `package.py` (description, options, notes) and
`ansible_builtin_runtime.yml` (`yum` redirect to `ansible.builtin.dnf`). Confirmed: proxy behaviour and minimum-intersection
arguments, `use` default `auto`, `ansible_package_use` since 2.17, `latest` only if supported, name syntax and no name
translation, running `setup` when facts are missing. Corrected: the claim that the yum module is gone in 2.17 now states the
runtime redirect. Removed unconfirmed claims about transaction behaviour per list versus loop and exact version pin forms
per manager.
Method: documentation only; no commands were run.
