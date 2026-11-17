---
id: computing-software.devops-ci-cd.deployment-strategies.vm-fleet-rolling-updates-with-ansible-serial
name: vm-fleet-rolling-updates-with-ansible-serial
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, ansible-serial, rolling-updates, max-fail-percentage, load-balancer-drain, delegate-to, throttle]
level: practitioner
status: draft
description: "Roll updates across VM fleets with Ansible serial batches: draining from load balancers, health gates, max_fail_percentage, run_once and delegate_to, and resuming failed runs."
sources:
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html#setting-the-batch-size-with-serial
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html#setting-a-maximum-failure-percentage
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# VM fleet rolling with Ansible serial

## Batches
```yaml
- hosts: web
  serial: [1, "10%", "25%"]       # canary 1 host, then 10% batches, then 25%
  max_fail_percentage: 0          # any failure in a batch stops the play
  any_errors_fatal: false
  pre_tasks:
    - name: Drain from load balancer
      community.general.haproxy: { state: disabled, host: "{{ inventory_hostname }}", backend: web, socket: /run/haproxy/admin.sock, wait: true, drain: true }
      delegate_to: "{{ item }}"
      loop: "{{ groups['lb'] }}"
  roles:
    - app_deploy
  post_tasks:
    - name: Wait for health
      ansible.builtin.uri: { url: "http://{{ inventory_hostname }}:8080/health", status_code: 200 }
      register: h
      until: h.status == 200
      retries: 20
      delay: 5
    - name: Re-enable in load balancer
      community.general.haproxy: { state: enabled, host: "{{ inventory_hostname }}", backend: web, socket: /run/haproxy/admin.sock }
      delegate_to: "{{ item }}"
      loop: "{{ groups['lb'] }}"
```
- `serial` makes the whole play (all tasks, including handlers at the end of each batch) run batch by batch.
- `max_fail_percentage` is checked per batch; with `serial: 1` a single failure exceeds 0%. Hosts already finished stay updated: plan for mixed versions.
- Cloud LBs: `amazon.aws.elb_target` (deregister/register with `target_status_timeout`), `azure.azcollection` backend pool membership, F5 `bigip_pool_member`.

## Related keywords
- `throttle: 2` on a task limits concurrency for that task only (e.g. DB migration tool, license server calls).
- `run_once: true` with `delegate_to` for steps that should happen once per play (migrations) - but with `serial` it runs once **per batch**; guard with a condition or put it in a separate play before the rolling play.
- `order: sorted|shuffle|inventory` controls host ordering.
- `strategy: free` is incompatible with careful rolling; keep `linear`.

## Resuming after a failure
```bash
ansible-playbook deploy.yml --limit @deploy.retry          # if retry_files_enabled
ansible-playbook deploy.yml --limit 'web:!web[0:9]'         # skip done hosts
ansible-playbook deploy.yml --start-at-task "Re-enable in load balancer" --limit web07
```
Make roles idempotent so re-running on already-updated hosts is a no-op.

## Health gate realism
A 200 from `/health` isn't enough for some apps; also check error rate from monitoring (`uri` against Prometheus API) before moving to the next batch, and add `pause: { minutes: 5 }` after the canary batch for soak.

## Verify
- [ ] With a deliberately broken build, the play stops after the first host and that host is still out of the LB.
- [ ] During a normal run, capacity never drops below N - batch size; LB shows hosts draining and returning.
