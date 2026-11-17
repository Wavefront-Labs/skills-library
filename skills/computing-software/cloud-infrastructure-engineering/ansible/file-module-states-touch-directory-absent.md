---
id: computing-software.cloud-infrastructure-engineering.ansible.file-module-states-touch-directory-absent
name: file-module-states-touch-directory-absent
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, files-archives, file-state, touch, file-module]
level: intro
status: docs-checked
description: "Use ansible.builtin.file states correctly: file, directory, touch, link, hard and absent, idempotent touch with preserved times, and recursive directory ownership."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# file module states

```yaml
- name: Directory tree
  ansible.builtin.file:
    path: /srv/app/releases
    state: directory
    owner: app
    group: app
    mode: "0750"            # intermediate directories are created with the supplied permissions

- name: Empty marker file, idempotent
  ansible.builtin.file:
    path: /srv/app/.maintenance
    state: touch
    mode: "0644"
    modification_time: preserve
    access_time: preserve

- name: Remove a directory and contents
  ansible.builtin.file:
    path: /srv/app/tmp
    state: absent
```

| state | Effect | Idempotent |
|---|---|---|
| `file` (default when `state` is omitted) | set attributes of an **existing** file; fails if the path is a directory or other non-file; with no other options it just reports current info | yes |
| `directory` | create (with parents) | yes |
| `touch` | create, or update access and modification times | only with `modification_time: preserve` and `access_time: preserve` (otherwise times default to now and it reports changed) |
| `link` / `hard` | symlink / hardlink (`src` required) | yes |
| `absent` | delete file, link or whole directory tree | yes |

## Recursion
`recurse: true` (only with `state: directory`) applies the attributes to the contents; a numeric mode such as `0750` is applied to files too, so files become executable. Symbolic modes (for example `u=rwX,g=rX,o=`) are supported, including `X`.

## Gotchas
- `state: file` does not create files; use `touch` or `copy` with `content`. A missing path makes it fail.
- `absent` removes files, links and directories recursively and does not fail when the path is already gone.
- `follow` defaults to true (since 2.5): attribute changes go to the symlink target, and `follow` plus `state=link` can modify `src`.
- For `state=link`, `src` may be a path that does not exist yet; relative `src` is relative to `path`. `force` replaces an existing file at `path` with a link.
- Quote octal modes (`"0644"`); an unquoted number is read as decimal.
- The module does not support Windows targets: use `win_file`.

## Verify
```bash
ansible host -m ansible.builtin.stat -a 'path=/srv/app/releases'
```

## Checked
Checked 2026-10-25 against ansible-core devel `modules/file.py` documentation and code, `plugins/doc_fragments/files.py` and `module_utils/basic.py` (commit of 2026-10). Confirmed: state semantics, intermediate directories created with the supplied permissions (corrected), `touch` idempotency with `preserve` (source shows changed only when attributes or timestamps differ), failure of `state=file` on a missing path, `follow` default, symlink `src` rules, symbolic modes with `X`, check mode and partial diff support. Removed unconfirmed claims about mount points and NFS root squash.
Method: documentation only; no commands were run.
