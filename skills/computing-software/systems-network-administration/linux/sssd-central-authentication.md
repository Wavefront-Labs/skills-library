---
id: computing-software.systems-network-administration.linux.sssd-central-authentication
name: sssd-central-authentication
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sssd, ldap, kerberos, realmd, central-authentication, active-directory, freeipa, domain-join, adcli, authselect, pam-sss, nss, keytab, kinit, id-mapping, sudo-ldap, home-directory, oddjob-mkhomedir, lpic-2, sysadmin, sssd-conf, simple-allow-groups]
level: advanced
status: draft
description: "Join Linux hosts to Active Directory or FreeIPA/LDAP with realmd and SSSD: domain join, sssd.conf access control, Kerberos tickets, home dirs, and the cache/clock/DNS failures that lock users out."
sources:
  - https://man.archlinux.org/man/sssd.conf.5
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/integrating_rhel_systems_directly_with_windows_active_directory/index
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SSSD central authentication — AD / FreeIPA / LDAP logins that keep working offline

**Goal:** let domain users log in to a Linux host with their central password, get a
home directory and the right groups, restrict who may log in, and survive a flaky DC.

## 1. Prerequisites that cause 90 % of failures
```bash
timedatectl                                  # clock within 5 min of the DC (Kerberos)
dig +short SRV _ldap._tcp.corp.example       # DNS must resolve the domain's SRV records
hostnamectl set-hostname host01.corp.example # FQDN; realm uses it for the computer object
```
Packages: RHEL `dnf install realmd sssd adcli oddjob oddjob-mkhomedir samba-common-tools krb5-workstation`;
Debian/Ubuntu `apt install realmd sssd sssd-tools adcli libnss-sss libpam-sss krb5-user packagekit`.

## 2. Join
```bash
realm discover corp.example                  # shows required packages and type (active-directory / kerberos=IPA)
realm join -U Administrator corp.example --computer-ou='OU=Linux,DC=corp,DC=example'
realm list                                   # login-policy, configured: kerberos-member
id alice@corp.example
```
FreeIPA clients use `ipa-client-install --mkhomedir` instead (configures SSSD, NTP,
certs and sudo in one go).

## 3. `/etc/sssd/sssd.conf` (mode 0600 root, or sssd refuses to start)
```ini
[sssd]
domains = corp.example
config_file_version = 2
services = nss, pam

[domain/corp.example]
id_provider = ad
access_provider = ad                 # honours AD "logon to" + GPO; or simple (below)
ad_domain = corp.example
krb5_realm = CORP.EXAMPLE
realmd_tags = manages-system joined-with-adcli
cache_credentials = True             # offline logins with cached hash
use_fully_qualified_names = False    # login as "alice" not "alice@corp.example"
fallback_homedir = /home/%u@%d
default_shell = /bin/bash
ldap_id_mapping = True               # SID->UID hashing; False if AD has POSIX uidNumber (rfc2307)
dyndns_update = True
# ad_gpo_access_control = permissive # if GPO "Allow log on locally" blocks everyone
```
Restrict logins without touching AD:
```bash
realm permit -g linux-admins@corp.example      # access_provider = simple; simple_allow_groups
realm deny --all
```
After edits: `systemctl restart sssd` and `sss_cache -E` (flush) when group changes don't appear.

## 4. PAM/NSS wiring and home directories
- RHEL: `authselect select sssd with-mkhomedir --force` and `systemctl enable --now oddjobd`.
- Debian/Ubuntu: `pam-auth-update` (tick "Create home directory on login") or add
  `session optional pam_mkhomedir.so skel=/etc/skel umask=0077` to `common-session`.
- `/etc/nsswitch.conf` must list `sss` for `passwd group shadow sudoers`
  (`getent passwd alice` proves NSS; `su - alice` proves PAM).
- sudo via AD groups: in `/etc/sudoers.d/domain`: `%linux-admins@corp.example ALL=(ALL) ALL`
  (escape spaces as `\ `; group names with `use_fully_qualified_names=False` drop the `@domain`).

## 5. Kerberos day-to-day
```bash
kinit alice; klist                           # user ticket; SSH with GSSAPIAuthentication yes = passwordless
klist -k /etc/krb5.keytab                    # host keytab created by join (host/host01.corp.example@CORP.EXAMPLE)
adcli update --computer-password-lifetime=30 # rotate machine password (sssd does it automatically by default)
```
Ticket in SSH sessions: `pam_sss` obtains a TGT at password login (`krb5_store_password_if_offline`),
so NFS `sec=krb5` home dirs work without a second `kinit`.

## 6. Troubleshooting
```bash
sssctl domain-status corp.example            # online/offline, active server
sssctl user-checks alice -s sshd             # simulates NSS+PAM for a service
journalctl -u sssd -b; sss_debuglevel 6; tail -f /var/log/sssd/sssd_corp.example.log
```
| Symptom | Cause |
|---|---|
| `realm join` → "Couldn't authenticate" / KDC not reachable | clock skew or DNS not resolving SRV; `kinit Administrator` to isolate |
| Login works for some users, not others | `access_provider` GPO/`simple_allow_groups`; `sssctl user-checks` shows the deny reason |
| UID differs between hosts | `ldap_id_mapping` differs or different `ldap_idmap_range_*`; keep sssd.conf identical fleet-wide |
| Groups missing after AD change | cache: `sss_cache -u alice` or `-E`; default `entry_cache_timeout` 5400 s |
| Everyone locked out when DC down | `cache_credentials = False` or user never logged in while online |
| sssd won't start | `sssd.conf` not 0600, or typo — `sssctl config-check` |

## Verify
- [ ] `getent passwd alice` and `id alice` return UID + all AD groups.
- [ ] SSH login as a domain user creates the home dir and `klist` shows a TGT.
- [ ] Disconnect from the DC (`realm` still joined): a previously logged-in user can still log in.
