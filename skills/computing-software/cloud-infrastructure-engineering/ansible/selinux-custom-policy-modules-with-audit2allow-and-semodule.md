---
id: computing-software.cloud-infrastructure-engineering.ansible.selinux-custom-policy-modules-with-audit2allow-and-semodule
name: selinux-custom-policy-modules-with-audit2allow-and-semodule
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, selinux, custom-policy-module, audit2allow, semodule, checkmodule, type-enforcement, avc-denials, rhel]
level: advanced
status: docs-checked
description: "Write, review, compile and deploy a custom SELinux policy module with audit2allow, checkmodule and semodule from Ansible, idempotently and only after booleans and contexts fail."
sources: ["https://github.com/SELinuxProject/selinux/blob/main/python/audit2allow/audit2allow.1", "https://github.com/SELinuxProject/selinux/blob/main/policycoreutils/semodule/semodule.8", "https://github.com/SELinuxProject/selinux/blob/main/checkpolicy/checkmodule.8", "https://github.com/linux-system-roles/selinux/blob/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELinux custom policy modules (audit2allow, semodule)

Goal: allow one specific, reviewed access that no boolean, port label or file context grants, and
ship it to every host as a versioned module. It is the last resort: try `seboolean`, `sefcontext`
and `seport` first (`audit2why` tells you if a boolean fixes it).

## 1. Capture the denials (on a test host)
```bash
setenforce 0                           # permissive briefly so ALL denials show, not just the first
# exercise the app end to end
ausearch -m AVC,USER_AVC -ts recent -c myapp > myapp.avc
audit2why < myapp.avc                  # boolean or context fix available?
audit2allow -m myapp_local < myapp.avc > myapp_local.te   # human-readable TE source
setenforce 1
```
**Read the `.te`.** Reject anything granting broad types (`unconfined_t`, `default_t`,
`shadow_t`, `*_exec_t` execute on random paths) — that usually means a missing file context.

## 2. Keep the source in the repo
`roles/selinux_myapp/files/myapp_local.te`:
```
module myapp_local 1.2;
require {
    type httpd_t;
    type myapp_var_t;
    class sock_file write;
    class unix_stream_socket connectto;
}
allow httpd_t myapp_var_t:sock_file write;
```
Bump the module version in the `module` line on every change; `semodule` uses it.

## 3. Compile and install from Ansible
```yaml
- name: Copy TE source
  ansible.builtin.copy: {src: myapp_local.te, dest: /etc/selinux/local/myapp_local.te, mode: "0644"}
  register: te

- name: Build and load module
  when: te is changed
  ansible.builtin.shell: |
    set -e
    cd /etc/selinux/local
    checkmodule -M -m -o myapp_local.mod myapp_local.te
    semodule_package -o myapp_local.pp -m myapp_local.mod
    semodule -i myapp_local.pp
  # needs checkpolicy and policycoreutils packages
```
Alternative: the `selinux` system role (`rhel-system-roles.selinux`) installs a local `.pp` or `.cil` file with
`selinux_modules: [{path: myapp_local.pp, state: enabled}]` (default priority 400); building modules from source on the nodes is not supported by the role.
For a `.cil` module `semodule -i myapp_local.cil` works without compiling.

## 4. Removal
`semodule -r myapp_local` (or a role entry with `name: myapp_local` and `state: absent`).

## Gotchas
- `audit2allow -M <name>` generates a loadable `.pp` package (and its `.te`); teams then load it without reading the `.te`. Always review the TE.
- `dontaudit` rules hide some denials; `semodule -DB` disables them while capturing, `semodule -B` restores.
- Build modules on the same OS release you deploy to, or ship CIL source (`semodule -i` accepts `.cil`).
- The `shell` task above only reruns on TE change; if a host lost the module (`semodule -l | grep myapp_local` empty), add a check task to force the build.

## Verify
- [ ] `semodule -l | grep myapp_local` shows the module on every host.
- [ ] In enforcing mode the app works and `ausearch -m AVC -ts recent -c myapp` is empty.

## Checked

Checked 2026-10-26 against the SELinux userspace manual pages on GitHub (main) and the linux-system-roles selinux README. Confirmed: `audit2allow` `-m` (module source), `-M` (loadable package), `-w` (why); `checkmodule` `-m` (non-base module), `-M` (MLS) and `-o`; `semodule` `-i` / `--install`, `-r` / `--remove` (priority 400 by default), `-B` / `--build`, `-D` / `--disable_dontaudit`, `-l`; the system role's `selinux_modules` entries (`path` `.pp` or `.cil`, `name`, `priority` default 400, `state` enabled, disabled or absent) and that it does not build modules from source. Removed the RHEL 8 versus 9 policy-version claim. Also confirmed `semodule_package -o <output> -m <module>` and the `ausearch` options `-m` (comma-separated record types, including avc and user_avc), `-c` and `-ts recent`.

Method: documentation only; no commands were run.
