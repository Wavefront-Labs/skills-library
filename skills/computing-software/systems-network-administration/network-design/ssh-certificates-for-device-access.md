---
id: computing-software.systems-network-administration.network-design.ssh-certificates-for-device-access
name: ssh-certificates-for-device-access
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, access-management, ssh-certificates, ssh-ca, openssh, network-device-access]
level: practitioner
status: docs-checked
description: "Use SSH certificates instead of static keys for admin access to network devices and servers: an SSH CA, short-lived user certs, principals, and device platform support."
sources:
  - https://man.openbsd.org/ssh-keygen.1#CERTIFICATES
  - https://developer.hashicorp.com/vault/docs/secrets/ssh/signed-ssh-certificates
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SSH certificates for device access

## Why
Static authorized_keys spread across hundreds of devices never get cleaned up when people leave.
With an SSH CA, devices trust **one CA key**; users get short-lived certificates (hours) carrying
their identity and allowed principals. Short lifetimes limit the need for revocation (OpenSSH also supports key revocation lists).

## Setting up (OpenSSH)
```
ssh-keygen -t ed25519 -f user_ca                     # keep offline / in Vault or a KMS
ssh-keygen -s user_ca -I alice@corp -n netadmin,readonly -V +<validity> id_ed25519.pub
ssh-keygen -L -f id_ed25519-cert.pub                 # inspect principals and validity
```
Device/server side (`sshd_config`):
```
TrustedUserCAKeys /etc/ssh/user_ca.pub
AuthorizedPrincipalsFile /etc/ssh/principals/%u     # map principals to local accounts
```
Host certificates (`ssh-keygen -s host_ca -h -I sw1 -n sw1.example.com host.pub`) let clients trust
hosts by CA instead of per-host keys (see ssh(1) and sshd(8) for the client-side trust setting).

## Issuing at scale
HashiCorp Vault's SSH secrets engine signs client keys (its documented example sets a 30 minute
ttl): the user authenticates to Vault first and receives a short-lived certificate.

## Network device support
Support for OpenSSH certificate authentication varies by platform and software version: check each
device's documentation for a trusted-CA setting before relying on it. Where a device cannot validate
SSH certificates, front it with a bastion that does and use TACACS+/RADIUS for the device login.

## Verify
- [ ] Expired certificate is refused; a user whose principals do not match the account cannot log in; CA private key access is audited.

## Checked

2026-10-28: Confirmed: ssh-keygen -s, -I, -n (principals), -h (host certificate) and -V (validity) in the OpenBSD ssh-keygen man page; TrustedUserCAKeys and AuthorizedPrincipalsFile with the %u token in sshd_config; Vault SSH secrets engine signing with valid_principals, a documented ttl of 30m, and ssh-keygen -L to inspect. Removed: the +8h example, the 8-hour issuance claim, the known_hosts @cert-authority line, and the per-platform support list (SONiC, Cumulus, EOS, Junos trusted-key, IOS-XE), none of which a fetched page confirmed.
Method: documentation only; no commands were run.
