---
id: computing-software.cryptography-implementation.key-management.aws-kms-cli-operations
name: aws-kms-cli-operations
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, aws-kms-cli, aws-kms, aws-cli, envelope-encryption, generate-data-key, encryption-context, cloud-kms]
level: practitioner
status: docs-checked
description: "Run AWS KMS create-key, alias, encrypt, decrypt, generate-data-key, re-encrypt and key-policy checks from the CLI with correct base64 and context handling."
sources: ["https://docs.aws.amazon.com/cli/latest/reference/kms/", "https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html", "https://docs.aws.amazon.com/kms/latest/developerguide/programming-encryption.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS KMS CLI operations

## Create and name a key
```
aws kms create-key --description "orders DEK wrapping" --key-spec SYMMETRIC_DEFAULT --key-usage ENCRYPT_DECRYPT \
  --tags TagKey=owner,TagValue=payments
aws kms create-alias --alias-name alias/orders --target-key-id <key-id>
aws kms enable-key-rotation --key-id alias/orders
```

## Encrypt / decrypt small secrets (max 4096 bytes plaintext)
```
aws kms encrypt --key-id alias/orders --plaintext fileb://secret.bin \
  --encryption-context app=orders,env=prod --query CiphertextBlob --output text | base64 -d > secret.enc
aws kms decrypt --ciphertext-blob fileb://secret.enc --encryption-context app=orders,env=prod \
  --query Plaintext --output text | base64 -d > secret.out
```
- `fileb://` passes raw bytes.
- Output fields are base64; decode them.

## Envelope encryption
```
aws kms generate-data-key --key-id alias/orders --key-spec AES_256 --encryption-context app=orders > dk.json
# use Plaintext (base64) as the AES key locally, store CiphertextBlob next to the data, discard Plaintext
aws kms generate-data-key-without-plaintext ...   # for a component that only stores, never encrypts
```

## Re-encrypt under a new key without seeing plaintext
```
aws kms re-encrypt --ciphertext-blob fileb://secret.enc --destination-key-id alias/orders-v2 \
  --source-encryption-context app=orders,env=prod --destination-encryption-context app=orders,env=prod
```

## Inspect
```
aws kms describe-key --key-id alias/orders
aws kms get-key-policy --key-id alias/orders --policy-name default --output text
aws kms list-grants --key-id alias/orders
```

## Gotchas
- A wrong encryption context makes decrypt fail; check it before suspecting corrupt data.
- Encryption context is not secret or encrypted and appears in plaintext in CloudTrail logs: never put sensitive data in it.
- Use data keys for bulk work rather than calling Encrypt per record.

## Verify
- [ ] Decrypt with a different context fails.
- [ ] CloudTrail shows Encrypt/Decrypt events with the expected context.

## Checked

2026-10-31. Confirmed: all 11 CLI commands and flags (check_commands), Encrypt plaintext limit 1-4096 bytes (botocore model), encryption context logged in plaintext in CloudTrail (KMS encryption context page). Removed: CLI v2 base64 behaviour, Decrypt key-id note, exception and throttle names.
Method: documentation only; no commands were run.
