---
id: computing-software.cloud-infrastructure-engineering.ansible.becoming-an-unprivileged-user-and-temp-file-permissions
name: becoming-an-unprivileged-user-and-temp-file-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, become, become-unprivileged, allow-world-readable-tmpfiles, setfacl, remote-tmp, become-user, non-root-become, chmod-failed, acl-package, pipelining-become, ansible-tmp, world-readable]
level: practitioner
status: docs-checked
description: "Fix 'Failed to set permissions on the temporary files' when become_user is non-root: install acl, use pipelining, remote_tmp, and only last allow world-readable temp files."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_privilege_escalation.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/doc_fragments/shell_common.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Becoming an unprivileged user and temp file permissions

## 1. Why it fails
When both the connection user (for example `automation`) and the `become_user` (for example
`postgres`) are unprivileged, the module file is written as the connection user but must be
readable by the become user. Ansible tries these in order:
1. POSIX ACLs, if `setfacl` is in the remote `PATH` and the temp directory's filesystem supports POSIX.1e ACLs.
2. `chown` of the module file, on systems that allow an unprivileged user to do so.
3. `chmod +a` (macOS ACLs; ansible-core 2.11+).
4. `chgrp` to the group in `ansible_common_remote_group` (2.10+), if set. Ansible does not check that
   the become user is really in that group, and does not fall back further once `chgrp` succeeds.
5. If none worked, the `world_readable_temp` shell option: when enabled the module is placed in a
   world-readable temporary directory with world-readable permissions.

If all fail and the option is off, the task fails with: "Failed to set permissions on the temporary
files Ansible needs to create when becoming an unprivileged user". Becoming root, or connecting as
root and then becoming another user, does not hit this because the file is protected by normal permissions.

## 2. Fixes, best first
1. Install the package that provides `setfacl` on the managed node (frequently `acl`; check your OS
   documentation); the temp directory must be on a filesystem with POSIX ACL support.
   ```yaml
   - ansible.builtin.package:
       name: acl
       state: present
     become: true
   ```
   On Solaris ZFS the ACLs are NFSv4, not POSIX.1e, so Ansible cannot use them; the docs suggest `world_readable_temp` there.
2. Pipelining: the module is piped to the remote Python interpreter's stdin, so no temp file is saved.
   Set `pipelining = True` in `[defaults]` or `[connection]` (env `ANSIBLE_PIPELINING`). It does not
   work for Python modules that transfer files (`copy`, `fetch`, `template`) or for non-Python
   modules, and with sudo you must first disable `requiretty` in `/etc/sudoers` on the managed hosts.
3. Avoid becoming an unprivileged user: connect as root and become the user, or run the privileged
   work as root.
4. Set `ansible_common_remote_group` to a group that both users share (needs `chgrp` to succeed).
5. Last resort: `world_readable_temp`. Set it with the variable `ansible_shell_allow_world_readable_temp: true`,
   the env var `ANSIBLE_SHELL_ALLOW_WORLD_READABLE_TEMP`, or `allow_world_readable_tmpfiles = True` in `[defaults]`.
   It turns the error into a warning, and any module arguments (including secrets) may be readable by other users on the host.

## 3. Worked example
```yaml
- hosts: db
  become: true
  tasks:
    - name: ACL support for become_user
      ansible.builtin.package:
        name: acl
    - name: Run as postgres
      community.postgresql.postgresql_query:
        db: app
        query: SELECT 1
      become_user: postgres
```

## Gotchas
- If both `ansible_common_remote_group` and `world_readable_temp` are set, the world-readable fallback is unlikely to trigger, and Ansible emits a warning.
- The fix is on the managed node (or connection settings), not on the control node.

## Verify
- [ ] `ansible db -b --become-user postgres -m command -a whoami` prints `postgres`.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_privilege_escalation.rst) and ansible-core devel
sources (`shell_common.py` doc fragment, `config/base.yml`; devel is 2.23 dev). Confirmed: fallback order, version
gates (2.10, 2.11), ZFS note, pipelining limits, `requiretty` note, and the names of the `world_readable_temp`
option (ini key `allow_world_readable_tmpfiles`, env `ANSIBLE_SHELL_ALLOW_WORLD_READABLE_TEMP`, variable
`ansible_shell_allow_world_readable_temp`). Fixed the old env var name. Removed unconfirmed claims about
`remote_tmp`, `su` prompts, SELinux and Controller execution environments.
Method: documentation only; no commands were run.
