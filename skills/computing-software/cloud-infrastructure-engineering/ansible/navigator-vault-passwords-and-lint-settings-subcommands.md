---
id: computing-software.cloud-infrastructure-engineering.ansible.navigator-vault-passwords-and-lint-settings-subcommands
name: navigator-vault-passwords-and-lint-settings-subcommands
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-navigator, navigator-vault, navigator-lint, navigator-settings]
level: practitioner
status: docs-checked
description: "Supply vault passwords to ansible-navigator runs safely, and use its lint, settings and config subcommands to run ansible-lint and inspect effective settings in the EE."
sources: ["ansible-navigator FAQ (https://github.com/ansible/ansible-navigator/blob/main/docs/faq.md)", "ansible-navigator subcommands (https://github.com/ansible/ansible-navigator/blob/main/docs/subcommands.md)", "ansible-navigator configuration source (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/configuration_subsystem/navigator_configuration.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# navigator: vault passwords, lint and settings

## Vault passwords
Prompts (`--ask-vault-pass`, `--ask-pass`, `vars_prompt`) need `--enable-prompts` (`--ep`, added in navigator v2.3), which switches to stdout mode and disables playbook artifact creation.
```bash
ansible-navigator run site.yml --enable-prompts --ask-vault-pass
```
Non-interactive options from the navigator FAQ (do not keep password files in source control):
1. A project script that echoes the password from an environment variable, with the variable passed through to the execution environment:
```bash
ANSIBLE_VAULT_PASSWORD="$(~/bin/vault.sh)" ansible-navigator run site.yml --senv=ANSIBLE_VAULT_PASSWORD_FILE=vault.sh --penv=ANSIBLE_VAULT_PASSWORD
```
2. A password file linked into the project directory and `ANSIBLE_VAULT_PASSWORD_FILE` passed with `--pass-environment-variable`.
3. `ANSIBLE_VAULT_PASSWORD_FILE` pointing at an executable script that prints the password; variables whose names start with `ANSIBLE` are passed into the execution environment automatically, according to the FAQ.

`--senv` sets and `--penv` passes an environment variable into the execution environment. Artifacts can be switched off with `playbook-artifact: {enable: false}` (`--pae false`) or saved elsewhere with `save-as`.

## lint
```bash
ansible-navigator lint roles/ -m stdout
ansible-navigator lint --lint-config .ansible-lint playbooks/site.yml    # short form: --lic
```
`lint` runs ansible-lint on the given path (default: the current directory). With an execution environment, ansible-lint must be installed in the image; without one it must be installed on the host. Running lint in the production EE gives the same collections and ansible-core version.

## settings and config
```bash
ansible-navigator settings --effective -m stdout     # navigator's own settings with sources
ansible-navigator settings --sample > ansible-navigator.yml   # generate a sample settings file (--gs)
ansible-navigator settings --sources -m stdout            # where each value came from
ansible-navigator config dump -m stdout --only-changed   # ansible-config view as the EE sees it
ansible-navigator config list -m stdout
```
`settings --effective` combines defaults, the settings file, environment variables and CLI parameters; `--sources` shows the source of each entry. In stdout mode `config` accepts the same parameters as `ansible-config`.

## Verify
- [ ] A CI run decrypts vault without prompts and the stored artifacts and logs contain no plaintext secrets.

## Checked
Checked 2026-10-23 against the ansible-navigator repository on GitHub (docs/faq.md, docs/subcommands.md, navigator_configuration.py): `--enable-prompts` behaviour and version (v2.3), the FAQ's vault password approaches with `--senv`/`--penv`, the `lint` subcommand notes and `--lint-config`/`--lic`, `settings --effective/--sources/--sample/--schema`, `playbook-artifact.enable` and `config` stdout parity with ansible-config. Removed the unconfirmed `<EE_HOME>` mount recipe, `--vault-id` path advice and the claim about supported dev-tools images.
Method: documentation only; no commands were run.
