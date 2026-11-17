---
id: computing-software.cloud-infrastructure-engineering.openbao.transit-encrypt-decrypt
name: transit-encrypt-decrypt
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, transit, encrypt, rotate, rewrap]
level: practitioner
status: docs-checked
description: "Encryption as a service with OpenBao transit: create keys, encrypt and decrypt base64 data, rotate versions and rewrap without plaintext."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/secrets/transit/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit encrypt, decrypt, rotate, rewrap

```
bao secrets enable transit
bao write -f transit/keys/my-key
bao write transit/encrypt/my-key plaintext=$(echo "my secret data" | base64)
bao write transit/decrypt/my-key ciphertext=<ciphertext>
bao write -f transit/keys/my-key/rotate
bao write transit/rewrap/my-key ciphertext=<ciphertext>
```

- Use `-path` to mount elsewhere. Usually one key per application.
- Plaintext must be base64. Ciphertext begins `vault:v1:` where `v1` is the key version used. Decrypt returns base64 to decode.
- Rotate adds a version: new encryptions use it, old data stays decryptable.
- Rewrap re-encrypts to the newest version without exposing plaintext, so a process with only rewrap permission cannot read the data.

## min_decryption_version

Versions below it are archived and generally cannot decrypt. This limits access to obsolete data; lower it in an emergency to restore access.

## Warnings

- API requests are capped at 32MB (tunable per listener).
- Rotate AES-GCM keys before a version reaches about 2^32 encryptions (NIST SP 800-38D); estimate your rate.
- With some backends such as Raft, very frequent rotation can make the archive entry too large; consider time-bounded named keys.
- Importing keys is less secure than letting transit generate them; wrap symmetric keys as raw bytes and asymmetric as PKCS8 DER.

## Checked

2026-11-04. Read the OpenBao transit secrets engine overview page in full. Confirmed: the setup, encrypt, decrypt, rotate and rewrap commands, base64 requirement, the `vault:v1:` ciphertext prefix, rewrap not revealing plaintext, `min_decryption_version` archiving, the 32MB request cap, the NIST 2^32 guidance, Raft archive size caveat and the import advice. Removed: nothing.
Method: documentation only; no commands were run.
