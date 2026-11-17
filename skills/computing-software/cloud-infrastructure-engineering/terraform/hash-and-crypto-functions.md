---
id: computing-software.cloud-infrastructure-engineering.terraform.hash-and-crypto-functions
name: hash-and-crypto-functions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, hash-functions, crypto-functions, filemd5, sha256, filebase64sha256, uuid, bcrypt, change-detection]
level: practitioner
status: verified
description: "Use hash functions for change detection and naming (md5, sha256, filemd5, filebase64sha256, uuidv5) and know which crypto functions to avoid (bcrypt, uuid, rsadecrypt)."
sources: ["https://developer.hashicorp.com/terraform/language/functions/filemd5", "https://developer.hashicorp.com/terraform/language/functions/sha256", "https://developer.hashicorp.com/terraform/language/functions/bcrypt", "https://developer.hashicorp.com/terraform/language/functions/uuidv5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash and crypto functions

## Change detection
```hcl
resource "aws_s3_object" "cfg" {
  source = "${path.module}/cfg.json"
  etag   = filemd5("${path.module}/cfg.json")          # re-upload when content changes
}

resource "aws_lambda_function" "fn" {
  filename         = "build/fn.zip"
  source_code_hash = filebase64sha256("build/fn.zip")  # the format Lambda reports
}

resource "terraform_data" "rebuild" {
  triggers_replace = sha256(join("", [for f in fileset("${path.module}/src", "**") : filesha256("${path.module}/src/${f}")]))
}
```
Functions: `md5`, `sha1`, `sha256`, `sha512`, `base64sha256`, `base64sha512`, and
`file*` variants that hash file bytes directly (correct for binaries).

Note: S3 `etag` equals MD5 only for non-multipart, non-KMS uploads; with SSE-KMS use
`source_hash` instead.

## Stable short IDs
```hcl
locals {
  suffix = substr(sha256("${var.project}-${var.env}"), 0, 8)
  id     = uuidv5("dns", "api.${var.domain}")    # deterministic UUID
}
```

## Avoid
| Function | Problem |
|---|---|
| `uuid()` | new value every plan → perpetual diff; use `random_uuid` resource |
| `bcrypt()` | random salt → changes every run; use `random_password.bcrypt_hash` |
| `rsadecrypt()` | needs the private key in config/state; e.g. Windows password decryption — keep out of shared states |

## Gotchas
- MD5/SHA1 for change detection only — not for security.
- `base64sha256(x)` ≠ `base64encode(sha256(x))` (the latter encodes the hex string).
- Hashing large directories on every plan is slow; prefer archive_file hashes.

## Verify
- [ ] Touching a file changes only the resource whose hash depends on it.
- [ ] No `uuid()`/`bcrypt()` in config: `grep -rnE "\buuid\(\)|bcrypt\(" .` is empty.

## Checked
- Terraform 1.9.8 `terraform console` and a local plan: `md5`, `sha1`, `sha256`, `sha512`, `base64sha256`/`base64sha512`; `filemd5`/`filesha256`/`filebase64sha256` equal the string forms; `base64sha256(x)` is not `base64encode(sha256(x))`; `file()` rejects non-UTF-8 content with a message pointing at the hashing functions; `substr(sha256(...), 0, 8)` and `uuidv5` are stable; `uuid()` and `bcrypt()` change on every evaluation; the `terraform_data` `triggers_replace` expression over `fileset` plans. The AWS provider docs describe `etag` (MD5 only for plaintext or AWS-managed-key objects), `source_hash` for the KMS case and Lambda `source_code_hash`. `rsadecrypt` and `archive_file` hashes were not run.
