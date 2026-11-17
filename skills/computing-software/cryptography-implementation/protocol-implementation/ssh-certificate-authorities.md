---
id: computing-software.cryptography-implementation.protocol-implementation.ssh-certificate-authorities
name: ssh-certificate-authorities
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, ssh, openssh, ssh-certificates, ssh-ca, trustedusercakeys, principals, host-certificates, krl, short-lived-certificates]
level: advanced
status: docs-checked
description: "Run an OpenSSH certificate authority: signing user and host certs with principals and validity, TrustedUserCAKeys and @cert-authority, KRL revocation, and short-lived issuance."
sources: ["https://man.openbsd.org/ssh-keygen#CERTIFICATES", "https://man.openbsd.org/sshd_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH certificate authorities

OpenSSH certificates (not X.509) replace `authorized_keys` sprawl and
trust-on-first-use host keys: servers trust a CA key, and the CA signs user
keys with principals and expiry.

## User certificates

```bash
ssh-keygen -t ed25519 -f user_ca -C "user CA 2026"            # keep offline / in HSM / Vault
ssh-keygen -s user_ca -I "alice@corp ticket-1234" -n alice,deploy \
  -V +8h -O no-port-forwarding -z 1001 alice_id_ed25519.pub    # -> alice_id_ed25519-cert.pub
ssh-keygen -L -f alice_id_ed25519-cert.pub                      # inspect
```

Server (`sshd_config`):

```
TrustedUserCAKeys /etc/ssh/user_ca.pub
AuthorizedPrincipalsFile /etc/ssh/principals/%u     # which principals may log in as each user
```

- `-n` principals: without `AuthorizedPrincipalsFile`, the principal must
  equal the Unix username. Use the file to map roles (`deploy`) to accounts.
- `-V +8h`: short validity means no revocation needed in practice.
- `-I` key id appears in sshd logs - put the human and ticket in it.
- `-z` serial lets you revoke specific certs.

## Host certificates

```bash
ssh-keygen -s host_ca -I web01 -h -n web01.corp,10.0.0.5 -V +52w /etc/ssh/ssh_host_ed25519_key.pub
# sshd_config: HostCertificate /etc/ssh/ssh_host_ed25519_key-cert.pub
```

For host certificates the `-n` principals are host names and may contain wildcards.

## Revocation

```bash
ssh-keygen -k -f /etc/ssh/revoked.krl -s user_ca.pub -z 1001     # revoke by serial
ssh-keygen -k -u -f /etc/ssh/revoked.krl alice_id_ed25519.pub    # revoke a key
# sshd_config: RevokedKeys /etc/ssh/revoked.krl
```

Distribute the KRL to all servers; if the `RevokedKeys` file is not readable, sshd
refuses public key authentication for all users, so deploy the file before the config line.
Replace the file atomically; do not modify it in place while sshd runs.

## Operating the CA

Protect the CA private key like a root CA and keep user and host CAs separate.
A CA key can also live in an ssh-agent or PKCS#11 token (`-U`, `-D`) instead of a file.

## Verify

- [ ] sshd logs show the certificate key id (`-I`).
- [ ] Expired cert and wrong principal are rejected.
- [ ] KRL present on all servers; revoked serial cannot log in.

## Checked

Date: 2026-11-01. Confirmed in the OpenBSD ssh-keygen manual (CERTIFICATES, KEY REVOCATION LISTS, -s -I -n -V -z -h -k -u -U -D) and sshd_config manual (TrustedUserCAKeys, AuthorizedPrincipalsFile default behaviour, RevokedKeys unreadable-file behaviour and atomic replacement, HostCertificate). Removed: the `@cert-authority` known_hosts example and TOFU claims, the PROTOCOL.certkeys source (page not found), vendor CA tools, validity-duration advice, CA rotation overlap and the `ssh -v` message (not in the cited pages).
Method: documentation only; no commands were run.
