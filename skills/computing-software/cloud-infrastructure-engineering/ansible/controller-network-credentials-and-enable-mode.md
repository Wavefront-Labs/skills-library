---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-network-credentials-and-enable-mode
name: controller-network-credentials-and-enable-mode
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, network-credential, machine-credential, enable-mode, become-enable, network-cli, cisco-ios, privilege-escalation]
level: practitioner
status: docs-checked
description: "Choose and configure controller credentials for network devices: Machine credential with become method enable for network_cli, the legacy Network type, and enable passwords."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://docs.ansible.com/projects/ansible/latest/network/user_guide/platform_index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller network credentials and enable mode

Goal: jobs log in to switches/routers with the right user and enter privileged (enable) mode
without passwords appearing in inventory, surveys or job output.

## Modern way: Machine credential + network_cli
Inventory/group vars (no secrets):
```yaml
# group_vars/ios.yml
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: cisco.ios.ios
ansible_become: true
ansible_become_method: enable
```
Credential type **Machine**:
- Username / Password (or SSH private key)
- Privilege Escalation Method: `enable`
- Privilege Escalation Password: the enable secret
Attach it to the job template. Controller injects `ansible_user`, `ansible_password`/key and
`ansible_become_password`; `network_cli` uses the become password to answer the `enable` prompt.

## Legacy "Network" credential type
A separate Network credential type exists for the old `connection: local` + `provider:` style
modules. Only use it for playbooks you have not migrated yet; with `network_cli` its injected
variables are ignored.

## Per-platform notes
Check each platform's become support in the Ansible network platform guide before enabling
escalation: IOS-style devices use `enable` with the enable secret; NX-OS/Junos-style platforms
typically take user privilege from AAA and need no become.

## Multiple device groups with different passwords
One Machine credential per access tier; a job template accepts only one Machine credential, so
split templates per tier or use a custom credential type with `extra_vars` injectors per group
(and `ansible_become_password: "{{ tier_b_enable }}"` in group vars), or an external secret
lookup (CyberArk, Vault) attached to the credential fields.

## Gotchas
- Setting `ansible_become_password` in inventory overrides the credential's injected value — and leaks it into inventory; keep it only in the credential.
- AAA/TACACS users with privilege 15 at login do not need enable; forcing `become` on them can hang waiting for a prompt that never comes. Increase `ansible_command_timeout` only after checking the prompt.
- Network jobs run on the execution node, which must reach device management IPs (port 22/443/830); pin the template to an instance group with that reach.

## Verify
- [ ] `cisco.ios.ios_command: commands: [show privilege]` returns level 15 in a job.
- [ ] Job output and the job API show no password values (`$encrypted$` only).

## Checked

- 2026-10-31: Machine credential fields (username/password/SSH key, privilege escalation method and
  password), `$encrypted$` handling and the job API status/fields confirmed in AAP 2.5 Using
  automation execution; the network automation platform guide (platform_index) confirms the
  platform-specific privilege-escalation model.
- Removed: the legacy Network-credential env-var list (`ANSIBLE_NET_USERNAME` etc.) and the
  per-platform become table (kept as a pointer to the platform guide).
Method: documentation only; no commands were run.
