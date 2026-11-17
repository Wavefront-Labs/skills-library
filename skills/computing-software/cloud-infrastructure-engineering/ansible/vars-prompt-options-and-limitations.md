---
id: computing-software.cloud-infrastructure-engineering.ansible.vars-prompt-options-and-limitations
name: vars-prompt-options-and-limitations
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, prompts-interactive, prompt-default, prompt-limitations, vars-prompt]
level: practitioner
status: docs-checked
description: "Use vars_prompt options (default, private, confirm, encrypt, salt_size, unsafe) and know where prompts do not work: roles, includes, non-interactive runs and controller."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_prompts.html", "https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vars_prompt options and limitations

```yaml
- hosts: db
  vars_prompt:
    - name: target_version
      prompt: PostgreSQL version to install
      default: "16"
      private: false
    - name: admin_password
      prompt: New admin password
      private: true            # default: input hidden
      confirm: true            # ask twice, must match
      encrypt: sha512_crypt    # store a crypt hash instead of plaintext
      salt_size: 16            # default salt size is 8
    - name: banner_text
      prompt: Login banner
      unsafe: true             # accept special characters such as { and % without templating errors
      private: false
```

## Behaviour
- A prompt is skipped for any variable already defined with `--extra-vars`, and in non-interactive sessions (such as cron or AWX) — the CI-friendly path: `ansible-playbook db.yml -e target_version=16 -e @secrets.yml`.
- `default` is the value used when the user presses Enter.
- Precedence: `vars_prompt` values sit at level 13 in the documented order, above play vars and below `vars_files`; extra vars always win.
- `encrypt` accepts the schemes of Passlib if installed; without Passlib the `crypt` fallback supports at most `bcrypt`, `md5_crypt`, `sha256_crypt` and `sha512_crypt`, depending on the platform. Only `salt` or `salt_size` may be given as parameters.

## Where prompts do not work
- **Roles, blocks and task files**: `vars_prompt` is a play keyword only.
- **Non-interactive sessions** (cron, AWX): prompts are skipped; pass the values as extra vars, or use surveys in automation controller.

## Gotchas
- `encrypt` hashes are for uses such as the `user` module's password; do not use them where the plaintext is needed.
- Hiding input (`private`, the default) only affects the prompt; keep `no_log: true` on tasks that use prompted secrets (the devel documentation says ansible-core 2.22 also masks private prompt values in output).

## Verify
```bash
ansible-playbook db.yml -e target_version=16 -e admin_password=x --check    # both prompts skipped because both variables are defined
```

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Interactive input: prompts (playbooks_prompts.rst) and Variables page (precedence list), devel; play.py.
Confirmed:
- private, default, confirm, encrypt, salt_size (default 8), unsafe; prompts skipped for variables defined with --extra-vars and in non-interactive sessions; encrypt schemes with and without Passlib.
- vars_prompt is level 13 in the precedence list, above play vars and below vars_files; it is a play-level keyword.
- Removed the navigator, pause and imported-playbook claims.

Method: documentation only; no commands were run.
