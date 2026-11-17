---
id: computing-software.cloud-infrastructure-engineering.ansible.copy-with-inline-content-backup-and-validate
name: copy-with-inline-content-backup-and-validate
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, files-archives, copy-content, copy, validate]
level: intro
status: docs-checked
description: "Use ansible.builtin.copy with inline content, backup and validate for small config files, choose copy vs template, and handle remote_src and directory copies."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/copy.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# copy: content, backup and validate

## Inline content
```yaml
- name: sudoers drop-in, validated
  ansible.builtin.copy:
    dest: /etc/sudoers.d/automation
    content: |
      automation ALL=(ALL) NOPASSWD: ALL
    owner: root
    group: root
    mode: "0440"
    validate: /usr/sbin/visudo -csf %s
    backup: true
```
- `content` sets the file contents directly (it works only when `dest` is a file); the docs say to use `template` for advanced formatting or when the content contains a variable.
- `validate` runs the command with `%s` replaced by the temporary file; `%s` is required, and a non-zero exit fails the task before the destination is replaced.
- `backup: true` keeps a copy of the previous file, with timestamp information, when it is replaced; the name is returned as `backup_file`.

## copy vs template
| Use | Module |
|---|---|
| static file from role `files/` | copy |
| small generated snippet | copy with content |
| Jinja logic | template |
| file already on the target | copy with `remote_src: true` |

## Directories
```yaml
- ansible.builtin.copy:
    src: files/conf.d/        # trailing slash: copy contents
    dest: /etc/app/conf.d/
- ansible.builtin.copy:
    src: files/conf.d         # no slash: copy the directory itself
    dest: /etc/app/
```
The docs note that the recursive copy facility does not scale to lots (more than hundreds) of files; they list `ansible.posix.synchronize` as a related module.

## Gotchas
- `content` with a trailing newline matters: YAML `|` adds one, `|-` strips it.
- `force: false` only creates the file when missing (good for seeding).
- `remote_src: true` supports recursive copying as of version 2.8; `force` defaults to `true` (replace when contents differ).

## Verify
- [ ] Run the task twice: the second run reports no change.

## Checked
Checked 2026-10-26 against ansible-core devel `lib/ansible/modules/copy.py` (options, notes, seealso, validate code).
Confirmed: `content`, `backup`, `force` default true, `remote_src` and recursive support from 2.8, `%s` in `validate`
and failure on non-zero exit, `backup_file` return value, the recursive-copy scaling note. Removed unconfirmed claims
about `--diff` output and an ad-hoc verification command.
Method: documentation only; no commands were run.
