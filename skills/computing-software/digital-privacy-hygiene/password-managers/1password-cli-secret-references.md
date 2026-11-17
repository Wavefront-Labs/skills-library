---
id: computing-software.digital-privacy-hygiene.password-managers.1password-cli-secret-references
name: 1password-cli-secret-references
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, 1password-cli, password-manager-cli, op-run, op-read, op-inject, secret-references, dotenv, biometric-unlock]
level: practitioner
status: docs-checked
description: "Replace plaintext secrets in .env files and scripts with 1Password secret references resolved at runtime by op run, op read and op inject."
sources:
  - "https://developer.1password.com/docs/cli/"
  - "https://developer.1password.com/docs/cli/secret-references/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 1Password CLI secret references

**Goal:** no API keys or passwords in plaintext files on disk, repos or shell history.

## Reference syntax
`op://<vault-name>/<item-name>/[section-name/]<field-name>`. Vault, item, section and field can each be given by name or unique identifier; the section is optional.

## Three ways to use them
```bash
# 1. read a single value
op read op://development/GitHub/credentials/personal_token
op read op://development/GitHub/credentials/personal_token --out-file token.txt

# 2. run a command; op run scans environment variables for references,
#    resolves them and runs the command in a subprocess
op run --env-file=node.env -- ./deploy.sh

# 3. render a template (stdin/stdout by default; -i / -o for files)
op inject -i config.yml.tpl -o config.yml
```
- `op run` masks secrets printed to stdout by default; `--no-masking` shows them.
- If you use `$MY_VAR` in the same command line as `op run`, your shell may expand it first: export it beforehand or wrap in `sh -c`.
- `op read` query parameters return metadata: field attributes `type`, `value`, `title`, `id`, `purpose`, `otp`; file attributes `content`, `size`, `id`, `name`, `type`. `ssh-format=openssh` returns an SSH private key in OpenSSH format.
- Files and templates that contain only references can be committed to Git.

## Sign-in
The CLI overview says the CLI can be unlocked with your fingerprint via app integration, and that service accounts can limit which vaults the CLI reaches and support automation when a personal account uses SSO or MFA. Details are on linked pages not covered here.

## Gotchas (judgement)
- `op inject` writes plaintext output; delete it after use or prefer `op run`.
- A service-account token is itself a secret.

## Verify
- [ ] Search the project for your secret's known prefix finds nothing.
- [ ] `op run` succeeds and values are masked in output.

## Checked
Method: 2026-11-08 read the secret-references page and the CLI overview (both now served at 1password.dev). Removed as unsupported: install steps, the Settings > Developer menu path, `op vault list`, Copy Secret Reference menu path, advice on spaces in names.
