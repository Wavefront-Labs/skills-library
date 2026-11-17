---
id: computing-software.cybersecurity-defensive.cosign.generate-key-pair
name: generate-key-pair
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, generate-key-pair, cosign-password, key-pair, cosign-key]
level: intro
status: docs-checked
description: "Create a cosign key pair with generate-key-pair, set the file prefix, supply the password non-interactively with COSIGN_PASSWORD and what files result."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_generate-key-pair.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# generate-key-pair

```
cosign generate-key-pair
cosign generate-key-pair --output-key-prefix my-name
```

Default output: `cosign.key` and `cosign.pub`. With `--output-key-prefix my-name` you get `my-name.key` and `my-name.pub`.

Caveat from the docs: "This command interactively prompts for a password. You can use the COSIGN_PASSWORD environment variable to provide one."

```
COSIGN_PASSWORD=... cosign generate-key-pair
```

Then:
```
cosign sign --key cosign.key <IMAGE DIGEST>
cosign verify --key cosign.pub <IMAGE>
```

See key-file-format for what is inside and extract-public-key to re-derive a public key.

For keys held in a KMS, Kubernetes, GitHub or GitLab, see key-pair-in-kms. To use an existing key, see import-key-pair.

## Checked

2026-11-04. Confirmed on the cosign generate-key-pair reference page: the examples with default and `--output-key-prefix` file names, the interactive password caveat with COSIGN_PASSWORD, and the KMS, Kubernetes, GitHub and GitLab forms. Removed: that the private key file is encrypted, and the CI and distribution advice (not on the page).

Method: documentation only; no commands were run.
