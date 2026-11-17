---
id: computing-software.messaging-and-integration.apache-zookeeper.authentication-providers-config
name: authentication-providers-config
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, authentication, superuser, superdigest, digest-auth, x509, ip-auth, sasl]
level: advanced
status: docs-checked
description: "Server-side authentication settings: zookeeper.superUser, X509 and digest superuser, digestAlg SHA1, IP x-forwarded-for risk, authProvider.N and ensembleAuthName."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication settings

- `zookeeper.superUser`: name of a SASL user who can access the znode hierarchy as super user; several via `zookeeper.superUser.[suffix]` (for example `zookeeper.superUser.1`).
- `X509AuthenticationProvider.superUser`: an X500 principal name; only an authenticated client with that principal bypasses ACL checks.
- `DigestAuthenticationProvider.superDigest` (3.2+): disabled by default; no ACL checking for a user authenticated as super. Generate the value with `org.apache.zookeeper.server.auth.DigestAuthenticationProvider` called with `super:...`; clients pass scheme `digest` with the matching authdata. Digest authdata travels in plaintext, so use localhost or an encrypted connection.
- `DigestAuthenticationProvider.enabled` (3.7): default true for backwards compatibility; consider disabling if unused because it can create misleading audit-log entries.
- `DigestAuthenticationProvider.digestAlg` (3.7.0): default SHA1, which the page says will be deprecated; set the same value on all servers. To migrate, regenerate the superDigest and setAcl on znodes that used the old algorithm.
- `IPAuthenticationProvider.usexforwardedfor` (3.9.3): default false. When on, X-Forwarded-For is preferred over the Host header; ZooKeeper does not validate it, so any client can forge an IP and bypass IP-based ACLs. Enable only behind trusted proxies that overwrite the header and with direct access blocked.
- `authProvider.[n]`: register provider classes, usually SASL, for example `authProvider.1=org.apache.zookeeper.server.auth.SASLAuthenticationProvider`.
- `zookeeper.ensembleAuthName` (3.6.0, system property only): comma-separated valid ensemble names; a client presents the name as the credential for scheme `ensemble`, and a mismatch is refused (guards against connecting to the wrong ensemble).
- `sessionRequireClientSASLAuth` (3.6.0): default false; when true only SASL-authenticated clients get a session.
- `fips-mode` (3.8.2): default true in 3.9.0+, false in 3.8.x; disables the custom ZKTrustManager (no hostname verification on the quorum protocol) and DIGEST-MD5 SASL (only GSSAPI/Kerberos remains).

Keep a super user credential in a secret store, never in docs: use `<PASSWORD>` placeholders in examples.

Verify: `whoami` in the CLI lists the auth schemes added to the session, for example `digest: user1` after `addauth digest user1:12345`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Administrator's Guide (Encryption, Authentication, Authorization options) and the CLI guide (`whoami`, `addauth`). No claims removed.
