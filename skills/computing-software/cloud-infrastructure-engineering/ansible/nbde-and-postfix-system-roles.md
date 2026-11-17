---
id: computing-software.cloud-infrastructure-engineering.ansible.nbde-and-postfix-system-roles
name: nbde-and-postfix-system-roles
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, rhel-system-roles, nbde-client-role, nbde-server-role, postfix-role]
level: practitioner
status: docs-checked
description: "Configure network-bound disk encryption with the nbde_server and nbde_client system roles (Tang/Clevis) and mail relays with the postfix role."
sources:
  - https://raw.githubusercontent.com/linux-system-roles/nbde_server/main/README.md
  - https://raw.githubusercontent.com/linux-system-roles/nbde_client/main/README.md
  - https://raw.githubusercontent.com/linux-system-roles/postfix/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nbde and postfix system roles

## Tang servers (nbde_server)
```yaml
- hosts: tang
  roles:
    - role: redhat.rhel_system_roles.nbde_server
      vars:
        nbde_server_manage_firewall: true
        nbde_server_manage_selinux: true
        nbde_server_port: 7500
```
The role deploys Tang. `nbde_server_port` defaults to 80; the role manages the firewall port and
SELinux labelling for it only when `nbde_server_manage_firewall` / `nbde_server_manage_selinux` are
true (both default false). `nbde_server_firewall_zone` defaults to `public`. Without keys the role
creates them; existing keys are untouched unless `nbde_server_rotate_keys: true` (default false).

Back up and redeploy keys with `nbde_server_fetch_keys: true` and `nbde_server_deploy_keys: true`;
both need `nbde_server_keys_dir` set to an absolute path on the control node. Fetched keys go in
subdirectories named after each host; keys in subdirectories are deployed to that host only, keys
in the top level to every host. Using the same keys on every host is supported but not recommended.

## LUKS clients (nbde_client)
```yaml
- hosts: encrypted
  roles:
    - role: redhat.rhel_system_roles.nbde_client
      vars:
        nbde_client_bindings:
          - device: /dev/vdb1
            encryption_password: "{{ vault_luks_passphrase }}"
            servers:
              - http://tang1.example.com:7500
              - http://tang2.example.com:7500
            threshold: 1
```
Only Tang bindings with Clevis are supported (not TPM2). The `device` must already be a LUKS device,
and you supply a valid `encryption_password` or `encryption_key_src` to unlock it (vault-encrypt it).
`slot` defaults to 1 and `state` to `present` (`absent` removes the binding). With several `servers`,
`threshold` is how many must succeed to recover the passphrase (Shamir Secret Sharing, default 1).
`password_temporary: true` removes the supplied passphrase after binding.

`nbde_client_early_boot` (default true) configures the initrd to unlock the volume; disabling it is for
volumes unlocked by clevis-luks-askpass. For static IP addressing use `nbde_client_extra_dracut_settings`
(lines written to `/etc/dracut.conf.d/nbde_client.conf`) rather than disabling early boot; it fails if
early boot is disabled.

## Postfix
```yaml
- hosts: all
  roles:
    - role: redhat.rhel_system_roles.postfix
      vars:
        postfix_conf:
          relayhost: example.com
        postfix_manage_firewall: false
        postfix_backup_multiple: true
```
`postfix_conf` is a dictionary of Postfix parameters (unsupported keys are ignored). `postfix_check`
(default true) runs `postfix check` before starting Postfix after a config change. `postfix_backup_multiple`
(default true) keeps timestamped copies of main.cf; to use the single-copy `postfix_backup` you must
set `postfix_backup_multiple: false`. `postfix_manage_firewall` opens 25/tcp, 465/tcp and 587/tcp and
`postfix_manage_selinux` labels them `smtp_port_t`; both default false and only add. SASL credentials
and other small lookup files go in `postfix_files` (with `postmap: true` to build the table).

## Gotchas
- NBDE binding needs an existing valid passphrase or key for the LUKS device; keep it in Vault.
- There is no way to remove individual Postfix parameters. `previous: replaced` inside `postfix_conf` reinstalls the postfix package and replaces `/etc/postfix/main.cf` and `master.cf`; back them up first.
- The role fetching keys writes them to the control node: protect `nbde_server_keys_dir`.

## Verify
- [ ] The play with `nbde_client_bindings` reports the binding added (and a second run reports no change).
- [ ] The Tang port you set in `nbde_server_port` is open and labelled if you enabled firewall and SELinux management.
- [ ] The Postfix settings you set in `postfix_conf` show up in `main.cf` after the play.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the linux-system-roles nbde_server, nbde_client and postfix READMEs (each read in full). Confirmed: variable names, defaults, key fetch/deploy behaviour, bindings keys, TPM2 limitation, dracut settings, `previous: replaced` warning, firewall ports, backup options. Removed as not in the pages: the key-rotation sequence (rebind clients, old keys kept), the `rd.neednet=1` advice, `clevis luks list` and `postconf relayhost` check commands, the `smtp_tls_security_level` and `inet_interfaces` example values, "restarts on change" and the claim that `postfix_conf` replaces only listed keys. The Red Hat RHEL 9 guide was not read, so it is no longer cited.
