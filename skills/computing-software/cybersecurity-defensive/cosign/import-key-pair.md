---
id: computing-software.cybersecurity-defensive.cosign.import-key-pair
name: import-key-pair
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, import-key-pair, pem, rsa, ec-private-key]
level: practitioner
status: docs-checked
description: "Import a PEM-encoded RSA or EC private key into cosign format with import-key-pair, output prefix, overwrite prompt and password handling."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_import-key-pair.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# import-key-pair

```
cosign import-key-pair --key openssl.key --output-key-prefix my-key
```

Imports "a PEM-encoded RSA or EC private key for signing".

Flags:
- `-k, --key` the key to import.
- `-o, --output-key-prefix` name of outputs; default `import-cosign`, so you get `import-cosign.key` and `import-cosign.pub` (or `my-key.key` and `my-key.pub` with the prefix above).
- `-y, --yes` skip the prompt about overwriting an existing key.

Password: the command prompts interactively; set `COSIGN_PASSWORD` to supply one.

After import:
```
cosign sign --key my-key.key <IMAGE DIGEST>
cosign verify --key my-key.pub <IMAGE>
```

Gotchas:
- RSA keys can be imported, but cosign generates only ECDSA P-256 itself (README); verifiers must support the key type.
- Keep the default prefix in mind: it differs from generate-key-pair's `cosign`.

## Checked

2026-11-04. Confirmed on the cosign import-key-pair reference page (description, examples, `-k`, `-o` default import-cosign, `-y` overwrite prompt, COSIGN_PASSWORD caveat) and the README statement that cosign only generates ECDSA-P256 keys. Removed: the advice about the original PEM file.

Method: documentation only; no commands were run.
