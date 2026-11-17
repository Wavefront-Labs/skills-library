---
id: computing-software.cybersecurity-defensive.security-architecture.ssh-certificate-authority
name: ssh-certificate-authority
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [cryptography, ssh-certificates, ssh-ca, ssh-keygen, trustedusercakeys, short-lived-credentials, principals, vault-ssh]
level: advanced
status: docs-checked
description: "Replace authorized_keys sprawl with an SSH CA: user and host certs, principals, validity windows, TrustedUserCAKeys, KRL revocation, and issuing via Vault."
sources: ["https://man.openbsd.org/ssh-keygen#CERTIFICATES", "https://man.openbsd.org/sshd_config", "https://developer.hashicorp.com/vault/docs/secrets/ssh/signed-ssh-certificates"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH certificate authority

Static public keys in `authorized_keys` are hard to audit and revoke. OpenSSH certificates
consist of a public key, identity information, zero or more principal (user or host) names and options,
signed by a CA key. Clients or servers trust only the CA key. OpenSSH certificates are a different, much
simpler format than X.509.

Keep CA private keys offline, in a PKCS#11 token or ssh-agent (`-D` and `-U` options), or in a system such as Vault.

## User certificates
Sign a user's public key with principals (typically usernames):
```
ssh-keygen -s /path/to/ca_key -I id -n user1,user2 /path/to/user_key.pub
```
The certificate is written as `user_key-cert.pub`. `-I` is a key identifier that the server logs when the
certificate is used and that can be used to revoke keys. `-V` sets the validity start and end times; by
default a certificate is valid from the Unix Epoch to the distant future, so always set a window.

Server `sshd_config`:
```
TrustedUserCAKeys /etc/ssh/user_ca.pub
AuthorizedPrincipalsFile /etc/ssh/auth_principals/%u
RevokedKeys /etc/ssh/revoked_keys
```
`TrustedUserCAKeys` lists CA public keys one per line; a certificate signed by a listed CA may log in as
any user in its principals list, and certificates without principals are refused. If `AuthorizedPrincipalsFile`
is set (it accepts the `%u` token), the certificate must contain a principal listed in that file for the
target user; the default is none, in which case the username must appear in the certificate's principals.
Certificate options restrict use: `no-port-forwarding`, `force-command=command`, and
`source-address=address_list` (CIDR pairs). Unknown critical options cause the certificate
to be refused.

## Host certificates
```
ssh-keygen -s /path/to/ca_key -I id -h -n foo.example.org /path/to/host_key.pub
```
For host certificates the `-n` principals are hostnames and may contain wildcards. The certificate is written
as `host_key-cert.pub`. In `sshd_config`, `HostCertificate` names the certificate file; its public key must
match a private host key already given with `HostKey`.

## Issuance in practice
Do not hand-sign. HashiCorp Vault's SSH secrets engine can act as the CA: enable it with
`vault secrets enable -path=ssh-client-signer ssh`, configure the CA at `config/ca`, put the CA public key on
target hosts as the `TrustedUserCAKeys` file, and create a role that sets a `ttl`. Prefer short TTLs. Vault roles
that omit `allowed_extensions` were permissive before Vault 1.9, so set it explicitly.

## Revocation
Prefer short validity. For emergencies, `ssh-keygen -k` generates a Key Revocation List (KRL), which can revoke
certificates by serial number or key ID (the CA key must be given with `-s`); `-u` merges into an existing KRL.
Point `RevokedKeys` at it. sshd may consult the file on every public-key attempt, so replace it atomically and
never edit it in place, and note that if the file is not readable, public key authentication is refused for
all users.

## Gotchas
- Set `AuthorizedKeysFile none` once certificates are rolled out, otherwise old keys in `authorized_keys` still work (the default is `.ssh/authorized_keys .ssh/authorized_keys2`).
- A certificate with no validity window never expires; always pass `-V`.
- sshd logs the certificate key ID, so make `-I` values meaningful for audit.

## Verify
An expired certificate is refused; a certificate whose principals do not include the target user (or a listed
principal) is refused; a certificate listed in the KRL is refused; `authorized_keys` login is disabled.

## Checked

2026-11-08: Read ssh-keygen (CERTIFICATES and KEY REVOCATION LISTS sections as served), sshd_config (TrustedUserCAKeys, AuthorizedPrincipalsFile, RevokedKeys, HostCertificate, AuthorizedKeysFile) and the Vault signed SSH certificates page. Rewrote to what these state. Removed: the CA key-generation commands, the +8h and -z 1042 and -L examples, 52-week host validity, the known_hosts cert-authority line, CA rotation advice, clock-skew advice, step-ca and Teleport mentions, and the serial-in-logs claim, because the fetched pages do not state them.

Method: docs-only read of cited pages, 2026-11-08
