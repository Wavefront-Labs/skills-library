---
id: computing-software.devops-ci-cd.deployment-strategies.ansible-deploy-playbooks
name: ansible-deploy-playbooks
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, ansible-deploy, deployment-automation, idempotent-deploy]
level: practitioner
status: docs-checked
description: "Deploy applications to VM fleets with Ansible playbooks: idempotent tasks, serial batches, handlers for restarts, health checks, check mode and running from CI."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ansible deploy playbooks

```yaml
- name: Deploy api
  hosts: api
  serial: "25%"                 # batches; see rolling updates
  max_fail_percentage: 0
  vars: { version: "{{ app_version }}" }
  pre_tasks:
    - name: Drain from load balancer
      ansible.builtin.uri: { url: "http://{{ lb }}/drain/{{ inventory_hostname }}", method: POST }
      delegate_to: localhost
  tasks:
    - name: Fetch artifact
      ansible.builtin.get_url:
        url: "https://artifacts.example.com/api/{{ version }}/api.tar.gz"
        dest: "/opt/api/releases/{{ version }}.tar.gz"
        checksum: "sha256:{{ artifact_sha256 }}"
    - name: Unpack
      ansible.builtin.unarchive:
        src: "/opt/api/releases/{{ version }}.tar.gz"
        dest: "/opt/api/releases/{{ version }}"
        remote_src: true
        creates: "/opt/api/releases/{{ version }}/bin/api"
    - name: Point current symlink
      ansible.builtin.file: { src: "/opt/api/releases/{{ version }}", dest: /opt/api/current, state: link }
      notify: restart api
  handlers:
    - name: restart api
      ansible.builtin.systemd: { name: api, state: restarted }
  post_tasks:
    - ansible.builtin.meta: flush_handlers
    - name: Health check
      ansible.builtin.uri: { url: "http://{{ inventory_hostname }}:8080/healthz", status_code: 200 }
      register: h
      retries: 20
      delay: 3
      until: h.status == 200
    - name: Re-enable in load balancer
      ansible.builtin.uri: { url: "http://{{ lb }}/enable/{{ inventory_hostname }}", method: POST }
      delegate_to: localhost
```

## Practices
- Modules over `shell:`; when `shell` is unavoidable, add `creates:`/`changed_when:` for idempotency.
- Run check mode in CI for PRs touching playbooks and lint them.
- Pin collection versions.
- Run from CI with an SSH key from the secret store and host keys verified.

## Verify
- [ ] Second run reports `changed=0`; one bad host stops the play before the next batch.

## Checked

2026-10-28. Confirmed against the Ansible docs: `serial` batches by number or percentage and `max_fail_percentage` (playbook strategies page), `delegate_to`, `meta: flush_handlers`, `get_url` `checksum` in `sha256:<digest>` form, `unarchive` `remote_src` and `creates`, the `uri` module, `systemd_service` `state: restarted`, and `until` retry loops. Removed: `ansible-lint`, `--check --diff` flags, `requirements.yml` and `ANSIBLE_HOST_KEY_CHECKING` specifics.

Method: documentation only; no commands were run.
