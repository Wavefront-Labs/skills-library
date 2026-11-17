---
id: computing-software.cryptography-implementation.openssl.certificate-serial-numbers-and-validity
name: certificate-serial-numbers-and-validity
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, certificate-serial-number, validity-period, openssl-ca, cab-forum, x509]
level: practitioner
status: verified
description: "Set certificate serial numbers and validity in OpenSSL CAs: random 64+ bit serials, the serial file, -set_serial pitfalls, -days, -not_before/-not_after and backdating."
sources: ["https://docs.openssl.org/3.0/man1/openssl-ca/", "https://docs.openssl.org/3.0/man1/openssl-x509/", "https://cabforum.org/working-groups/server/baseline-requirements/requirements/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate serial numbers and validity

## Serials
- Must be unique per issuer and positive. CA/Browser Forum Baseline Requirements: at least 64 bits from a CSPRNG
  (7.1). Private CAs should follow the same rule to avoid collisions across reissues or restored databases.
- `openssl ca` reads/increments the `serial` file; initialise it randomly:
  `openssl rand -hex 16 | sed 's/^./7/' > serial` (keeps the top bit clear so the integer stays positive).
- `openssl x509 -req -CA ... -CAcreateserial` writes a `.srl` file seeded with a random serial.
- `-set_serial 1` gives duplicates across runs; avoid outside tests. Duplicate serials from the same issuer
  break revocation and Firefox rejects them (SEC_ERROR_REUSED_ISSUER_AND_SERIAL).

## Validity
```sh
openssl ca -config ca.cnf -in r.csr -days 90 -out c.pem
openssl ca -config ca.cnf -in r.csr -startdate 20261101000000Z -enddate 20270201000000Z -out c.pem
openssl x509 -req -in r.csr -CA ca.pem -CAkey ca.key -not_before 20261101000000Z -not_after 20270130000000Z -out c.pem  # 3.4+
```
- Backdate notBefore by a few minutes to tolerate client clock skew; never months.
- Public TLS certs: max 398 days now, falling to 200 (2026), 100 (2027), 47 days (2029) per CA/B Forum ballot SC-081.
- Leaf validity must not exceed the issuing CA's validity.

## Verify
- [ ] `openssl x509 -noout -serial -dates -in c.pem` shows a long random serial and intended dates.

## Checked
- OpenSSL 3.2.3 mini CA run: random serial recipe, `openssl ca -days` and `-startdate/-enddate`, `x509 -req -CAcreateserial` (random 160-bit `.srl`), and `-set_serial 1` giving serial 01 each time.
- `-not_before`/`-not_after` are rejected on 3.2.3 and appear in the 3.4 `openssl-x509` manual but not the 3.3 one. CA/B Forum BR.md: serial must be below 2^159 with at least 64 bits from a CSPRNG; validity limits 200 days from 2026-03-15, 100 from 2027-03-15, 47 from 2029-03-15.
