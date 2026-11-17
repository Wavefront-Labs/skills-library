---
id: computing-software.cloud-infrastructure-engineering.ansible.rhel-system-roles-vpn-ipsec-tunnels
name: rhel-system-roles-vpn-ipsec-tunnels
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, rhel-system-roles, vpn-role, vpn, ipsec, libreswan, host-to-host, mesh-vpn, opportunistic-ipsec, linux-system-roles]
level: advanced
status: docs-checked
description: "Build host-to-host and mesh IPsec tunnels with the RHEL vpn system role (Libreswan): PSK vs certificate auth, tunnel definitions, mesh policies, firewall and verification."
sources:
  - https://raw.githubusercontent.com/linux-system-roles/vpn/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RHEL system roles: vpn (Libreswan IPsec)

Goal: encrypted host-to-host or full-mesh traffic between RHEL hosts, defined in inventory and
applied by the `vpn` role instead of hand-written Libreswan config files.

## Host-to-host with generated PSKs
```yaml
- hosts: db_pair
  become: true
  vars:
    vpn_connections:
      - hosts:
          db1.example.com:
          db2.example.com:
        auth_method: psk          # role generates a PSK with openssl on the controller
        auto: start               # start at IPsec startup
    vpn_manage_firewall: true     # opens 500/udp, 4500/udp and 4500/tcp via the firewall role
    vpn_manage_selinux: true
  roles:
    - redhat.rhel_system_roles.vpn
```
The role sets up a tunnel between each pair of hosts listed, and host names are assumed to match
the inventory names and to resolve (use `hostname:` to give an FQDN or IP instead). A host that is
not in the inventory (a cloud gateway) needs `hostname:`; the role then configures only the local
end of its tunnels. The role generates PSKs with `openssl` on the controller (`vpn_ensure_openssl`,
default true). To supply your own, use `shared_key_content` read from Vault, never plain text in
inventory; the README advises letting the role generate keys, and notes the PSK is visible in verbose
or debug output.

## Certificate authentication
```yaml
vpn_connections:
  - hosts:
      app1.example.com: {hostname: 10.0.1.11, cert_name: app1}
      app2.example.com: {hostname: 10.0.1.12, cert_name: app2}
    auth_method: cert
```
The `cert_name` must already exist in the IPsec NSS certificate database on the host; the
`certificate` system role can issue such certificates. `auth_method` (or global `vpn_auth_method`)
accepts `psk` or `cert` and sets Libreswan `authby`.

## Opportunistic mesh
```yaml
vpn_connections:
  - opportunistic: true
    auth_method: cert
    policies:
      - {policy: private, cidr: default}
      - {policy: private-or-clear, cidr: 192.168.122.0/24}
      - {policy: clear, cidr: 192.168.110.7/32}   # the control node
```
Valid `policy` values are `private`, `private-or-clear` (the default) and `clear`; `cidr: default`
applies a policy to every host not matched by another entry. If the control node shares a CIDR with
the mesh, add a `clear` policy for its address or the SSH connection is lost during the play.

## Gotchas
- `vpn_regen_keys` (default false) controls whether PSKs are regenerated for host sets that already have keys.
- `vpn_manage_firewall` and `vpn_manage_selinux` default to false and only add ports and policy; to remove them use the firewall or selinux role directly. SELinux management is skipped if the firewall is not installed.
- `auto` accepts `add`, `ondemand`, `start` and `ignore`; the default is null (no automatic startup operation).
- Leave `ike`, `esp` and the other Libreswan algorithm settings unset unless you must; the role README says the minimum acceptable algorithms are AES, MODP2048 and SHA2.
- The README flags `leftupdown`: keep arguments free of spaces and shell metacharacters.

## Verify
- [ ] `ipsec status | grep <connectionname>` shows the connection loaded.
- [ ] `ipsec trafficstatus | grep <connectionname>` shows the tunnel started.
- [ ] `ipsec whack --listcerts` shows an imported certificate (cert auth).
- [ ] If a connection did not load, `ipsec auto --add <connectionname>` prints the specific error.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the linux-system-roles vpn README (read in full). Confirmed: variable names and defaults, `psk`/`cert`, `auto` values, policy values and `default` cidr, ports 500/UDP, 4500/UDP and 4500/TCP, manage_firewall/selinux behaviour, verification commands. Removed as unsupported by the page: the claim that every host must be in the play, the NSS path and `ipsec import` command, "mesh is certificate-only", the MTU and ESP overhead advice, the cloud security group note, the tcpdump check, the `ipsec status | grep established` check and the back-up advice for generated PSKs. The Red Hat RHEL 9 guide and Libreswan man page were not read, so they are no longer cited.
