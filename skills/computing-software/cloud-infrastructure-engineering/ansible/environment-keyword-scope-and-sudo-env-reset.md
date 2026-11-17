---
id: computing-software.cloud-infrastructure-engineering.ansible.environment-keyword-scope-and-sudo-env-reset
name: environment-keyword-scope-and-sudo-env-reset
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, module-defaults, play-environment, env-reset, environment-keyword, become]
level: practitioner
status: docs-checked
description: "Set environment variables at play, block, role or task level, understand inheritance and merging, and why sudo env_reset or secure_path can hide them under become."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_environment.html", "https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# environment: scope and become

```yaml
- hosts: app
  environment:                         # play level: every task
    http_proxy: http://proxy.corp:3128
    https_proxy: http://proxy.corp:3128
    no_proxy: localhost,127.0.0.1,.corp
  tasks:
    - name: Build with extra PATH
      ansible.builtin.command: make release
      args: {chdir: /opt/src}
      environment:                     # task level: merged over play values
        PATH: "/opt/go/bin:{{ ansible_env.PATH }}"
        GOFLAGS: -mod=vendor
```

## Inheritance
- Play → role → block → task; the `environment` lists of parent and child are combined into one dictionary and inner keys win.
- Values are set only for the module process of tasks run by the same user; they do not persist on the host and do not become Ansible facts. To populate `ansible_env`, put `environment` on an explicit `gather_facts` task.
- `ansible_env` is captured at fact gathering, so it reflects the `remote_user` or `become_user` used then; basing values on it (for example extending PATH) is risky if that user changes.

## become
The keyword is applied to the module process on the target. Check the effect under your become method with the verify task below rather than assuming it survives sudo or su settings (`env_reset`, `secure_path`) on the target (not confirmed by the Ansible docs). Services started by a module do not inherit the task environment; configure them in the service itself.

## Persistent environment
For daemons and cron, configure the environment in the service or job definition (for example a systemd unit `Environment=` setting) instead of the keyword.

## Gotchas
- `environment` does not affect Ansible itself, its configuration settings, other users' environments, or plugins such as lookups and filters, and it only applies to modules.
- Environment variables are normally passed in clear text (shell plugin dependent), so the docs advise against using them to pass secrets.

## Verify
```yaml
- ansible.builtin.command: env
  register: e
  changed_when: false
- ansible.builtin.assert: {that: "'http_proxy=http://proxy.corp:3128' in e.stdout_lines"}
```

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_environment.rst and ansible-core devel `playbook/base.py` (`environment` is an extending, prepending list) and `playbook/task.py` (list merged into one dictionary). Confirmed: scope and inheritance, no facts from environment, `ansible_env` caveat, clear-text warning, limits (modules only). Removed unconfirmed claims about sudo `env_reset`/`secure_path`, `su` login resets, persistent-environment file paths and `-vvv` output.
Method: documentation only; no commands were run.
