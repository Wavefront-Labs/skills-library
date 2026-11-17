---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-vault-secrets-management
name: ansible-vault-secrets-management
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-vault, vault-id, vault-password-file, vault-password-client, encrypt-string, rekey, secrets-management, no-log, vault-indirection, git-textconv, sops, community-sops, hashicorp-vault, hashi-vault-lookup, aws-secrets-manager, secret-rotation, ci-secrets, encryption-at-rest, vault-edit, vault-view]
level: practitioner
status: docs-checked
description: "Manage Ansible secrets with Vault: per-env vault IDs, password client scripts, vars/vault indirection, encrypt_string, rekey rotation, readable git diffs, no_log, external stores."
sources: ["https://docs.ansible.com/ansible/latest/vault_guide/index.html", "https://docs.ansible.com/ansible/latest/vault_guide/vault_managing_passwords.html", "https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html", "https://docs.ansible.com/ansible/latest/vault_guide/vault_using_encrypted_content.html", "https://github.com/ansible-collections/community.sops"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Ansible Vault secrets management — encrypted in Git, readable in review, rotatable

**Goal:** secrets are committed only encrypted, each environment has its own key so a
stage leak does not expose prod, reviewers can still see *which* variable changed, and
rotating a vault password is a routine command.

## 1. Vault IDs per environment
```bash
ansible-vault create --vault-id prod@prompt inventories/prod/group_vars/all/vault.yml
ansible-playbook site.yml -i inventories/prod --vault-id prod@scripts/vault-client.py
```
- The file header records the label: `$ANSIBLE_VAULT;1.2;AES256;prod`.
- Several `--vault-id` flags may be given. By default the label is only a hint: Ansible does not check that it matches the header of the encrypted data.
- Set `vault_identity_list = prod@scripts/vault-client.py, stage@scripts/vault-client.py` under `[defaults]`
  in `ansible.cfg` (a list, equivalent to several `--vault-id` flags, tried in order) only on machines meant to hold both.
- `vault_id_match = True` (`DEFAULT_VAULT_ID_MATCH`, default false) makes Ansible decrypt data only with the password whose label matches, which catches mislabelled files. It does not enforce which password is used for a label.

## 2. Never keep the password in a plain file in the repo
A password source can be `@prompt`, a file, or an **executable**. A script whose name
ends in `-client` (e.g. `vault-client.py`) is called with `--vault-id <label>` and must
print the password:
```python
#!/usr/bin/env python3
import argparse, os
p = argparse.ArgumentParser(); p.add_argument("--vault-id", default="default")
label = p.parse_args().vault_id
# replace the environment lookup with your keyring or secrets-manager call
print(os.environ["VAULT_PASSWORD_" + label.upper()])
```
The password must be printed on a single line. In CI, inject it from the CI secret store (environment
variable or a temp file with mode 0600).

## 3. Indirection: plain names, vaulted values
```yaml
# group_vars/all/vars.yml  (plain, greppable)
db_password: "{{ vault_db_password }}"
# group_vars/all/vault.yml (encrypted)
vault_db_password: "<SET_ME>"
```
Everyone can find where `db_password` comes from without decrypting anything.
For a single value inside a plain file:
```bash
ansible-vault encrypt_string --vault-id prod@prompt --name 'api_token' '<VALUE>'
```
(paste output into YAML; typing the value on the command line leaves it in shell history, so use `--stdin-name` and read from stdin or the prompt).

## 4. Edit, view, diff
```bash
ansible-vault edit --vault-id prod@prompt group_vars/all/vault.yml
ansible-vault view ...
```
Whole-file encryption hides variable names and changes the whole ciphertext on each edit, so keep vault
files small and separate, with plain indirection variables as in section 3.

## 5. Rotation
```bash
ansible-vault rekey --vault-id prod@old-pass-client.py --new-vault-id prod@prompt \
  $(grep -rl '^\$ANSIBLE_VAULT;1.2;AES256;prod' inventories/)
```
`rekey` works on whole files only; encrypted variables (`encrypt_string`) cannot be rekeyed and must be
re-encrypted individually. Rekeying does **not** rotate the secrets themselves — if a vault password
leaked, also rotate every credential it protected, because history still holds the old ciphertext.

## 6. Keep secrets out of logs
- `no_log: true` on tasks that receive secrets (users, DB grants, API calls). It hides
  module args *and* results, so add a non-sensitive debug task when troubleshooting.
- Do not `register` secret-bearing output and then `debug: var=`.

## 7. When Vault is the wrong tool
Use runtime lookups when secrets rotate often or are shared with apps:
the `community.hashi_vault.vault_kv2_get` and `amazon.aws.secretsmanager_secret` lookups,
`azure.azcollection.azure_keyvault_secret`, or SOPS-encrypted files via `community.sops`.

## Gotchas
- Vault encrypts at rest only; values are plaintext in memory, in facts, and in templates written to hosts — set file `mode: "0600"`.
- Without a label the header is format 1.1 (`$ANSIBLE_VAULT;1.1;AES256`); labelled data uses 1.2.

## Verify
- [ ] `git grep -L '^\$ANSIBLE_VAULT' -- '*vault.yml'` returns nothing (no unencrypted vault files).
- [ ] Stage credentials cannot decrypt prod files (`ansible-vault view` with the stage ID fails).
- [ ] No vault password file is tracked by Git (`git ls-files | grep -i vault-pass` is empty).
- [ ] A `-v` run of the playbook shows `censored` for every secret task.
- [ ] Rotation runbook has been executed once in non-prod.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/vault_guide (managing passwords, encrypting content, using encrypted content): header format `$ANSIBLE_VAULT;1.2;AES256;<label>`, labels are hints unless DEFAULT_VAULT_ID_MATCH is set, client scripts end in `-client` or `-client.EXTENSION`, are executable and are called with `--vault-id <label>`, `encrypt_string --stdin-name`, `rekey --vault-id ... --new-vault-id ...`, encrypted variables cannot be rekeyed, 1.1 versus 1.2 format.
- Confirmed in config/base.yml: DEFAULT_VAULT_ID_MATCH (ini vault_id_match, default False) and DEFAULT_VAULT_IDENTITY_LIST (ini vault_identity_list, a list tried in order).
- Confirmed lookup and plugin files exist in the collection repositories: community.hashi_vault vault_kv2_get, amazon.aws secretsmanager_secret, azure.azcollection azure_keyvault_secret, community.sops sops.
- Removed unconfirmed claims: git textconv diff recipe, AWS CLI client example, vars_files failure behaviour, encrypt_string indentation gotcha, -vvv log remark, the 1.1/label uncertainty note.

Method: documentation only; no commands were run.
