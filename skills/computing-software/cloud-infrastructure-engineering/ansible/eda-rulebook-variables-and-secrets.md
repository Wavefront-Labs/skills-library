---
id: computing-software.cloud-infrastructure-engineering.ansible.eda-rulebook-variables-and-secrets
name: eda-rulebook-variables-and-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, event-driven-ansible, eda-vars, eda-secrets, ansible-rulebook, rulebook-activation, eda-credentials, vault, env-vars]
level: advanced
status: docs-checked
description: "Parameterise rulebooks with variables and keep secrets out of them: --vars and --env-vars locally, and EDA controller activation vars and credential injection."
sources: ["https://docs.ansible.com/projects/rulebook/en/latest/variables.html", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_decisions/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EDA rulebook variables and secrets

Goal: one rulebook works across environments (thresholds, hostnames, Kafka topics differ) and
API tokens or webhook secrets are never committed in it.

## Variables in a rulebook
```yaml
- name: Disk alerts
  hosts: all
  sources:
    - ansible.eda.kafka:
        host: "{{ kafka_host }}"
        port: 9093
        topic: "{{ alert_topic }}"
  rules:
    - name: Disk above threshold
      condition: event.body.disk_pct > vars.disk_threshold
      action:
        run_job_template:
          name: Clean disk
          organization: Ops
          job_args: {extra_vars: {mount: "{{ event.body.mount }}"}}
```
- In **source arguments and action args**, use Jinja `{{ var }}`.
- In **conditions**, use `vars.<name>` (conditions are not Jinja).

## Supplying values locally
```bash
ansible-rulebook -r disk.yml -i inventory.yml --vars vars/prod.yml
export KAFKA_PASSWORD=<KAFKA_PASSWORD>
ansible-rulebook -r disk.yml -i inventory.yml --vars vars/prod.yml --env-vars KAFKA_PASSWORD
```
`--env-vars` takes a list of environment variable names parsed into the rulebook as variables
(data types are preserved for `--vars` values, while `--env-var` values arrive as strings).
Use it for secrets in CI or container runs; keep the non-secret values in the `--vars` file.
Otherwise pass secrets via env.

## In the EDA controller (rulebook activations)
- **Variables** field on the activation = the `--vars` file (YAML). Non-secret only.
- **Credentials** on the activation inject secrets: built-in types (e.g. "Basic Event Stream",
  container registry, vault) or **custom credential types** whose injector is
  `extra_vars: {kafka_password: "{{ password }}"}`. Values are encrypted at rest and not shown.
- The AAP credential (controller URL + token) used by `run_job_template` is separate; it needs
  Execute on the target templates.
- Restart the activation after changing variables or credentials; running activations keep old values.

## Passing secrets onward
Don't put secrets into `job_args.extra_vars` from events; the job template should get its own
credentials. Event payloads land in job extra vars and in the activation's audit log — treat
everything in `event` as visible.

## Gotchas
- An undefined `vars.foo` in a condition makes the rule never match (no error); a test event and
  debug-level activation logs help.
- Source plugins read arguments once at start; rotating a token requires an activation restart.
- Activation logs at debug level can print source arguments; keep log level at error/info in production.

## Verify
- [ ] `ansible-rulebook ... --vars vars/stage.yml` connects to stage Kafka; the same rulebook with prod vars connects to prod.
- [ ] `grep -ri password rulebooks/` in the repo finds nothing; the activation shows credentials attached, not literal values.

## Checked

- 2026-10-31: rulebook variable handling (`--vars` and `--env-var` command line arguments,
  preserved vs string data types, accessing variables in conditions via `vars.<name>`), the
  `run_job_template` action and its `extra_vars` parameter confirmed in the ansible-rulebook
  variables documentation. `ansible.eda.kafka`/`ansible.eda.webhook` source plugins, rulebook
  activations, EDA credential types (Rule Engine, external secret management) and troubleshooting
  guidance confirmed in AAP 2.5 Using automation decisions and the documentation set overview.
- Removed: the `--print-events` flag, the `--vault-id`/`--vault-password-file` support claim and
  the custom-credential injector example specifics (not in the fetched documentation; the generic
  credential-injection mechanism on activations is kept).
Method: documentation only; no commands were run.
