---
id: computing-software.cloud-infrastructure-engineering.ansible.template-backup-ownership-and-modes
name: template-backup-ownership-and-modes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, jinja2-templates, template-backup, template-module, file-permissions]
level: intro
status: docs-checked
description: "Set owner, group, mode, SELinux context and backup on the template module, keep timestamped backups and restore from them, and avoid insecure default modes."
sources: ["https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/modules/template.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/modules/copy.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/doc_fragments/files.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/module_utils/basic.py", "https://github.com/ansible/ansible-lint/blob/main/docs/rules/risky-file-permissions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# template: backup, owner and mode

```yaml
- name: Render sshd_config
  ansible.builtin.template:
    src: sshd_config.j2
    dest: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: "0600"
    backup: true
    validate: /usr/sbin/sshd -t -f %s
  register: sshd_conf
  notify: Restart sshd
```

## backup
- `backup: true` (default false) keeps the previous file in the same directory as `dest`, named `<dest>.<pid>.<YYYY-MM-DD@HH:MM:SS>~` (for example `sshd_config.12345.2026-10-18@10:22:01~`). The template module hands the file to the `copy` code, which makes the backup only when the content differs (or `dest` is a symlink), the destination exists, and the run is not in check mode.
- The backup path is returned as `backup_file`; capture it for rollback:
```yaml
- name: Restore previous config on failure
  ansible.builtin.copy:
    src: "{{ sshd_conf.backup_file }}"
    dest: /etc/ssh/sshd_config
    remote_src: true
  when: sshd_conf.backup_file is defined
```
- Backups accumulate. To prune them use `ansible.builtin.find` (`paths`, `patterns: 'sshd_config.*~'`, `age: 30d` selects files at least 30 days old) and remove the results with `ansible.builtin.file: state=absent`.

## Mode
- Quote the mode: `"0644"`. The module documentation says to quote octal numbers so Ansible converts the string itself, that a leading zero (`0755`) "works sometimes, but can fail in loops and some other circumstances", and that a number given without either form is read as decimal, with unexpected results.
- Symbolic modes work: `u=rw,g=r,o=r`.
- Without `mode`, a new file gets the system default umask permissions and an existing file keeps its mode. Specifying `mode` is documented as the best way to ensure correct permissions (CVE-2020-1736 is cited), and ansible-lint's `risky-file-permissions` rule covers `template` among other modules.

## Ownership and SELinux
`owner` and `group` set the file's ownership. The shared file options include the SELinux context settings `setype`, `seuser`, `serole` and `selevel`.

## Other useful options
`force: false` (only write the file if `dest` does not exist), `follow: true` (follow symlinks), `newline_sequence`, `output_encoding`.

## Verify
```bash
ansible host -m ansible.builtin.stat -a 'path=/etc/ssh/sshd_config'
```
The result shows `mode` and the owner (`pw_name`) and group (`gr_name`).

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5). Confirmed in `module_utils/basic.py` (`backup_local` naming), `modules/copy.py` (when `backup_file` is created and returned), the `template_common`, `backup` and `files` doc fragments (`mode` guidance, `force`, `follow`, SELinux options), `modules/find.py` (`age`, `patterns`), `modules/stat.py` return fields, and ansible-lint's `risky-file-permissions` rule page. Removed the `become` ownership remark and the claim about SELinux defaults, which the documentation does not state.
Method: documentation only; no commands were run.
