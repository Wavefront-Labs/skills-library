---
id: computing-software.cloud-infrastructure-engineering.ansible.posix-acls-with-ansible
name: posix-acls-with-ansible
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, files-archives, acl, posix-acl, setfacl, default-acl]
level: practitioner
status: docs-checked
description: "Grant extra users or groups access to files and directories with ansible.posix.acl, including default ACLs for new files, recursion, and the mask that silently limits rights."
sources: ["https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/acl.py", "https://man7.org/linux/man-pages/man5/acl.5.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# POSIX ACLs with Ansible

Classic permissions allow one owner and one group. ACLs add more: "the deploy user may write to
`/srv/app` owned by root:www-data".

```yaml
- name: Deploy user may write app dir
  ansible.posix.acl:
    path: /srv/app
    entity: deploy
    etype: user              # user | group | mask | other
    permissions: rwx
    state: present

- name: Same for files created later (default ACL)
  ansible.posix.acl:
    path: /srv/app
    entity: deploy
    etype: user
    permissions: rwx
    default: true
    state: present

- name: Monitoring group can read logs recursively
  ansible.posix.acl:
    path: /var/log/app
    entity: monitoring
    etype: group
    permissions: rX           # capital X: execute only on dirs (and already-executable files)
    recursive: true
    state: present
```
Remove: `state: absent` with the same entity/etype. `state` defaults to `query`, which only reads the ACL, so always set `state: present` or `absent` explicitly.

## The mask
The ACL mask caps the effective rights of named users, named groups and the owning group.
`chmod g-w` on a file with ACLs **lowers the mask** — the deploy user's `rwx` becomes effective
`r-x`. `getfacl` shows `#effective:r-x`. Set the mask explicitly if tools chmod files (the module's `recalculate_mask` option, `default`, `mask` or `no_mask`, controls whether `setfacl` recomputes it):
```yaml
- ansible.posix.acl: {path: /srv/app, etype: mask, permissions: rwx, state: present}
```

## Requirements
- ACLs must be enabled on the target filesystem.
- The `setfacl` and `getfacl` binaries (the `acl` package on most distributions) must be installed on the target; the module calls them. Linux only.

## Gotchas
- `recursive: true` walks the whole tree; on huge trees prefer default ACLs on the top directory plus a one-time recursive set.
- `use_nfsv4_acls: true` switches the module to `nfs4_setfacl` / `nfs4_getfacl` for NFSv4 ACLs.
- Changing file permission bits (for example `mode:` on `copy` or `template`) modifies the associated ACL entries, including the mask: re-apply the mask afterwards or avoid group bits in `mode`.

## Verify
- [ ] `getfacl /srv/app` shows `user:deploy:rwx` and `default:user:deploy:rwx` with no `#effective` reduction.
- [ ] `sudo -u deploy touch /srv/app/x` succeeds.

## Checked

Checked 2026-10-26 against the ansible.posix `acl` module source (main) and acl(5) on man7.org. Confirmed: `etype` choices user, group, mask, other; `permissions` letters including capital `X`; `default`, `recursive`, `use_nfsv4_acls` and `recalculate_mask` options; `state` choices absent, present, query with default `query`; the module needs `setfacl` and `getfacl` and ACL support on the filesystem; acl(5): with a mask entry the group permission bits correspond to the mask, changing permission bits changes the ACL entries, effective rights are limited by the mask, and a directory's default ACL becomes the initial access ACL of new objects. Removed the claims about ext4/xfs defaults, recursive idempotence, NFSv3 and tar/rsync flags, which no page confirms.

Method: documentation only; no commands were run.
