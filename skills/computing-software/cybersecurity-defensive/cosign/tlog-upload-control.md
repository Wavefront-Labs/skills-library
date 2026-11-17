---
id: computing-software.cybersecurity-defensive.cosign.tlog-upload-control
name: tlog-upload-control
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, tlog-upload, record-creation-timestamp, rekor, transparency-log]
level: practitioner
status: docs-checked
description: "Control Rekor uploads with cosign sign --tlog-upload and --record-creation-timestamp, and the verify-side consequences of private or unlogged signatures."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transparency log upload

The sign docs give these examples:

```
cosign sign --key cosign.key <IMAGE DIGEST>                        # sign and upload to the transparency log
cosign sign --key cosign.key --tlog-upload=false <IMAGE DIGEST>   # skip uploading to the transparency log
cosign sign --key cosign.key --record-creation-timestamp <IMAGE DIGEST>   # honor the creation timestamp of the signature
```

Verify side: `--insecure-ignore-tlog` is described as "ignore transparency log verification, to be used when an artifact signature has not been uploaded to the transparency log. Artifacts cannot be publicly verified when not included in a log".

README, keyless prompt: the information (which may include the email address of the account you authenticate with) is stored in public transparency logs and cannot be removed later.

Separate flag: `--upload` is "whether to upload the signature (default true)"; it is distinct from `--tlog-upload`.

## Checked

2026-11-04. Confirmed against the cosign sign and verify docs and the README keyless prompt: the three sign examples and their comments, `--insecure-ignore-tlog` text, the log-permanence warning, `--upload` text. Removed: the claim that a key signature uploads by default beyond what the example comment says, the claim that `--upload=false` pushes to the registry specifically (the page says only "upload the signature"), and a cross-reference to a verify-signed-timestamps skill.
Method: documentation only; no commands were run.
