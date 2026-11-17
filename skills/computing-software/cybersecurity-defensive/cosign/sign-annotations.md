---
id: computing-software.cybersecurity-defensive.cosign.sign-annotations
name: sign-annotations
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, annotations, tag-signing, key-value-claims]
level: practitioner
status: docs-checked
description: "Add signed key=value annotations with cosign sign -a and require them at verify time, including the tag-to-digest mapping pattern."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signature annotations

Sign with extra claims:

```
cosign sign --key cosign.key -a key1=value1 -a key2=value2 <IMAGE DIGEST>
```

Annotations go into the signed payload (Optional section), so the signature protects them.

Require them when verifying:

```
cosign verify --key cosign.pub -a key1=value1 <IMAGE>
```

The verify output in the README shows them under `Optional`.

Tag signing pattern from the README: a signature protects digests, but annotations let you sign a tag-to-digest mapping.

```
cosign sign --key cosign.key -a tag=$TAG $IMAGE_URI_DIGEST
cosign verify --key cosign.pub -a tag=$TAG $IMAGE_URI
```

This checks both that the digest was signed and that the `tag` annotation equals `$TAG`. The README suggests timestamps could be added the same way for TUF-style freeze-attack prevention.

Note the help text for `verify -a` reads "extra key=value pairs to sign"; the README uses it to verify that the annotation has the given value.

## Checked

2026-11-04. Confirmed in the README Tag Signing section (annotations added to the signed payload, tag example, verify with `-a`, Optional output, timestamps remark) and on the cosign sign and verify reference pages (`-a, --annotations`). Removed: the claim that verification fails when an annotation is missing or different.

Method: documentation only; no commands were run.
