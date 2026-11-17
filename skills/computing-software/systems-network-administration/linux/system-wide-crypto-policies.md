---
id: computing-software.systems-network-administration.linux.system-wide-crypto-policies
name: system-wide-crypto-policies
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, crypto-policies, update-crypto-policies, fips-mode, openssl-policy, tls-legacy, sha1]
level: practitioner
status: docs-checked
description: "Manage RHEL-family system-wide crypto policies: DEFAULT, LEGACY, FUTURE, FIPS, subpolicies like NO-SHA1 or AD-SUPPORT, custom modules, and per-application opt-outs."
sources:
  - https://gitlab.com/redhat-crypto/fedora-crypto-policies
  - https://gitlab.com/redhat-crypto/fedora-crypto-policies/-/blob/master/crypto-policies.7.txt
  - https://gitlab.com/redhat-crypto/fedora-crypto-policies/-/blob/master/update-crypto-policies.8.txt
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# System-wide crypto policies

Distributions that ship the `crypto-policies` package (Fedora and the RHEL family): one setting generates back-end configs for BIND, GnuTLS, OpenJDK, Kerberos 5, Libreswan, NSS, OpenSSH, OpenSSL, libssh and the Sequoia PGP libraries under `/etc/crypto-policies/back-ends/`. Go applications and GnuPG 2 do not follow it, and only data in transit is covered.

## Inspect and set
```bash
update-crypto-policies --show                # current policy
update-crypto-policies --set DEFAULT:NO-SHA1
update-crypto-policies --set LEGACY          # temporarily, for an old peer
reboot                                       # recommended; otherwise restart every affected application (back-ends read the config at start-up)
```
| Policy | Meaning |
|---|---|
| DEFAULT | TLS/DTLS 1.2+, RSA and DH >= 2048 bits, signatures with SHA-224 or better and no DSA (SHA-1 signatures stay allowed in DNSSEC) |
| NEXT | alias of DEFAULT |
| LEGACY | TLS/DTLS 1.0+, 3DES and DSA allowed, RSA and DH > 1024 bits, SHA-1 signatures; for interop only (at least 64-bit security) |
| FUTURE | RSA and DH > 3071 bits, no SHA-1 in signatures, 256-bit AE ciphers only, no RSA key exchange; may break communication with common systems |
| BSI | based on BSI TR 02102 |
| FIPS | aids FIPS 140 conformance; applied automatically when the kernel boots with `fips=1` |
Subpolicies append with colons. Shipped ones include `NO-SHA1` (drops SHA-1 hash and signature support), `SHA1` (adds it back), `AD-SUPPORT` (re-enables RC4 and MD5 in Kerberos for Active Directory environments not yet migrated to AES), `OSPP` (restricts FIPS for the Common Criteria OSPP profile), `NO-CAMELLIA`, `ECDHE-ONLY`, `NO-HMAC-SHA1`.

## Custom subpolicy
Subpolicy files end in `.pmod`, live in `/etc/crypto-policies/policies/modules`, and need upper-case names. Use `option@scope = ...` to limit a directive to some back-ends (scopes such as `TLS`, `SSH`, `kerberos`); `-value` omits, `value+` appends.
```
# /etc/crypto-policies/policies/modules/NO-CBC.pmod
cipher@TLS = -AES-256-CBC -AES-128-CBC
cipher@SSH = -AES-256-CBC -AES-128-CBC
```
```bash
update-crypto-policies --set DEFAULT:NO-CBC
```

## Per-application exceptions (prefer over LEGACY)
The policy sets defaults only: a user can override it for one application by configuring that application explicitly (for example OpenSSH `Ciphers`/`KexAlgorithms`, or an application's own TLS settings). Prefer that, or a narrow subpolicy such as `SHA1`, over switching the whole system to LEGACY.

## Typical failures after hardening
Peers that only offer what the stricter policy removes fail to connect: TLS below 1.2, certificates or signatures using SHA-1, RSA or DH parameters below the minimum, 3DES, or (under FUTURE) RSA key exchange and non-AE ciphers. For Kerberos against Active Directory accounts that lack AES keys, the long-term fix is to enable AES on the accounts rather than keep `AD-SUPPORT`. Compare the failing peer with the policy lists above, then use `update-crypto-policies --check` to confirm the generated files match the set policy.

## Verify
- [ ] `update-crypto-policies --show` matches the baseline on every host (check in config management).
- [ ] A TLS 1.1 handshake fails under DEFAULT (for example `openssl s_client -connect host:443 -tls1_1`, if your OpenSSL build still offers that option); required partners still connect.

## Checked
Checked 2026-10-27 against the upstream fedora-crypto-policies sources (crypto-policies(7) and update-crypto-policies(8) text, and policies/modules/*.pmod on the master branch at gitlab.com/redhat-crypto/fedora-crypto-policies).
- Policy contents for DEFAULT, NEXT, LEGACY, FUTURE, BSI and FIPS are from crypto-policies(7); FIPS is applied automatically with `fips=1`; Go applications and GnuPG 2 do not follow the policy.
- Subpolicy files NO-SHA1, SHA1, AD-SUPPORT (RC4 and MD5 in Kerberos), OSPP, NO-CAMELLIA, ECDHE-ONLY, NO-HMAC-SHA1 exist; `.pmod` files go in `/etc/crypto-policies/policies/modules` with upper-case names; `option@scope` syntax; there is no `ssh_cipher` option, so `cipher@SSH` is used.
- `update-crypto-policies --show`, `--set`, `--check`; a restart is recommended after changing the policy.
- Removed unconfirmed claims: RHEL-version-specific statements, `fips-mode-setup`, `OPENSSL_CONF` and Java overrides, `sshd` ordering rule, and the error-message table. The earlier claim that FUTURE has no SHA-1 at all was corrected (it removes SHA-1 from signatures; HMAC needs SHA-256 or better).
Method: documentation only; no commands were run.
