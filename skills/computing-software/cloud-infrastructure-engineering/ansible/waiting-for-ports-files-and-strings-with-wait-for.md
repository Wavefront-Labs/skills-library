---
id: computing-software.cloud-infrastructure-engineering.ansible.waiting-for-ports-files-and-strings-with-wait-for
name: waiting-for-ports-files-and-strings-with-wait-for
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, async-polling, wait-for-module, wait-for, readiness]
level: practitioner
status: docs-checked
description: "Wait for ports to open or drain, files to appear or disappear, and log strings with ansible.builtin.wait_for, including delegated checks and timeouts."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_connection_module.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/modules/wait_for.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# wait_for: ports, files and strings

## Port open (service ready)
```yaml
- name: Wait for PostgreSQL to listen
  ansible.builtin.wait_for:
    host: 127.0.0.1
    port: 5432
    state: started          # default
    timeout: 120
```

## Port check from outside (delegated)
```yaml
- name: App reachable from the load balancer
  ansible.builtin.wait_for:
    host: "{{ ansible_host }}"
    port: 443
    timeout: 300
  delegate_to: "{{ groups['lb'] | first }}"
```

## Connections drained
```yaml
- ansible.builtin.wait_for:
    port: 8080
    state: drained                    # no active connections
    exclude_hosts: [10.0.0.5]         # ignore health-check source
    timeout: 600
```

## Files and log lines
```yaml
- ansible.builtin.wait_for:
    path: /var/lib/app/ready
    state: present
- ansible.builtin.wait_for:
    path: /var/log/app/startup.log
    search_regex: 'Started Application in [0-9.]+ seconds'
    timeout: 180
- ansible.builtin.wait_for:
    path: /var/run/app.lock
    state: absent
```

## Options
| Option | Use |
|---|---|
| `delay` | seconds to wait before polling starts (default 0) |
| `timeout` | maximum wait in seconds (default 300) |
| `sleep` | seconds between checks (default 1) |
| `connect_timeout` | seconds to wait for a connection before closing and retrying (default 5) |
| `msg` | custom failure message |
| `active_connection_states` | which TCP states count for drained |

## wait_for vs others
- Host back after reboot → `wait_for_connection` (tests full Ansible connection) or the `reboot` module.
- HTTP readiness (status code, body) → `uri` with `until`.

## Gotchas
- `state: started` only proves a TCP listener, not app health.
- The module supports POSIX targets only and has no check mode or diff mode support (module attributes).
- Running wait_for on the target against `localhost` does not prove the firewall is open; delegate from a client.

## Verify
- [ ] Task returns `elapsed` well below `timeout` on a healthy host.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in modules/wait_for.py (stable-2.22): host default 127.0.0.1, timeout default 300, connect_timeout default 5, delay default 0, sleep default 1, state choices absent/drained/present/started/stopped, path and port mutually exclusive, search_regex, exclude_hosts (list), active_connection_states, msg, return value elapsed; platform posix, check_mode and diff_mode support none.
- Confirmed in modules/wait_for_connection.py: defaults connect_timeout 5, delay 0, sleep 1, timeout 600, and that it needs no Python on the remote.

Method: documentation only; no commands were run.
