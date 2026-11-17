---
id: computing-software.cloud-infrastructure-engineering.ansible.load-balancer-pattern-delegating-in-a-rolling-play
name: load-balancer-pattern-delegating-in-a-rolling-play
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, delegation, delegate-loop, loadbalancer-pattern, rolling-update, serial, haproxy]
level: advanced
status: docs-checked
description: "Do the classic rolling update: per batch, disable each host in every load balancer via delegate_to loop, update, health-check, then re-enable, with failure limits."
sources: ["Controlling where tasks run: delegation (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html)", "Controlling playbook execution: strategies and serial (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html)", "Error handling, max_fail_percentage and force_handlers (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html)", "community.general.haproxy module source (https://github.com/ansible-collections/community.general/blob/main/plugins/modules/haproxy.py)", "Playbook keywords source, order and max_fail_percentage (https://github.com/ansible/ansible/blob/devel/lib/ansible/keyword_desc.yml)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load balancer pattern: delegating in a rolling play

```yaml
- name: Rolling update of web tier
  hosts: web
  serial: [1, "25%"]
  max_fail_percentage: 0
  order: sorted
  become: true

  pre_tasks:
    - name: Disable host in every load balancer
      community.general.haproxy:
        state: disabled
        host: "{{ inventory_hostname }}"
        backend: app
        wait: true
        drain: true
      delegate_to: "{{ item }}"
      loop: "{{ groups['lb'] }}"

  roles:
    - app

  post_tasks:
    - name: Wait for the app to be healthy
      ansible.builtin.uri:
        url: "http://{{ hostvars[inventory_hostname]['ansible_host'] | default(inventory_hostname) }}:8080/health"
        status_code: 200
      register: hc
      until: hc.status == 200
      retries: 30
      delay: 5
      delegate_to: "{{ groups['lb'][0] }}"   # check from the LB's network position

    - name: Re-enable host in every load balancer
      community.general.haproxy:
        state: enabled
        host: "{{ inventory_hostname }}"
        backend: app
        wait: true
      delegate_to: "{{ item }}"
      loop: "{{ groups['lb'] }}"
```

## Why each piece
- `serial: [1, "25%"]` — canary of one host, then quarter batches.
- `max_fail_percentage: 0` — the play aborts when more than 0% of a batch fails, i.e. at the first failure (the setting applies per batch and only on linear strategies); the failed host stays drained, which is the safe state.
- `delegate_to` + `loop` over `groups['lb']` — every LB is told, not just the first.
- `drain: true` + `wait: true` — per the haproxy module docs, `drain` waits until the server has no active connections (or the `wait_interval` x `wait_retries` timeout) and continues once the status is `MAINT`; `wait` waits for the status to match the requested state. The socket path defaults to `/var/run/haproxy.sock`; set `socket:` if yours differs.
- Health check delegated to the LB: under delegation `ansible_host` and the other connection variables describe the **delegated** host, so the web host's own address is read through `hostvars[inventory_hostname]`.
- Health check before re-enable; nothing goes back into rotation unhealthy.

## Other load balancers
The structure is the same with the module for your platform that can disable and enable a pool member: delegate to the host that can reach the load balancer (often `localhost` for API-based modules) and check that module's documentation for its drain or wait options.

## Gotchas
- Do not re-enable in a handler: when a later task fails on a host, notified handlers do not run on that host unless `force_handlers` is set; use post_tasks.
- If the LB is reached via API from localhost, delegate to localhost and set `become: false` on that task (under delegation the become options come from the delegated host).
- Monitoring must tolerate drained hosts; silence alerts for the batch or rely on LB health checks.
- `serial` percentages are applied to the total number of hosts in the play, and no matter how small the percentage the batch size is always at least 1.

## Verify
- [ ] During a run, the LB stats page shows exactly one batch in MAINT/DRAIN at a time.
- [ ] After the run, every web host is enabled again in every load balancer.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21), ansible-core 2.21.5 and community.general main.
- Confirmed in the haproxy module: options `backend`, `drain`, `host`, `socket` (default `/var/run/haproxy.sock`), `state` (`disabled`, `drain`, `enabled`), `wait`, `wait_interval`, `wait_retries`, and the drain and wait semantics quoted above.
- Confirmed: `serial` list of mixed counts and percentages, always at least one host per batch; `max_fail_percentage` applies per batch, aborts when more than the percentage fails and works on linear strategies; `order: sorted`; handlers do not run on a host after a later failure unless forced; connection variables such as `ansible_host` refer to the delegated host.
- Fixed: the health-check task used `{{ ansible_host }}` under `delegate_to`, which resolves to the delegated load balancer; and `community.general.nginx_status_info` is an information module, not a way to disable a member (the vendor-module suggestions were removed as unconfirmed).
- Removed as unconfirmed: the socat command and the example socket path.

Method: documentation only; no commands were run.
