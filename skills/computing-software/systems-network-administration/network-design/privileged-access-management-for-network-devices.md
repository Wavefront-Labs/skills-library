---
id: computing-software.systems-network-administration.network-design.privileged-access-management-for-network-devices
name: privileged-access-management-for-network-devices
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, access-management, privileged-access-management, credential-vault, tacacs, break-glass]
level: practitioner
status: draft
description: "Control privileged access to network devices: TACACS+/RADIUS with MFA, vaulted local and shared credentials, session brokering and recording, rotation and break-glass accounts."
sources:
  - https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
  - https://developer.hashicorp.com/vault/docs/secrets
  - https://www.cisco.com/c/en/us/td/docs/security/ise/3-2/admin_guide/b_ise_admin_3_2/b_ISE_admin_32_device_admin_policies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Privileged access management for device credentials

## Layers
1. **Named accounts via AAA**: TACACS+ (ISE, ClearPass, tac_plus-ng) with per-command authorisation
   and accounting; MFA at the AAA server or the jump host.
2. **Vaulted local/shared credentials**: local admin, enable secret, SNMPv3 keys, API tokens in
   a vault (CyberArk, Delinea, HashiCorp Vault, Bitwarden for small teams) with check-out logs.
3. **Session brokering/recording**: PAM proxy or bastion records SSH/RDP/console sessions for audit.

## Local accounts
- One emergency local account per device (break-glass), unique password per device stored in the
  vault, used only when AAA is unreachable (`aaa authentication login default group tacacs+ local`).
- Rotate after each use and on schedule; automation (Ansible/Nornir) with vault lookups changes them.
- Remove default/vendor accounts; disable password recovery where policy requires.

## Automation credentials
Service accounts with scoped privilege levels, short-lived tokens where APIs allow, stored in the
vault and injected at runtime (never in git or playbooks).

## Controls to evidence (NIST 800-53 AC-2, AC-6, IA-2(1), AU-12)
Least privilege roles (read-only vs config), MFA, logging of every command, periodic access reviews,
immediate removal for leavers.

## Verify
- [ ] Every device login maps to a named person or a vaulted check-out; break-glass use alerts and triggers rotation; quarterly access review completed.
