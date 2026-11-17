---
id: computing-software.cryptography-implementation.applied-cryptography.labelled-key-hierarchies-from-a-root-key
name: labelled-key-hierarchies-from-a-root-key
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, key-derivation, kdf-label-hierarchy, key-hierarchy, hkdf, domain-separation, crypto-kdf, multi-tenant]
level: advanced
status: docs-checked
description: "Design a labelled key hierarchy from one root key: label grammar, versioning, per-tenant subkeys, rotation and blast radius, with HKDF or crypto_kdf."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-7.1", "https://doc.libsodium.org/key_derivation", "https://csrc.nist.gov/pubs/sp/800/108/r1/upd1/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Labelled key hierarchies from one root key

Deriving many keys from one root (instead of storing each) keeps storage
small and makes key purpose explicit. The design work is the label scheme.

## Label grammar

Define a registry and a fixed encoding, for example:

```
label = "acme/" + version + "/" + purpose + "/" + scope
        "acme/v1/field-enc/tenant:8812"
        "acme/v1/blind-index/tenant:8812/email"
        "acme/v1/token-mac/global"
```

- Labels are constants in code plus validated ids; never raw user input.
- Length-prefix variable components (or forbid the separator) so
  `tenant:1` + `2/x` cannot collide with `tenant:12` + `/x`.
- Put the version first so a new hierarchy never overlaps the old one.

## Derivation

```python
def subkey(root: bytes, label: str) -> bytes:
    return HKDF(hashes.SHA256(), 32, salt=None, info=label.encode()).derive(root)
```

libsodium: `crypto_kdf_derive_from_key(sub, 32, subkey_id, "fieldenc", root)`
takes an 8-character context, a 64-bit subkey id and subkeys of 16 to 64 bytes.
The libsodium page says up to 2^64 subkeys can be derived, but with 128-bit
subkeys it is not safe to derive more than 2^48 from the same key. Contexts
need not be secret; their purpose is to separate domains and mitigate accidental
bugs.

Worked examples of labelled derivation in standards: TLS 1.3 (RFC 8446 section
7.1) defines `HKDF-Expand-Label(Secret, Label, Context, Length)` over an
`HkdfLabel` structure holding the length, the label prefixed with "tls13 " and
a context; SP 800-108 KDFs take a Label (a string identifying the purpose of the
derived keying material), a Context (which may include party identities) and
the output length L, separated by a 0x00 octet in the fixed input data.

## Structure and blast radius

- Root key lives in a KMS/HSM; derive intermediate keys there or in a narrow
  service, and give applications only the leaf keys they need.
- Anyone holding a key can derive every descendant. Put trust boundaries
  (tenants, environments) at separate roots or separate KMS keys when a
  compromise of one must not expose the other.
- Do not derive keys of different algorithms from the same label.

## Rotation

- Rotating the root changes every derived key: store `root_version` with each
  ciphertext and keep old roots decrypt-only until data is re-encrypted.
- Rotating one leaf: bump its label version (`/v2/`) without touching the root.

## Verify

- [ ] Label registry is in code with a unit test asserting uniqueness.
- [ ] Ciphertexts record root version and label version.
- [ ] Applications never receive the root key.

## Checked

Confirmed from RFC 8446 section 7.1 (HKDF-Expand-Label and HkdfLabel structure), the libsodium Key derivation page (crypto_kdf context, subkey id, size limits, domain-separation purpose) and the SP 800-108 Rev. 1 PDF (Label, Context, L and the 0x00 separator). The label grammar, blast-radius and rotation sections are design guidance rather than documented facts and were left as practice advice, with no figures.

Method: docs-checked 2026-11-09 against RFC 8446 text, SP 800-108 Rev. 1 PDF and the libsodium key derivation page.
