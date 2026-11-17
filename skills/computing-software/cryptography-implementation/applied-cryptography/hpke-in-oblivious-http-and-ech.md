---
id: computing-software.cryptography-implementation.applied-cryptography.hpke-in-oblivious-http-and-ech
name: hpke-in-oblivious-http-and-ech
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ohttp, oblivious-http, rfc-9458, encrypted-client-hello, ech, hpke, key-config, relay, privacy]
level: advanced
status: docs-checked
description: "Implement or debug HPKE inside Oblivious HTTP (RFC 9458) key configs and encapsulation, and Encrypted Client Hello configs, including key rotation."
sources: ["https://www.rfc-editor.org/rfc/rfc9458", "https://datatracker.ietf.org/doc/rfc9849/", "https://www.rfc-editor.org/rfc/rfc9180"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPKE in Oblivious HTTP and ECH

## Oblivious HTTP (RFC 9458)
Roles: client, relay, gateway, target resource (RFC 9458 calls them Client, Oblivious Relay Resource, Oblivious Gateway Resource and Target Resource).

**Key configuration** (served as `application/ohttp-keys`):
`key_id (8 bits) || kem_id (2) || public_key || symmetric_algorithms_length (2) || [kdf_id (2) aead_id (2)]...`

**Request encapsulation:**
```
hdr  = key_id || kem_id || kdf_id || aead_id
info = "message/bhttp request" || 0x00 || hdr
enc, ctx = SetupBaseS(pkR, info)
ct = ctx.Seal("", binary_http_request)
message/ohttp-req body = hdr || enc || ct
```
**Response:** gateway exports `secret = ctx.Export("message/bhttp response", Nk)`, picks a random
`response_nonce` (max(Nn, Nk) bytes), derives `prk = Extract(enc || response_nonce, secret)`, `aead_key`/`aead_nonce`
with Expand labels "key"/"nonce", and returns `response_nonce || Seal(aead_key, aead_nonce, "", response)`.

**Operations:**
- Regular rotation of server keys limits the messages affected by a key compromise, and more than one configuration
  may need to be active during rotation. Each active configuration partitions the client anonymity set, so give every
  client the same config and use a consistency mechanism (RFC 9458 points to a key-consistency draft).
- A gateway returns an error when `key_id` does not match a key of the stated `kem_id`.

## Encrypted Client Hello
- The server publishes an `ECHConfigList` (RFC 9849 mentions HTTPS DNS records as a delivery mechanism). Each
  ECHConfig carries an HPKE public key, cipher suites and a `public_name`.
- Client encrypts the inner ClientHello with HPKE base mode, `info = "tls ech" || 0x00 || ECHConfig`; the outer
  ClientHello shows only `public_name`.
- A server can return `retry_configs` (an `ECHConfigList`) so clients with stale configs can recover.

## Verify
- [ ] OHTTP request/response round trip passes RFC 9458 Appendix A test vector.
- [ ] Stale key_id produces a clean error, not a crash; rotation overlap tested.
- [ ] ECH: the outer ClientHello carries `public_name`, not the inner server name.

## Checked
2026-11-01. Confirmed in RFC 9458: roles, key config and media types (`application/ohttp-keys`, `message/ohttp-req`),
request `hdr`/`info`/Seal with empty AAD, response export label, `response_nonce` length, Extract/Expand labels
("key", "nonce"), rotation and anonymity-set text, Appendix A example. Confirmed in RFC 9849 (the ECH specification
the old draft link now points to): `ECHConfigList`, `public_name`, `retry_configs`, HPKE info `"tls ech" || 0x00 ||
ECHConfig`. Removed: DNS parameter name, ECH rotation timing, relay/gateway logging advice.
Method: documentation only; no commands were run.
