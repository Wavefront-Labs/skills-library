---
id: computing-software.devops-ci-cd.semaphore-ui.ansible-prompts
name: ansible-prompts
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [prompts, limit, tags, skip-tags, ansible-playbook, semaphore-ui]
level: practitioner
status: docs-checked
description: "Enable per-run Ansible prompts for limit, tags, skip tags and verbosity so users and API calls can override them."
sources:
  - https://semaphoreui.com/docs/user-guide/task-templates/prompts
  - https://semaphoreui.com/docs/user-guide/tasks
  - https://semaphoreui.com/docs/user-guide/apps/ansible
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Template prompts for Ansible

Goal: let runs customise Ansible CLI flags without editing the template.

Prompts are predefined options enabled by checkboxes in the template. When enabled they appear in the New Task dialog and accept values from API calls and schedules.

- Limit: `--limit`. Run on a subset, e.g. `web-01.example.com` or `webservers:&production`.
- Tags: `--tags deploy,restart` runs only matching tagged tasks.
- Skip Tags: `--skip-tags testing,debug` omits them.
- Debug/verbosity and Dry Run (`--check`) and Diff (`--diff`) are offered as task-time toggles for Ansible templates.

Example playbook tags:

```yaml
- hosts: all
  tasks:
    - name: Install packages
      apt: { name: nginx }
      tags: install
    - name: Deploy application
      copy: { src: app.tar.gz, dest: /opt/app/ }
      tags: deploy
```

With Tags enabled, running with `deploy,restart` skips installation.

Critical gotcha: when launching through the API with a limit, the matching prompt (Ansible prompts: Limit) must be enabled in the template. Otherwise the value in the API call is ignored. The same applies to tags.

Template-level defaults for tags, skip-tags and limit can be set and are overridden at task creation when the prompt is on.

Verify: run with a limit and check that the `PLAY RECAP` lists only the targeted hosts.

## Checked

2026-11-04: checked against the prompts, tasks and Ansible app pages. Every remaining claim is stated on those pages.

Method: documentation only; no commands were run.
