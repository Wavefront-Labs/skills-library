---
id: computing-software.systems-network-administration.linux.selinux-port-labels
name: selinux-port-labels
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, selinux, semanage-port, port-labeling, port-type, http-port-t, ssh-port-t, name-bind, avc-denial, rhcsa, security, sysadmin]
level: practitioner
status: docs-checked
description: "Let confined services bind or connect to non-standard ports with semanage port: finding the right port type, add/modify/delete, ranges, reading name_bind/name_connect denials, and verifying."
sources:
  - https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-port.8
  - https://github.com/SELinuxProject/selinux/blob/main/python/semanage/seobject.py
  - https://github.com/SELinuxProject/selinux/blob/main/python/sepolicy/sepolicy-network.8
  - https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-export.8
  - https://github.com/ansible-collections/community.general/blob/main/plugins/modules/seport.py
  - https://github.com/firewalld/firewalld/blob/main/doc/xml/firewall-cmd.xml.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELinux port labels with semanage port

**Goal:** run sshd on 2222, httpd on 8443 or a database on a custom port without
disabling SELinux — label the port, not the process.

## 1. Symptom
Service fails to start (or can't connect out) after a port change; journal/audit shows:
```
avc: denied { name_bind } for comm="sshd" src=2222 scontext=system_u:system_r:sshd_t:s0 tcontext=system_u:object_r:unreserved_port_t:s0 tclass=tcp_socket
```
`name_bind` = listening, `name_connect` = outgoing connection. `tcontext` shows the port's current type.
```bash
ausearch -m AVC -ts recent | grep name_
```

## 2. Find the right type
```bash
semanage port -l | grep -w http_port_t       # ports currently labelled http_port_t
semanage port -l | grep -E '^ssh_port_t'
sepolicy network -d sshd_t                   # ports the domain may connect to or bind
sepolicy network -p 2222                     # SELinux port types associated with this port number
```
Pick the type the service's domain is allowed to bind (`http_port_t` for httpd/nginx, `ssh_port_t`
for sshd, `postgresql_port_t`, `mysqld_port_t`, `syslogd_port_t`, ...).

## 3. Change
```bash
semanage port -a -t ssh_port_t -p tcp 2222          # add
semanage port -a -t http_port_t -p tcp 8100-8110    # range
semanage port -m -t http_port_t -p tcp 9090         # already defined with another type → modify
semanage port -d -t ssh_port_t -p tcp 2222          # delete a local customisation
semanage port -l -C                                  # list local customisations only
```
`-a` on a port that already has a definition prints "already defined, modifying instead" and modifies it, so `-m` is the explicit form.
Changes are written to the policy store and the policy is reloaded unless `-N` is given; restart the service.

## 4. Full sequence for sshd on 2222
```bash
semanage port -a -t ssh_port_t -p tcp 2222
sed -i 's/^#\?Port .*/Port 2222/' /etc/ssh/sshd_config
firewall-cmd --permanent --add-port=2222/tcp && firewall-cmd --reload
systemctl restart sshd && ss -ltnp | grep 2222
```
Keep the old port open until you've logged in on the new one.

## Gotchas
- A port number has one type at a time, so relabelling it affects every domain that relied on the old type.
- Ports defined in the base policy cannot be deleted, only modified.
- Outbound denials (`name_connect`) for web apps can also be governed by a boolean such as `httpd_can_network_connect`; check both the port type and the booleans.
- Ansible: `community.general.seport` module; export customisations with `semanage export -f`.

## Verify
- [ ] `semanage port -l | grep <port>` shows the intended type; service listening (`ss -ltnp`).
- [ ] `ausearch -m AVC -ts recent` shows no new `name_bind` denials after restart, with SELinux enforcing.

## Checked
Checked 2026-10-26 against the SELinuxProject/selinux man pages (semanage-port, semanage-export, sepolicy-network), the semanage source seobject.py, the community.general seport module source and the firewall-cmd manual source.
Confirmed: `semanage port -a/-m/-d/-l/-C -t TYPE -p PROTO`, the `-N` no-reload option, the man-page examples for http_port_t and ssh_port_t; `sepolicy network -d/-p/-t` meanings (the earlier text used -t for a domain, which is wrong: -t takes a port type); adding an existing port prints "already defined, modifying instead"; ports defined in policy cannot be deleted; `semanage export -f`; the `community.general.seport` module; firewall-cmd `--permanent`, `--add-port` and `--reload`.
Removed as unconfirmed: the list of ports under http_port_t, the squid example.
Method: documentation only; no commands were run.
