---
id: computing-software.cloud-infrastructure-engineering.ansible.templating-directory-trees-with-filetree
name: templating-directory-trees-with-filetree
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, jinja2-templates, filetree, template-tree, community-general, directory-templates]
level: practitioner
status: docs-checked
description: "Render a whole directory of templates to a target, recreating subdirectories and symlinks, with the community.general.filetree lookup and a three-task loop."
sources: ["https://github.com/ansible-collections/community.general/blob/main/plugins/lookup/filetree.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/modules/copy.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Templating directory trees with filetree

`ansible.builtin.template` handles one file. For a tree (`/etc/myapp/` with conf.d, certs dirs,
symlinks), use `community.general.filetree`, which recursively walks a local directory and returns one item per
directory, file or symlink with `path` (relative to the root), `state` (`directory`, `file` or `link`), `mode`, `owner`,
`group`, `size`, `src` (not returned for directories) and more. Other file types are skipped.

```yaml
- name: Create directories
  ansible.builtin.file:
    path: "/etc/myapp/{{ item.path }}"
    state: directory
    mode: "{{ item.mode }}"
  loop: "{{ query('community.general.filetree', 'templates/myapp/') }}"
  when: item.state == 'directory'

- name: Render files
  ansible.builtin.template:
    src: "{{ item.src }}"
    dest: "/etc/myapp/{{ item.path | splitext | first }}"   # drops the .j2 suffix
    mode: "{{ item.mode }}"
  loop: "{{ query('community.general.filetree', 'templates/myapp/') }}"
  when: item.state == 'file'
  loop_control: {label: "{{ item.path }}"}
  notify: Restart myapp

- name: Recreate symlinks
  ansible.builtin.file:
    src: "{{ item.src }}"
    dest: "/etc/myapp/{{ item.path }}"
    state: link
    follow: false      # avoid corrupting target files if the link already exists
    force: true
  loop: "{{ query('community.general.filetree', 'templates/myapp/') }}"
  when: item.state == 'link'
```
If you give more than one path the lookup uses first_found logic and skips entries already seen in earlier paths, which lets you merge trees in order of importance. Newer versions of the collection add an `exclude` option (a regular expression matched against the base name, for example to skip `.git`).

## Removing files no longer in the tree
The lookup only lists what exists locally, so it adds and updates but never removes. To prune:
```yaml
- ansible.builtin.find: {paths: /etc/myapp, recurse: true, file_type: file}
  register: present
- ansible.builtin.file: {path: "{{ item }}", state: absent}
  loop: "{{ present.files | map(attribute='path') | difference(wanted) }}"
  vars:
    wanted: "{{ query('community.general.filetree', 'templates/myapp/') | selectattr('state','eq','file')
               | map(attribute='path') | map('splitext') | map('first') | map('regex_replace','^','/etc/myapp/') | list }}"
```

## Alternatives
- Static files only: `ansible.builtin.copy` with a directory `src`; a trailing `/` copies only the contents, no trailing `/` copies the directory itself (like rsync).
- Few files: a plain list in vars and one template task.

## Gotchas
- Every file in the loop that you pass to `template` is rendered as Jinja: binary files or files containing `{{` (Go templates) break. Keep them in a separate tree copied with `copy`, or wrap with `{% raw %}`.
- Large trees mean one task item per file per host; consider an archive for big trees.
- `community.general` must be installed on the control node (lookups run there).

## Verify
- [ ] `--check --diff` on a converged host reports no changes.
- [ ] The deployed tree has the same structure as the source tree (minus `.j2`).

## Checked
Date 2026-10-24. Documentation: the `community.general.filetree` plugin source on GitHub (options, return fields, `state` choices, first_found behaviour, `exclude` added in 12.0.0, example tasks including `follow: false` for links), the `copy` module documentation (directory `src` and trailing slash). Removed the `synchronize` alternative, the claim that the lookup searches a role's `templates/` and `files/` directories, and the git file-mode tip, none of which the documentation covers.
Method: documentation only; no commands were run.
