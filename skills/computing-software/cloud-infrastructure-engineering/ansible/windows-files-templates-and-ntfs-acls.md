---
id: computing-software.cloud-infrastructure-engineering.ansible.windows-files-templates-and-ntfs-acls
name: windows-files-templates-and-ntfs-acls
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, windows-automation, win-copy, win-acl, win-template, win-file, ntfs-permissions, win-owner]
level: practitioner
status: docs-checked
description: "Copy files and render templates to Windows hosts with win_copy and win_template, create folders with win_file, and set NTFS permissions, inheritance and owners with win_acl."
sources: ["https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_copy.py", "https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_template.py", "https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_acl.py", "https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_acl_inheritance.py", "https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_owner.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows files, templates and NTFS ACLs

Linux file modules (`copy`, `file`, `template`) do not work on Windows; use the `win_` ones.

## Files and templates
```yaml
- ansible.windows.win_file:
    path: <DRIVE>:\Apps\Shop\logs
    state: directory

- ansible.windows.win_copy:
    src: files/shop/          # trailing slash: copy contents
    dest: <DRIVE>:\Apps\Shop\
    backup: true

- ansible.windows.win_template:
    src: appsettings.json.j2
    dest: <DRIVE>:\Apps\Shop\appsettings.json
    newline_sequence: "\r\n"   # the default for win_template
  notify: Recycle shop app pool
```
Paths: in YAML use single backslashes inside unquoted or single-quoted strings
(`<DRIVE>:\Apps`); in double quotes escape them (`"<DRIVE>:\\Apps"`). Forward slashes also work for most modules.
`remote_src: true` copies from a path on the target host itself.

## NTFS permissions
```yaml
- name: App pool identity can modify logs
  ansible.windows.win_acl:
    path: <DRIVE>:\Apps\Shop\logs
    user: IIS AppPool\Shop
    rights: Modify               # .NET FileSystemRights names such as FullControl, Modify, ReadAndExecute
    type: allow
    state: present
    inherit: ContainerInherit, ObjectInherit
    propagation: None

- name: Stop inheriting from <DRIVE>:\Apps, keep current entries as explicit
  ansible.windows.win_acl_inheritance:
    path: <DRIVE>:\Apps\Shop\secrets
    state: absent
    reorganize: true

- name: Remove broad access
  ansible.windows.win_acl:
    path: <DRIVE>:\Apps\Shop\secrets
    user: BUILTIN\Users
    rights: ReadAndExecute
    type: allow
    state: absent

- ansible.windows.win_owner:
    path: <DRIVE>:\Apps\Shop
    user: BUILTIN\Administrators
    recurse: true
```
Order matters: for `state: absent`, `reorganize: true` copies the inherited ACEs to the folder, so do this before removing an inherited entry.

## Gotchas
- `win_copy` takes no backup when `remote_src` is false and several files are copied, so `backup: true` on a directory copy has no effect.
- `win_acl` `inherit` accepts `ContainerInherit` and `ObjectInherit` and defaults to both for directories; `propagation` defaults to `None`.
- `win_template` renders on the controller; `output_encoding` defaults to `utf-8` (set another encoding if the application needs it).

## Verify
- [ ] `ansible.windows.win_shell: (Get-Acl <DRIVE>:\Apps\Shop\logs).Access | ft IdentityReference,FileSystemRights,IsInherited` matches the intent.
- [ ] Second run reports no changes.

## Checked

Checked 2026-10-26 against the ansible.windows module sources (main). Confirmed: `win_copy` `remote_src`, `backup` and the no-backup rule for multi-file copies; `win_template` `newline_sequence` default `\r\n` and `output_encoding` default utf-8; `win_acl` `inherit` choices and default, `propagation` choices (default None), `type` allow or deny, `state` present or absent; `win_acl_inheritance` `state` (default absent) and `reorganize`; `win_owner` `user` and `recurse`. Removed the UNC delegation remark, the exact-match removal claim and the performance advice, which the module pages do not state.

Method: documentation only; no commands were run.
