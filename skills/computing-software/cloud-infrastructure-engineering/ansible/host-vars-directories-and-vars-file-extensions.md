---
id: computing-software.cloud-infrastructure-engineering.ansible.host-vars-directories-and-vars-file-extensions
name: host-vars-directories-and-vars-file-extensions
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, group-host-vars, host-vars-directory, vars-file-extensions, host-vars]
level: intro
status: docs-checked
description: "Lay out host_vars/<host>/ directories with multiple files, and know which file names and extensions the host_group_vars plugin loads or ignores."
sources: ["https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/vars/host_group_vars.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_inventory.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# host_vars directories and file extensions

## Layout
```
inventory/
  hosts.yml
  host_vars/
    db01.example.com/        # directory named exactly like the inventory host name
      main.yml
      vault.yml              # ansible-vault encrypted
      backups.yml
    web01.example.com.yml    # single file form
  group_vars/
    all/
      common.yml
```
The default `host_group_vars` vars plugin loads these files. Ansible reads all the files in a host or group directory in lexicographical order and merges them: a later file replaces an earlier one's variable of the same name (the `hash_behaviour` setting defaults to `replace`; the configuration documentation advises against changing it).

## Names must match exactly
The directory or file name must equal the inventory host name (the alias), not `ansible_host`. If the inventory says `db01 ansible_host=10.0.0.5`, the file is `host_vars/db01.yml`. An FQDN versus short-name mismatch is a common reason for "my host vars are ignored".

## Extensions loaded
The plugin accepts `.yml`, `.yaml`, `.json` or no extension (default of `yaml_valid_extensions` in `[defaults]`, environment variable `ANSIBLE_YAML_FILENAME_EXT`). Files with other extensions are skipped, so these are ignored:
- `main.yml.bak`, `main.yml.orig`, `vars.yml~` (editor backups): good.
- `vault.txt`, `secrets.vault`: probably not what you intended.

Hidden files and directories (starting with `.`) and backup files (ending with `~`) are ignored. A file with **no** extension is loaded, so a `README` inside `host_vars/web01/` would be read as YAML; name it `README.md`.

## Where they are read from
The plugin searches paths relative to the inventory source and relative to the playbook file; with `ansible-playbook`, variables sourced relative to the playbook override those sourced relative to the inventory source. Commands without a playbook (`ansible`, `ansible-console`, `ansible-inventory`) use `--playbook-dir`. The plugin applies only to inventory sources that are existing paths; put `host_vars/` beside a dynamic inventory plugin's config file.

## Verify
```bash
ansible-inventory -i inventory --host db01.example.com
ansible -i inventory db01.example.com -m ansible.builtin.debug -a 'var=backup_schedule'
```
The first command prints the merged variables for the host.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed in the `host_group_vars` vars plugin documentation and code (extensions `.yml`, `.yaml`, `.json` or none, hidden and `~` files ignored, existing-path sources only, lexicographic loading), the inventory guide ("Organizing host and group variables": alias-based names, playbook-relative overrides inventory-relative, `--playbook-dir`), and `DEFAULT_HASH_BEHAVIOUR` and `YAML_FILENAME_EXTENSIONS` in `config/base.yml`. Removed the `jq` pipeline and the "number one cause" ranking.
Method: documentation only; no commands were run.
