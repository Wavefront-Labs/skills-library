---
id: computing-software.cloud-infrastructure-engineering.ansible.vault-encrypted-files-and-vault-identity-list
name: vault-encrypted-files-and-vault-identity-list
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-vault, vault-encrypted-files, vault-identity-list, vault-id]
level: practitioner
status: docs-checked
description: "Encrypt whole files (keys, certs, binaries) for copy and template with ansible-vault, decrypt-on-copy behaviour, and set default vault IDs with vault_identity_list."
sources: ["Ansible vault guide, encrypting content (https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html)", "Ansible vault guide, using encrypted content (https://docs.ansible.com/ansible/latest/vault_guide/vault_using_encrypted_content.html)", "Ansible vault guide, managing passwords and vault IDs (https://docs.ansible.com/ansible/latest/vault_guide/vault_managing_passwords.html)", "Ansible configuration reference (https://docs.ansible.com/ansible/latest/reference_appendices/config.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vault-encrypted files and vault_identity_list

## Whole-file encryption
```bash
ansible-vault encrypt --vault-id prod@prompt roles/web/files/server.key
ansible-vault encrypt --vault-id prod@path/to/password_file files/license.bin
```
`--vault-id label@source` takes a source of `prompt`, a password file or an executable script, and the label is stored in clear text in the file header (`$ANSIBLE_VAULT;1.2;AES256;prod`).
```yaml
- name: Install TLS key (decrypted on the fly)
  ansible.builtin.copy:
    src: server.key            # vault-encrypted in files/
    dest: /etc/pki/tls/private/server.key
    owner: root
    mode: "0600"
    decrypt: true              # default: auto-decrypt a vaulted src
```
- If an encrypted file is the `src` of `copy`, `template`, `unarchive`, `script` or `assemble`, it is decrypted and is **not** encrypted on the target host (given the right vault password).
- Auto-decryption does not work with `remote_src: true` in `copy`. Set `decrypt: false` to ship the file still encrypted.
- The `ansible.builtin.unvault` lookup returns the contents of vaulted (or plain) files on the controller, for use in variables.

## When to use file vs variable encryption
| Content | Approach |
|---|---|
| keys, certs, kubeconfigs, binaries | whole-file vault |
| individual values inside YAML | `ansible-vault encrypt_string` |
| many secrets per environment | a vaulted vars file per environment |
File-level encryption lets you `rekey` files; encrypted variables cannot be rekeyed. Ansible decrypts every encrypted file referenced in a playbook when it loads, whereas encrypted variables are decrypted on demand.

## vault_identity_list
Supply default vault IDs so nobody types `--vault-id` every run:
```ini
[defaults]
vault_identity_list = dev@dev.pass, prod@prod-client.sh
vault_id_match = true
vault_encrypt_identity = dev
```
- `ANSIBLE_VAULT_IDENTITY_LIST` is the environment form; the entries act like several `--vault-id` options and are tried in order.
- `vault_id_match` (default `false`): by default the label is only a hint and Ansible tries each password, starting with the one whose label matches; when `true`, only the password for the matching vault ID is tried. Ansible still does not enforce using the same password every time for a given label.
- `vault_encrypt_identity` sets the vault ID used for encrypting by default; `--encrypt-vault-id` overrides it. `vault_identity` is the label used when none is given (default `default`).

## Verify
```bash
head -1 roles/web/files/server.key        # $ANSIBLE_VAULT;1.2;AES256;prod
```

## Checked
Checked 2026-10-23 against the Ansible vault guide source and ansible-core source on GitHub (vault_encrypting_content.rst, vault_using_encrypted_content.rst, vault_managing_passwords.rst, config/base.yml, modules/copy.py, doc_fragments/decrypt.py, plugins/lookup/unvault.py; latest ansible-core release v2.21.5): header format, the list of modules that decrypt a vaulted `src`, the `decrypt` option (default true) and the `remote_src` limitation, `DEFAULT_VAULT_IDENTITY_LIST`, `DEFAULT_VAULT_ID_MATCH`, `DEFAULT_VAULT_ENCRYPT_IDENTITY`, `DEFAULT_VAULT_IDENTITY` and the label-matching behaviour. Wrong claim fixed: with `vault_id_match = false` Ansible tries every password but starts with the matching label; the skill described it as slower and hiding mislabeled files. Removed the unconfirmed claims that `lookup('file')` decrypts, that `--diff` prints plaintext for vaulted templates, and the example home-directory password paths.
Method: documentation only; no commands were run.
