---
id: computing-software.cybersecurity-defensive.cosign.extract-public-key
name: extract-public-key
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, extract-public-key, public-key, outfile, kms]
level: intro
status: docs-checked
description: "Get a public key out of a cosign private key, KMS, Vault or URL with cosign public-key and write it to a file or stdout."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_public-key.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign public-key

"Gets a public key from the key-pair and writes to a specified file. By default, it will write to standard out."

```
cosign public-key --key <PRIVATE KEY FILE> --outfile <OUTPUT>
cosign public-key --key https://host.for/<FILE> --outfile <OUTPUT>
cosign public-key --key awskms://[ENDPOINT]/[ID/ALIAS/ARN]
cosign public-key --key gcpkms://projects/[PROJECT]/locations/global/keyRings/[KEYRING]/cryptoKeys/[KEY]
cosign public-key --key azurekms://[VAULT_NAME][VAULT_URI]/[KEY]
cosign public-key --key hashivault://[KEY]
cosign public-key --key gitlab://[OWNER]/[PROJECT_NAME]
```

Use it to publish the verification key for a KMS-held signing key, or to re-derive a public key from a private key file. Other flags: `--sk` and `--slot` for a hardware key. Without `--outfile` the key goes to standard out.

## Checked

2026-11-04. Confirmed on the cosign public-key reference page: the description quote, the examples for key file, URL, AWS, Google Cloud, Azure, Hashicorp Vault and GitLab, and the flags. Removed: the password prompt remark, the PEM header and PKIX format claim and the publishing advice (none on the page). The page's own `--outfile` help text reads "path to a payload file to use rather than generating one", which contradicts its synopsis.

Method: documentation only; no commands were run.
