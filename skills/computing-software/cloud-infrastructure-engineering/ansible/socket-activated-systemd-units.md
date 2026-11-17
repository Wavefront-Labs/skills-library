---
id: computing-software.cloud-infrastructure-engineering.ansible.socket-activated-systemd-units
name: socket-activated-systemd-units
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, services-systemd, systemd-socket, systemd-units, unit-files]
level: practitioner
status: docs-checked
description: "Deploy and manage socket-activated systemd units with Ansible: .socket plus .service templates, enabling the socket not the service, and restart semantics."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/systemd_service_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/systemd_service.py", "https://github.com/systemd/systemd/blob/main/man/systemd.socket.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Socket-activated units

systemd listens on the socket and starts the matching service when traffic arrives (systemd.socket).

## Deploy
```yaml
- name: Socket unit
  ansible.builtin.copy:
    dest: /etc/systemd/system/metrics-agent.socket
    content: |
      [Unit]
      Description=Metrics agent socket
      [Socket]
      ListenStream=127.0.0.1:9101
      Accept=no
      [Install]
      WantedBy=sockets.target
    mode: "0644"
  notify: Restart metrics socket

- name: Service unit
  ansible.builtin.template:
    src: metrics-agent.service.j2      # [Service] ExecStart=/usr/local/bin/metrics-agent ; Requires=metrics-agent.socket
    dest: /etc/systemd/system/metrics-agent.service
    mode: "0644"

- name: Enable and start the socket (not the service)
  ansible.builtin.systemd_service:
    name: metrics-agent.socket
    enabled: true
    state: started
    daemon_reload: true
```

## Handlers
```yaml
handlers:
  - name: Restart metrics socket
    ansible.builtin.systemd_service:
      name: metrics-agent.socket
      state: restarted
      daemon_reload: true
```
Restart the `.socket` when its listen settings change; restart the `.service` when only the daemon's own configuration changed.

## Gotchas
- With `Accept=no` a single service instance handles all connections and receives the listening socket; with `Accept=yes` a service template is instantiated per connection (systemd.socket).
- Enable and start the `.socket` unit; the matching service is pulled in by systemd, so enabling the service separately is usually unnecessary.

## Verify
- [ ] `systemctl is-active metrics-agent.socket` reports `active` on the host.

## Checked
Checked 2026-10-26 against systemd `man/systemd.socket.xml` (`ListenStream=`, `Accept=`, `sockets.target`) and ansible-core
`systemd_service.py` (`daemon_reload`, `enabled`, `state`). Removed unconfirmed claims: the Ubuntu `ssh.socket` version and
`Port` behaviour, the Podman and cockpit examples, file-descriptor restart ordering advice, `service_facts` inactive
behaviour, and the `ss` command. The unit example (`Requires=`) was not run.
Method: documentation only; no commands were run.
