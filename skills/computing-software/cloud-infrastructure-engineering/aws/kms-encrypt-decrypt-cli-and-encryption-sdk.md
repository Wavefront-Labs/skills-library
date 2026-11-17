---
id: computing-software.cloud-infrastructure-engineering.aws.kms-encrypt-decrypt-cli-and-encryption-sdk
name: kms-encrypt-decrypt-cli-and-encryption-sdk
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kms, encryption-sdk, kms-encrypt-decrypt, envelope-encryption, encryption-context]
level: advanced
status: docs-checked
description: "Encrypt and decrypt with aws kms encrypt/decrypt (fileb, base64, 4 KB limit) and the AWS Encryption SDK for envelope encryption of larger data."
sources: ["https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/crypto-cli-install.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/crypto-cli-examples.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/crypto-cli-reference.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/python-example-code.html", "https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-parameters-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS encrypt/decrypt from the CLI and the Encryption SDK

## 1. Small payloads (up to 4,096 bytes) with KMS directly
```bash
aws kms encrypt --key-id alias/app/prod --plaintext fileb://token.txt \
  --encryption-context purpose=api-token --output text --query CiphertextBlob | base64 --decode > token.enc
aws kms decrypt --ciphertext-blob fileb://token.enc --encryption-context purpose=api-token \
  --output text --query Plaintext | base64 --decode
```
- CLI v2 treats blob args as base64; use `fileb://` for raw bytes or `--cli-binary-format raw-in-base64-out`.
- Output is base64 in JSON, hence the `base64 --decode`.
- Decrypt fails with `InvalidCiphertextException` if the encryption context differs.

## 2. Larger data: envelope encryption via the Encryption SDK CLI
```bash
pip install aws-encryption-sdk-cli
aws-encryption-cli --encrypt --input report.csv --output . \
  --wrapping-keys key=arn:aws:kms:<REGION>:<ACCOUNT_ID>:key/<KEY_ID> \
  --encryption-context dept=finance --metadata-output metadata.txt \
  --commitment-policy require-encrypt-require-decrypt
aws-encryption-cli --decrypt --input report.csv.encrypted --output . \
  --wrapping-keys key=arn:aws:kms:<REGION>:<ACCOUNT_ID>:key/<KEY_ID> \
  --encryption-context dept=finance --metadata-output metadata-dec.txt \
  --commitment-policy require-encrypt-require-decrypt --max-encrypted-data-keys 1 --buffer
```
The documented examples use `--output .` (write to the current directory); the encrypted file gets a suffix (`.encrypted` in the docs example, configurable with `--suffix`). Decrypt checks that the encrypted message contains the encryption context you pass. `--commitment-policy` is required for `--wrapping-keys` in 1.8.x and optional but recommended from 2.1.x. The SDK encrypts each message with a unique data key and stores the encrypted data key in the message. Confirm the output file names on your CLI version.

## 3. In code (Python)
The current Python docs build a client with `aws_encryption_sdk.EncryptionSDKClient(commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT)` (this is also the default), create a KMS keyring from a boto3 KMS client, then call `client.encrypt(source=..., keyring=..., encryption_context=...)` and `client.decrypt(source=ciphertext, keyring=..., encryption_context=...)`. Keyrings need the optional Cryptographic Material Providers library, which requires Python 3.11 or later; master key providers belong to earlier versions and the docs describe how to migrate. Follow the "Encrypting and decrypting strings" example in the Python section of the Encryption SDK guide for the exact keyring construction, and use an explicit key ARN rather than a discovery configuration. Verify the encryption context on the decrypted message.

## Gotchas
- AWS KMS does not support decrypting KMS ciphertext outside KMS, and Encryption SDK messages are a different format; use the matching tool for each.
- KMS applies request quotas; see the request quotas page before designing high-volume direct encrypt calls.

## Verify
- [ ] Round-trip decrypt reproduces the original file (`cmp`).
- [ ] Decrypting with a wrong encryption context fails.

## Checked
2026-10-27. Documentation: AWS Encryption SDK Developer Guide (CLI install, CLI examples and reference, Python examples) and AWS CLI User Guide (blob parameters), and the Encrypt and PutKeyPolicy API model documentation for KMS, read this date. Confirmed: pip package aws-encryption-sdk-cli, encrypt/decrypt flags (--wrapping-keys key=, --encryption-context, --metadata-output, --commitment-policy, --max-encrypted-data-keys, --buffer, --output, --suffix), output behaviour, fileb:// raw binary and cli-binary-format semantics, Encrypt limit of 4,096 bytes for symmetric keys, InvalidCiphertextException on encryption context mismatch, EncryptionSDKClient and keyring-based encrypt/decrypt in Python and the Python 3.11 requirement for the MPL. Removed the master-key-provider code (older API), the AES-GCM claim and the stdin metadata output option.
Method: documentation only; no commands were run.
