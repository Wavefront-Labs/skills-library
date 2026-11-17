---
id: computing-software.cloud-infrastructure-engineering.ansible.idempotent-playbooks-and-roles
name: idempotent-playbooks-and-roles
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-playbook, roles, collections, idempotency, changed-when, failed-when, check-mode, diff-mode, handlers, ansible-lint, molecule, ansible-vault, inventory, group-vars, variable-precedence, fqcn, ansible-galaxy, become, serial, max-fail-percentage, configuration-management, ansible-navigator, execution-environments]
level: practitioner
status: docs-checked
description: "Write Ansible that converges and reports truthfully: idempotent modules over shell, changed_when, handlers, role layout, variable precedence, vault, and check/diff runs."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotent Ansible playbooks and roles — second run reports zero changes

**Goal:** playbooks you can run any number of times, where `changed` means something
actually changed, check mode tells the truth, and roles are reusable and tested.

## 1. Prefer modules; tame commands
- Use the declarative module (`ansible.builtin.package`, `template`, `lineinfile`,
  `systemd_service`, `user`, `community.general.*`). Use FQCNs everywhere.
- When you must use `command`/`shell`:
  ```yaml
  - name: Read current schema version
    ansible.builtin.command: /usr/local/bin/app schema-version
    register: schema
    changed_when: false
    check_mode: false          # run even in --check, it's read-only
  - name: Migrate
    ansible.builtin.command: /usr/local/bin/app migrate
    register: mig
    changed_when: "'Applied' in mig.stdout"
    failed_when: mig.rc not in [0, 3]
  ```

## 2. Handlers for restarts
- Notify a handler on config change instead of restarting unconditionally:
  `notify: Restart nginx`. `meta: flush_handlers` triggers handlers notified so far in the play.
- Validate before replacing with the `validate:` parameter of `template`/`copy`
  (for example `validate: 'nginx -t -c %s'`).
- Use `listen:` topics so several handlers can react to one event.

## 3. Role layout
```
roles/nginx/
  defaults/main.yml   # user-overridable, lowest precedence
  vars/main.yml       # internal constants, high precedence — rarely what you want
  tasks/main.yml
  handlers/main.yml
  templates/  files/
  meta/main.yml       # dependencies, platforms
  meta/argument_specs.yml   # typed, validated role inputs
```
- Prefix role variables with the role name (`nginx_worker_processes`) to avoid collisions.
- Role argument specifications live in `meta/argument_specs.yml` under a top-level
  `argument_specs` block.

## 4. Variables and secrets
- Precedence: more recently defined, more active, more explicit-scope variables win. Role
  defaults are easily overridden; host or inventory variables override role defaults;
  a role's `vars` directory or `include_vars` overrides inventory variables; registered
  vars and `set_fact` rank high; extra vars (`-e`) have global scope for the run.
- Put environment data in inventory (`inventories/prod/group_vars/web.yml`), not in roles.
- Secrets: `ansible-vault encrypt_string` for single values or vault-encrypted files;
  select a vault id with `--vault-id <label>@<source>`.

## 5. Running safely
- Dry run: `ansible-playbook site.yml -i inventories/prod --check --diff --limit web01`.
- Rolling changes: `serial` (a number, percentage or list) batches hosts and scopes failures
  to the batch; `max_fail_percentage` modifies that behaviour.

## Gotchas
- `command` tasks report `changed` every run by default; use `creates`, `changed_when` or `failed_when`.
- Tasks that do not run in check mode leave registered variables without output; set
  `check_mode: false` on read-only tasks that later tasks depend on.
- `vars/main.yml` in a role overrides inventory variables, so users cannot change those
  values without `-e`; role defaults are easily overridden.
- Becoming an unprivileged user needs `setfacl` (POSIX ACLs) on the target or pipelining
  to protect temporary files; see the privilege escalation docs.

## Verify
- [ ] Running the playbook twice in a row: second run shows `changed=0` on every host.
- [ ] `--check --diff` completes without errors and shows the intended changes only.
- [ ] No plaintext secrets in the repo; secrets are vaulted.
- [ ] Config templates use `validate:` where the service offers a syntax check.

## Checked
2026-11-09. Confirmed in the Ansible playbook guide (handlers, variables and precedence, roles argument specs, check mode, error handling, strategies, privilege escalation, vault): notify/listen/flush_handlers, check_mode: false, changed_when and failed_when, serial and max_fail_percentage, meta/argument_specs.yml, encrypt_string and --vault-id, setfacl for unprivileged become, the precedence notes. Removed as unchecked: the creates example, the | quote advice, ansible-lint enforcement and profile, Molecule, ansible-navigator execution environments, community.hashi_vault, no_log, the abridged precedence ladder, serial [1, 25%] advice, pipelining/requiretty and ControlPersist tuning, lineinfile and bool-string gotchas, --start-at-task.
Method: documentation only; no commands were run.
