---
id: computing-software.cloud-infrastructure-engineering.terraform.kms-ciphertext-with-aws-kms-secrets
name: kms-ciphertext-with-aws-kms-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, kms-secrets, aws-kms, secrets-management, ciphertext, sensitive-data]
level: practitioner
status: docs-checked
description: "Commit KMS-encrypted ciphertext instead of plaintext secrets and decrypt at plan time with aws_kms_secrets, including encryption context, IAM, and the state caveat."
sources: ["https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/kms_secrets.html.markdown", "https://docs.aws.amazon.com/cli/latest/reference/kms/encrypt.html", "https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS ciphertext with `aws_kms_secrets`

## Encrypt once (outside Terraform)
```bash
aws kms encrypt \
  --key-id alias/terraform-secrets \
  --plaintext fileb://<(printf '%s' "$DB_PASSWORD") \
  --encryption-context app=payments,env=prod \
  --query CiphertextBlob --output text > secrets/db_password.prod.enc
```
Commit the base64 ciphertext file. A trailing newline in the plaintext is decrypted
intact and breaks passwords, so avoid it (`printf '%s'`, or `echo -n`).

## Decrypt in Terraform
```hcl
data "aws_kms_secrets" "db" {
  secret {
    name    = "db_password"
    payload = trimspace(file("${path.module}/secrets/db_password.${var.env}.enc"))
    context = { app = "payments", env = var.env }
  }
}
resource "aws_db_instance" "main" {
  # ...
  password = data.aws_kms_secrets.db.plaintext["db_password"]
}
```
`plaintext` is a map keyed by each `secret` `name`. With an asymmetric KMS key, also
set `encryption_algorithm` (and `key_id`) on the `secret` block, using the algorithm
you encrypted with.

## IAM
The plan/apply role needs permission to decrypt with the key. The `context` you pass
must match the encryption context used at encrypt time; see the KMS concepts page on
encryption context for using it to scope access.

## Caveats
- The provider docs warn that this data source conceals secrets in configuration but
  does not protect them in Terraform logging and state output. The decrypted value is
  stored in **state**; protect state.
- Rotation: re-encrypt and commit; rotate the actual credential too if the old
  plaintext may have leaked.

## Verify
- [ ] Repository contains only ciphertext.
- [ ] Dev role gets AccessDenied decrypting prod ciphertext.

## Checked
2026-10-31. Confirmed against the aws provider `aws_kms_secrets` documentation (raw GitHub, because the registry page is a stub) and the AWS CLI `kms encrypt` page: `secret` block arguments (`name`, `payload`, `context`, `encryption_algorithm`, `key_id`), `plaintext` map attribute, base64 payload from CiphertextBlob, `--encryption-context`, `--query CiphertextBlob --output text`, trailing-newline warning, state caveat. Removed: the `kms:Decrypt` condition-key example, the sensitive/redacted claim, the SOPS comparison and the write-only/ephemeral suggestion.
Method: documentation only; no commands were run.
