---
id: computing-software.systems-network-administration.patch-management.ansible-rolling-patch-playbooks
name: ansible-rolling-patch-playbooks
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-deployment, patch-orchestration, ansible-patching, serial-batches, max-fail-percentage, rolling-patching, ansible, linux-patching]
level: practitioner
status: docs-checked
description: "Patch Linux fleets with Ansible: serial batches, max_fail_percentage, drain/patch/reboot/verify per host, reboot-only-if-needed, and safe handling of clustered services."
sources:
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/reboot_module.html
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/dnf_module.html
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/apt_module.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/needs_restarting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling patch playbooks with Ansible

**Goal:** patch a group of servers in controlled batches, stop automatically when things
go wrong, and leave every host verified.

## Playbook skeleton
```yaml
- hosts: web
  serial: ["1", "20%", "50%"]        # canary host, then bigger batches
  max_fail_percentage: 0             # any failure in a batch stops the run
  become: true
  pre_tasks:
    - name: Drain from load balancer
      ansible.builtin.uri:
        url: "https://lb.<domain>/api/pools/web/members/{{ inventory_hostname }}/disable"
        method: POST
        headers: { Authorization: "Bearer {{ lb_token }}" }
      delegate_to: localhost
  tasks:
    - name: Apply updates (RHEL family)
      ansible.builtin.dnf: { name: "*", state: latest, security: "{{ security_only | default(false) }}" }
      when: ansible_os_family == "RedHat"
    - name: Apply updates (Debian family)
      ansible.builtin.apt: { upgrade: dist, update_cache: true }
      when: ansible_os_family == "Debian"
    - name: Reboot needed? (RHEL)
      ansible.builtin.command: dnf needs-restarting -r
      register: nr
      changed_when: false
      failed_when: nr.rc not in [0, 1]
      when: ansible_os_family == "RedHat"
    - name: Reboot needed? (Debian)
      ansible.builtin.stat: { path: /var/run/reboot-required }
      register: rr
      when: ansible_os_family == "Debian"
    - name: Reboot
      ansible.builtin.reboot: { reboot_timeout: 900 }
      when: (nr.rc | default(0)) == 1 or (rr.stat.exists | default(false))
  post_tasks:
    - name: Health check
      ansible.builtin.uri: { url: "http://{{ inventory_hostname }}/healthz", status_code: 200 }
      retries: 10
      delay: 6
      register: hc
      until: hc.status == 200
    - name: Re-enable in load balancer
      ansible.builtin.uri:
        url: "https://lb.<domain>/api/pools/web/members/{{ inventory_hostname }}/enable"
        method: POST
        headers: { Authorization: "Bearer {{ lb_token }}" }
      delegate_to: localhost
```

## Practices
- Run `--check --diff` first and `--limit` to a single host for new playbooks.
- Pin packages that must not move (`exclude:` in dnf, `apt-mark hold`) in the playbook,
  not by hand.
- Clusters (DB, Elasticsearch, Kubernetes nodes): use the product's maintenance steps
  in `pre_tasks` (e.g. disable shard allocation, drain node) and `serial: 1`.
- Log output to a file/AWX job history as patch evidence.

## Gotchas
- `serial` with a failing canary stops the play; that is the point. Do not raise
  `max_fail_percentage` to get past it.
- `apt upgrade: dist` may remove packages; review the diff on the canary.

## Verify
Job summary: all hosts `ok`/`changed`, none failed or unreachable; post-run package
report shows the target versions; health checks green.

## Checked
Date: 2026-10-27. Documentation checked: Ansible playbook strategies page (`serial` as number, percentage or list; `max_fail_percentage` limits failure per batch), `ansible.builtin.dnf` (`security`, `exclude`), `ansible.builtin.apt` (`upgrade: dist` runs apt-get dist-upgrade, `update_cache`), `ansible.builtin.reboot` (`reboot_timeout`), dnf-plugins-core needs-restarting page (`-r` exits 1 when a reboot is required, 0 when not), Ubuntu server documentation (`/var/run/reboot-required`). The reboot check now calls `dnf needs-restarting -r`, the documented form.

Method: documentation only; no commands were run.
