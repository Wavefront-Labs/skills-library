---
id: computing-software.cloud-infrastructure-engineering.ansible.splitting-group-vars-into-directories-with-vault-files
name: splitting-group-vars-into-directories-with-vault-files
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, group-vars, host-vars, vars-directories, split-vars-files, vault-group-vars, vars-and-vault, ansible-vault]
level: practitioner
status: docs-checked
description: "Split group_vars/<group>/ and host_vars/<host>/ into several files, keep secrets in an encrypted vault.yml beside plain vars, and reference them via vault_ prefixed names."
sources: ["How to build your inventory, organizing host and group variables (https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#organizing-host-and-group-variables)", "Tips and tricks, keeping vaulted variables visible (https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)", "Encrypting content with Ansible Vault (https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html)", "host_group_vars vars plugin source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/vars/host_group_vars.py)", "DataLoader.find_vars_files source (https://github.com/ansible/ansible/blob/devel/lib/ansible/parsing/dataloader.py)", "Configuration settings, YAML_FILENAME_EXTENSIONS and DEFAULT_HASH_BEHAVIOUR (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Split group_vars into directories with vault files

The `host_group_vars` vars plugin accepts either `group_vars/web.yml` **or** a directory
`group_vars/web/` whose files are all loaded and merged.

```
inventory/production/
  hosts.yml
  group_vars/
    all/
      00-common.yml
      ntp.yml
      vault.yml          # ansible-vault encrypted
    web/
      nginx.yml
      tls.yml
      vault.yml
  host_vars/
    db1.example.com/
      main.yml
      vault.yml
```

## Load rules
- Files are read in sorted (lexical) order; later files overwrite earlier keys (the default `hash_behaviour` is `replace`). Prefix with numbers when order matters, but better: never define the same key in two files.
- Accepted extensions: `.yml`, `.yaml`, `.json`, or none (`[defaults] yaml_valid_extensions`, env `ANSIBLE_YAML_FILENAME_EXT`). Other extensions are ignored; hidden files (starting with `.`) and backup files ending in `~` are ignored too.
- Subdirectories inside `group_vars/web/` are loaded recursively.

## The vault indirection pattern
```yaml
# group_vars/web/vault.yml  (encrypted)
vault_tls_key_passphrase: s3cr3t
vault_api_token: abc123

# group_vars/web/tls.yml  (plain, greppable)
tls_key_passphrase: "{{ vault_tls_key_passphrase }}"
api_token: "{{ vault_api_token }}"
```
Why: `grep -r api_token` still finds where a variable is defined and used, diffs of plain files stay
reviewable, and only `vault.yml` is opaque.
```bash
ansible-vault create inventory/production/group_vars/web/vault.yml
ansible-vault edit   inventory/production/group_vars/web/vault.yml
ansible-vault view   inventory/production/group_vars/web/vault.yml
```
With multiple vault IDs per environment: `ansible-vault create --vault-id prod@prompt ...`
and run with `--vault-id prod@prod-password-file` (a password file path after the `@`, or `prompt`).

## Gotchas
- Do not keep both `group_vars/web.yml` and `group_vars/web/`: the loader looks for the directory first and stops at the first match, so `web.yml` is ignored when `web/` exists. Pick one form.
- Encrypting single values with `encrypt_string` inside plain files is the alternative; do not mix both styles within one group.
- The vars plugin caches applicable paths and file content, so creating or editing `group_vars`/`host_vars` files mid-play for hosts already targeted has no effect on that run.

## Verify
- [ ] `ansible-inventory -i inventory/production --host web1 --vault-id ...` shows merged values from every file.
- [ ] `head -1 group_vars/*/vault.yml` shows `$ANSIBLE_VAULT;1.1;AES256` (or 1.2 with id) for every vault file; add this as a pre-commit check.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5 sources.
- Confirmed in `DataLoader` and the `host_group_vars` plugin: directory entries are processed in sorted order and recursively, hidden and `~` files are skipped, extensions limited to `.yml`, `.yaml`, `.json` or none; contents are merged with `combine_vars` (default `hash_behaviour` is `replace`); file content is cached.
- Confirmed in the vault docs: headers `$ANSIBLE_VAULT;1.1;AES256` and `$ANSIBLE_VAULT;1.2;AES256;<id>`, `--vault-id <id>@prompt` and `<id>@<password file>`, `ansible-vault create/edit/view` and `encrypt_string`; the `vault_` prefix pattern from the tips page.
- Fixed: having both `group_vars/web.yml` and `group_vars/web/` does not load both; the directory wins and the file is ignored.
- Removed as unconfirmed: the claim that an undecryptable file fails the run even when its variables are unused, and the claim that `~` backups are not ignored on some versions (they are ignored).

Method: documentation only; no commands were run.
