---
id: computing-software.cryptography-implementation.protocol-implementation.hpke-secret-export
name: hpke-secret-export
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, hpke, hpke-exporter, export-only, key-encapsulation, exporter-context, rfc9180, oblivious-http]
level: advanced
status: docs-checked
description: "Use HPKE's Export() to derive secrets for other keys (response keys, MACs) with exporter contexts, as Oblivious HTTP does, instead of reusing Seal keys."
sources: ["https://www.rfc-editor.org/rfc/rfc9180#section-5.3", "https://www.rfc-editor.org/rfc/rfc9458#section-4.4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPKE secret export

Every HPKE context has an exporter secret. `ctx.Export(exporter_context, L)`
returns L bytes derived with the KDF's Expand from the exporter secret,
independent of the Seal/Open keys. Use it when the encapsulated secret must key
something else.

## Typical uses

- **Response encryption**: the sender encapsulates to the server; the server
  needs to encrypt a reply back without the client having a key pair. Oblivious
  HTTP (RFC 9458 section 4.4) exports `secret = Export("message/bhttp response", max(Nn, Nk))`,
  generates a random `response_nonce` of the same length, extracts with salt
  `enc || response_nonce`, and expands labels "key" and "nonce" to the AEAD
  key and nonce.
- **Export-only usage**: applications that never call Seal can use the
  export-only AEAD id 0xFFFF in the key schedule (RFC 9180 section 5.3).

## Rules

- Use a distinct, descriptive `exporter_context` per derived key. The context
  is an input to LabeledExpand, so different contexts give different outputs;
  its maximum length depends on the KDF (RFC 9180 section 7.2.1).
- `L` has a maximum of 255*Nh for the KDFs in RFC 9180.
- Derive fresh keys from the exported secret through the KDF as RFC 9458
  does, rather than using it directly.
- Both sides call Export after setup; the recipient must have set up the same
  mode with the same `info` or outputs differ.

```text
Client: enc, ctxS = SetupBaseS(pkR, info); ct = ctxS.Seal(aad, req)
        secret = ctxS.Export("example response", max(Nn, Nk))
Server: ctxR = SetupBaseR(enc, skR, info); req = ctxR.Open(aad, ct)
        secret = ctxR.Export("example response", max(Nn, Nk))
        nonce = random(max(Nn, Nk)); prk = Extract(enc || nonce, secret)
        key = Expand(prk, "key", Nk); iv = Expand(prk, "nonce", Nn)
```

## Verify

- [ ] RFC 9180 Appendix A "exported values" vectors pass.
- [ ] Each exported key has a unique exporter context string.
- [ ] Response keys include a fresh server nonce so replays get fresh keys.

## Checked

2026-11-01: RFC 9180 section 5.3 and RFC 9458 section 4.4 read. Confirmed: Export definition, 255*Nh bound, export-only AEAD id 0xFFFF, the OHTTP response derivation steps and lengths. Removed: Noise/TLS PSK bootstrapping claim and the sequence-number collision claim.
Method: documentation only; no commands were run.
