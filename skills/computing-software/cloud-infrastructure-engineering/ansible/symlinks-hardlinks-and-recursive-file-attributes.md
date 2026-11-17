---
id: computing-software.cloud-infrastructure-engineering.ansible.symlinks-hardlinks-and-recursive-file-attributes
name: symlinks-hardlinks-and-recursive-file-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, files-archives, symlink, hardlink, recurse, file-module, release-symlink]
level: practitioner
status: docs-checked
description: "Create symlinks and hard links with ansible.builtin.file, switch a current-release symlink atomically, and set owner and mode recursively without breaking idempotence."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/file.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/doc_fragments/files.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Symlinks, hard links and recursive attributes

## Symlinks
```yaml
- name: Point current at the new release
  ansible.builtin.file:
    src: /opt/app/releases/{{ app_version }}
    dest: /opt/app/current
    state: link
    force: true            # replace an existing link (or file) at dest
  notify: Restart app
```
- `state: link` makes `path` (alias `dest`) a symbolic link to `src`; options such as `mode` and `owner` are often not applicable on the link itself and depend on `follow`.
- `force: true` forces creation when the link is symbolic and `src` does not exist yet, or when the destination exists as a file (it is unlinked and replaced by the link).

## Hard links
```yaml
- ansible.builtin.file:
    src: /data/shared/config.json
    dest: /etc/app/config.json
    state: hard
```
`state: hard` makes `path` a hard link to `src`.

## Recursive owner and mode
```yaml
- name: App owns its data tree
  ansible.builtin.file:
    path: /srv/app/data
    state: directory
    owner: app
    group: app
    recurse: true
```
`recurse: true` applies the attributes to directory contents and only works with `state: directory`. A single
numeric `mode` applies to files and directories alike, so symbolic modes (supported since 1.8) are usually better:
```yaml
    mode: u=rwX,g=rX,o=     # X is the symbolic-mode flag for conditional execute
```

## Idempotence on large trees
On very large trees you can limit work to the entries that are wrong; this `find` approach is a pattern, not a module feature:
```yaml
- ansible.builtin.command: find /srv/app/data ! -user app -print -exec chown app:app {} +
  register: chowned
  changed_when: chowned.stdout | length > 0
```

## Gotchas
- `state: touch` creates an empty file or updates access and modification times, so it always reports changed (module docs).
- `modification_time` and `access_time` accept `preserve`, `now` or a timestamp in `%Y%m%d%H%M.%S` format by default.

## Verify
- [ ] `readlink -f /opt/app/current` points to the expected release.
- [ ] A second run of the `file` tasks reports no change.

## Checked
Checked 2026-10-26 against ansible-core devel `file.py` documentation block and the `files` doc fragment. Confirmed `state`
choices (`link`, `hard`, `touch`), `force` cases, `recurse` (directory only), `follow`, `touch` always changing,
`modification_time`/`access_time` values and format, symbolic modes since 1.8. Removed unconfirmed claims: relative link
resolution, hard-link filesystem limits, Python walk performance, directory-replacement failure, SELinux link contexts and the
atomic-switch advice.
Method: documentation only; no commands were run.
