---
id: computing-software.cloud-infrastructure-engineering.ansible.become-and-variables-on-delegated-hosts
name: become-and-variables-on-delegated-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, delegation, delegated-become, delegate-vars, delegate-to, connection-variables]
level: advanced
status: docs-checked
description: "Know which connection, become and inventory variables apply when a task is delegated, and set them correctly for the delegate (including localhost and jump hosts)."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html#templating-in-delegation-context"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Become and variables on the delegated host

When a task for `web1` is `delegate_to: lb1`, the docs say:
- `ansible_host` and other connection variables reflect the host the task is delegated to, not `inventory_hostname`.
- The execution interpreter (normally Python), `connection`, `become` and `shell` plugin options are
  templated using values from the delegated-to host. All variables except `inventory_hostname` are
  then taken from that host, not the original task host. If you need a variable from the original
  host, reference it explicitly through `hostvars['web1']` (the docs name this approach for the original host).
- The delegated-to host does not inherit variables from the host that is delegating the task.
- Facts gathered by a delegated task are assigned to the original host unless `delegate_facts: true`.
- Some tasks (`include`, `add_host`, `debug`) always run on the control node and cannot be delegated.

Use `{{ hostvars['lb1'].lb_backend_name }}` for delegate-specific data.

## Become on the delegate
```yaml
- name: Drain backend on load balancer
  community.general.haproxy:
    state: disabled
    host: "{{ inventory_hostname }}"
    backend: app
  delegate_to: "{{ item }}"
  loop: "{{ groups['lb'] }}"
  become: true                            # become keyword on the task
```
`become` is a task keyword, so it applies on the delegate; become plugin options (such as
`ansible_become_password`) are templated from the delegate's variables, so a different password
for the lb hosts belongs in their `host_vars`.

## Delegating to localhost
```yaml
- name: Call cloud API from the controller
  amazon.aws.ec2_instance_info:
    instance_ids: ["{{ instance_id }}"]
  delegate_to: localhost
  become: false
```
With `become: true` on the play, a task delegated to localhost would also try to escalate; set
`become: false` there. The docs note that a play with `connection: local` and no
`ansible_python_interpreter` runs modules under `/usr/bin/python`, not `{{ ansible_playbook_python }}`;
using `local_action` or `delegate_to: localhost` instead avoids that issue.

## Gotchas
- Delegating to a host not in inventory (an IP or DNS name) works but does not add it to the inventory
  and might cause issues; such hosts inherit variables only from the `all` group.
- `local_action:` is the documented shorthand for delegating to 127.0.0.1.

## Verify
- [ ] `-vvv` output shows the connection to the delegate's address with the expected user.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_delegation.rst, "Templating in delegation
context" and delegation notes). Confirmed the statements above. Removed unconfirmed claims about
`ansible_delegated_vars` and `ansible_delegated_host` (not in the documentation), `remote_user` handling on delegates and a
variable-source table not stated in the docs.
Method: documentation only; no commands were run.
