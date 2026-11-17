---
id: computing-software.cybersecurity-defensive.system-hardening.selinux-administration
name: selinux-administration
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, selinux, mac, enforcing-mode, audit2allow, semanage, file-contexts, booleans]
level: advanced
status: docs-checked
description: "Run SELinux in enforcing mode on RHEL-family hosts: diagnose denials with ausearch and sealert, fix with contexts, booleans and ports, and write minimal local policy modules."
sources: ["https://github.com/SELinuxProject/selinux-notebook/blob/main/src/global_config_files.md", "https://github.com/SELinuxProject/selinux-notebook/blob/main/src/auditing.md", "https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-fcontext.8", "https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-permissive.8", "https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-port.8", "https://github.com/SELinuxProject/selinux/blob/main/python/audit2allow/audit2allow.1", "https://github.com/SELinuxProject/selinux/blob/main/policycoreutils/semodule/semodule.8", "https://github.com/SELinuxProject/selinux/blob/main/policycoreutils/setsebool/setsebool.8", "https://github.com/containers/podman/blob/main/docs/source/markdown/options/volume.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELinux administration

**Goal:** keep SELinux enforcing and fix denials correctly instead of turning it off.

## State
- `getenforce`, `sestatus`; config `/etc/selinux/config` with `SELINUX=enforcing|permissive|disabled` and `SELINUXTYPE=<policy name>` (`targeted` on RHEL-family systems).
- Never `setenforce 0` globally to debug; make a single domain permissive: `semanage permissive -a httpd_t` (remove after).

## Diagnose a denial
```
ausearch -m AVC,USER_AVC -ts recent
```
Read the AVC: `scontext` (process domain), `tcontext` (target label), `tclass`, permission. Without the audit daemon, AVC messages go to the system log (audit2allow(1)).

## Fix in this order
1. **Wrong file label** (for example content moved into a new directory):
   `semanage fcontext -a -t httpd_sys_content_t "/srv/www(/.*)?"` then `restorecon -Rv /srv/www`.
   `semanage fcontext` records the persistent labelling rule; `restorecon` applies it to files.
2. **Boolean** for a supported behaviour: `getsebool -a | grep httpd`; `setsebool -P httpd_can_network_connect_db on`.
3. **Non-standard port:** `semanage port -a -t http_port_t -p tcp 8443`.
4. **Custom policy module** as last resort, reviewed:
   `ausearch -m AVC -c myapp --raw | audit2allow -M myapp_local` then read `myapp_local.te` before `semodule -i myapp_local.pp`.
   Never blindly install audit2allow output; it generates whatever rules allow the logged denials, however broad.

## Hidden denials
`dontaudit` rules suppress some AVCs; `semodule -DB` disables them temporarily, `semodule -B` restores.

## Containers
Podman relabels bind-mounted volumes when `:z` (shared label for several containers) or `:Z` (private label for this container) is added to the mount.

## Verify
- [ ] `getenforce` returns Enforcing on all hosts (config management check).
- [ ] No unexplained AVCs in the last 24 h for production services.
- [ ] Local modules (`semodule -l | grep local`) are in version control with justification.

## Checked
Checked 2026-10-25 against the SELinux Notebook (SELinuxProject/selinux-notebook: configuration and auditing chapters, 2026-10-21), the SELinux userspace manual pages (SELinuxProject/selinux, 2026-10-16: semanage-fcontext, semanage-permissive, semanage-port, audit2allow, semodule, setsebool) and the Podman volume option text (containers/podman, 2026-10-23). Confirmed: `/etc/selinux/config` keys, AVC fields (`scontext`, `tcontext`, `tclass`), `semanage fcontext -a -t ...` and `semanage port -a -t http_port_t -p tcp`, `semanage permissive --add`, `setsebool -P`, `audit2allow -M`, `semodule -D` (temporarily removes dontaudits) and `-B` (rebuild reverts it), `ausearch -m ... -ts recent -c`, Podman `:z`/`:Z`. Removed unconfirmed: the sealert/setroubleshoot step, chcon-versus-relabel claim, the execmem/shadow_t examples and the container_t remark. Red Hat documentation and the CIS benchmark were not read.

Method: documentation only; no commands were run.
