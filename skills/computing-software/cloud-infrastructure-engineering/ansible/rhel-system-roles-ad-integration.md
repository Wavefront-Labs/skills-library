---
id: computing-software.cloud-infrastructure-engineering.ansible.rhel-system-roles-ad-integration
name: rhel-system-roles-ad-integration
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, rhel-system-roles, ad-integration-role, ad-integration, active-directory, realmd, sssd, domain-join, kerberos, linux-system-roles]
level: practitioner
status: docs-checked
description: "Join RHEL hosts to Active Directory with the ad_integration system role: realm, join credentials, computer OU, time and DNS prerequisites, crypto policy and SSSD settings."
sources:
  - https://raw.githubusercontent.com/linux-system-roles/ad_integration/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RHEL system roles: ad_integration (join Active Directory)

Goal: hosts join AD directly (realmd + SSSD), users log in with AD credentials, and the join is
repeatable and auditable instead of a hand-typed `realm join`.

## Playbook
```yaml
- hosts: linux_servers
  become: true
  vars:
    ad_integration_realm: CORP.EXAMPLE.COM
    ad_integration_user: svc-linuxjoin             # default is Administrator
    ad_integration_password: "{{ vault_ad_join_password }}"
    ad_integration_computer_ou: "OU=Linux,OU=Servers,DC=corp,DC=example,DC=com"
    ad_integration_manage_timesync: true
    ad_integration_timesync_source: dc01.corp.example.com
    ad_integration_manage_dns: true
    ad_integration_dns_server: 10.0.0.10
    ad_integration_dns_connection_name: ens192     # connection profile name, not the interface
    ad_integration_dns_connection_type: ethernet
    ad_integration_manage_crypto_policies: true
    ad_integration_allow_rc4_crypto: false         # true only if AES cannot be enabled in AD
    ad_integration_sssd_custom_settings:           # goes into the [domain/$REALM] section
      - {key: use_fully_qualified_names, value: "False"}
  roles:
    - redhat.rhel_system_roles.ad_integration
```
`ad_integration_realm` and `ad_integration_password` are the required variables. Use Ansible Vault
for the password, not cleartext. `ad_integration_sssd_settings` writes into the `[sssd]` section,
`ad_integration_sssd_custom_settings` into `[domain/$REALM]`, and `ad_integration_sssd_section_settings`
into any section (for example `nss` or `pam`).

## Prerequisites the role does not fully fix for you
- Use an AD user with sufficient join permissions; the README advises against Administrator because its security footprint is too large, and points to adcli's "Delegated Permissions" for the exact rights.
- The Linux host must resolve the default AD DNS SRV records (the role can add a DNS server with `ad_integration_manage_dns`).
- Time must be in sync with AD; the role uses the timesync role when `ad_integration_manage_timesync` is true and `ad_integration_timesync_source` is set.
- Ports reachable on the AD side from the client: DNS 53 (TCP/UDP), LDAP 389 (TCP/UDP), LDAPS 636 (TCP), Kerberos 88 and 464 (TCP/UDP), Global Catalog 3268 (TCP) and 3269 (TCP), and optionally NTP 123 and 323 (UDP).

## Re-runs, rejoin and leave
`ad_integration_force_rejoin: true` leaves the realm and joins again; the README says it may be needed
if the keytab cannot authenticate the machine account to the domain (default false). Set
`ad_integration_state: absent` to leave the realm; `ad_integration_leave_remove_computer`,
`ad_integration_leave_reset_computer` and `ad_integration_leave_sssd_cache_delete` control what else
happens on leave (all default false). `ad_integration_preserve_authselect_profile: true` stops realmd
overwriting earlier PAM/nsswitch changes (default false).

## Gotchas
- The role suppresses sensitive task output while `ad_integration_secure_logging` is true (the default); set it false only to debug.
- RHEL 8 and newer, and Fedora, no longer support RC4 out of the box. Enable AES in Active Directory if you can; otherwise the AD-SUPPORT crypto policy is needed, which the role sets via `ad_integration_manage_crypto_policies` and `ad_integration_allow_rc4_crypto` and which may reboot the machine.
- Older role versions lower-cased the realm in the sssd.conf section name, so duplicate `[domain/...]` sections can exist. `ad_integration_sssd_merge_duplicate_sections: true` merges them but forces a rejoin.
- `use_fully_qualified_names: False` changes username format, so anything keyed on the old names must be checked.

## Verify
- [ ] With `ad_integration_validate_sssd_config` true (the default) and the SSSD client, the role runs `sssctl config-check` after changes; the play fails on an invalid sssd.conf.
- [ ] A second run of the play reports no unexpected changes.
- [ ] The computer account appears in the expected OU in AD.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the linux-system-roles ad_integration README (read in full). Confirmed: variable names, defaults, firewall port table, RC4/AES and AD-SUPPORT text, time sync, leave options, secure logging, sssd settings sections. Corrected: domain-level SSSD settings belong in `ad_integration_sssd_custom_settings`, not `ad_integration_sssd_settings`. Removed as not in the page: the 5-minute clock skew figure, the 15-character NetBIOS hostname limit, `realm permit` and GPO access control advice, the claim that already-joined hosts are skipped, the snapshot-restore rejoin reason, the `realm list`, `id`, `kinit` and `dig` checks, and the exact AD permission list (the README only links to it). The Red Hat guide and man pages were not read, so they are no longer cited.
