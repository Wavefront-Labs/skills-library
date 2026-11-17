---
id: computing-software.systems-network-administration.dns-dhcp.tlsa-dane-and-sshfp-records
name: tlsa-dane-and-sshfp-records
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, tlsa-record, dane, sshfp, dnssec, certificate-pinning]
level: practitioner
status: verified
description: "Publish TLSA (DANE) and SSHFP records in DNSSEC-signed zones: generating values, usage/selector/matching fields, rollover order and client validation."
sources:
  - https://www.rfc-editor.org/rfc/rfc6698
  - https://www.rfc-editor.org/rfc/rfc7671
  - https://www.rfc-editor.org/rfc/rfc4255
  - https://www.rfc-editor.org/rfc/rfc7218
  - https://man.openbsd.org/ssh_config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLSA/DANE and SSHFP

Both bind keys to names via DNS. Both are only meaningful in DNSSEC-signed zones queried through
validating resolvers.

## SSHFP
```
ssh-keygen -r host.example.com -f /etc/ssh/ssh_host_ed25519_key.pub   # on the host, prints SSHFP lines for that key
host.example.com. IN SSHFP 4 2 <sha256-hex>    # algorithm 4 = Ed25519, 1 RSA, 3 ECDSA; type 2 = SHA-256
```
`ssh-keygen -r` prints two lines per key, fingerprint type 1 (SHA-1) and type 2 (SHA-256); publish the
SHA-256 line. Run against freshly generated Ed25519, RSA and ECDSA keys (OpenSSH on Windows) it gave
algorithm numbers 4, 1 and 3 as above.
Client: `ssh -o VerifyHostKeyDNS=yes host.example.com` (or in ssh_config; the default is `no`). With
`yes` the client implicitly trusts a key that matches a secure fingerprint from DNS; insecure
fingerprints are handled as if the option were `ask`, which shows the match but still makes you
confirm new host keys (ssh_config(5)). On glibc, `/etc/resolv.conf` needs `options edns0 trust-ad`
(glibc 2.31 or later) for the stub resolver to set the AD bit and pass the resolver's AD bit on
(resolv.conf(5)).

## TLSA
Owner `_port._proto.host`:
```
_443._tcp.www.example.com. IN TLSA 3 1 1 <sha256 of SubjectPublicKeyInfo>
_25._tcp.mail.example.com. IN TLSA 3 1 1 <...>
```
| Field | Common values |
|-------|---------------|
| Usage | 3 DANE-EE (pin the server key), 2 DANE-TA (pin your private CA), 1 PKIX-EE, 0 PKIX-TA (acronyms from RFC 7218) |
| Selector | 1 SubjectPublicKeyInfo (survives cert renewal with same key), 0 full cert |
| Matching | 1 SHA-256, 2 SHA-512, 0 exact match on the selected content |
Generate:
```
openssl x509 -in cert.pem -noout -pubkey | openssl pkey -pubin -outform der | sha256sum
```
On a host without `sha256sum`, end the pipe with `openssl dgst -sha256`. Both gave the same digest as
a SubjectPublicKeyInfo hash computed with Python `cryptography` for a test ECDSA certificate.

## Rollover
Publish the new TLSA alongside the old, wait at least TTL x2, then deploy the new key/certificate,
then remove the old record (RFC 7671 section 8.1: add the new records at least two TTLs before the
new chain is deployed). Reversing that order breaks DANE clients (mail delivery stops for
DANE-validating senders).

## Check
```
dig +dnssec _443._tcp.www.example.com TLSA
openssl s_client -connect www.example.com:443 -dane_tlsa_domain www.example.com -dane_tlsa_rrdata "3 1 1 <hex>"
```
The `s_client` check needs no DNS. With OpenSSL 3.2.3 against a local `s_server`, the correct hash
printed `DANE TLSA 3 1 1 ... matched the EE certificate at depth 0`, and an all-zero hash failed with
`verify error:num=65:no matching DANE TLSA records`.

## Verify
- [ ] Records validate with AD set and clients report a DANE/SSHFP match.
