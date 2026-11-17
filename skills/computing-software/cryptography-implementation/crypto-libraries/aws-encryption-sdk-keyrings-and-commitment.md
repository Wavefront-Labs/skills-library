---
id: computing-software.cryptography-implementation.crypto-libraries.aws-encryption-sdk-keyrings-and-commitment
name: aws-encryption-sdk-keyrings-and-commitment
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, aws-encryption-sdk, commitment-policy, committing-algorithm-suites, keyrings, kms-keyring, encryption-context, max-encrypted-data-keys, envelope-encryption]
level: advanced
status: draft
description: "Use the AWS Encryption SDK safely: KMS multi-keyrings, REQUIRE_ENCRYPT_REQUIRE_DECRYPT commitment, encryption context checks, strict mode, max data keys."
sources: ["https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/concepts.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/migrate-commitment-policy.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/configure.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AWS Encryption SDK keyrings and commitment policy

The AWS Encryption SDK (Java, Python, JS, C, .NET, CLI) implements envelope
encryption with a portable message format: a unique data key per message,
wrapped by one or more KMS keys (or raw AES/RSA wrapping keys), with an
encryption context and signatures by default.

## Keyrings

```python
import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy
from aws_cryptographic_material_providers.mpl import AwsCryptographicMaterialProviders
from aws_cryptographic_material_providers.mpl.config import MaterialProvidersConfig
from aws_cryptographic_material_providers.mpl.models import CreateAwsKmsMultiKeyringInput

client = aws_encryption_sdk.EncryptionSDKClient(
    commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT,
    max_encrypted_data_keys=3)
mpl = AwsCryptographicMaterialProviders(MaterialProvidersConfig())
keyring = mpl.create_aws_kms_multi_keyring(CreateAwsKmsMultiKeyringInput(
    generator="arn:aws:kms:eu-west-1:111122223333:key/...",
    kms_key_ids=["arn:aws:kms:eu-central-1:111122223333:key/..."]))   # second region for DR
ct, header = client.encrypt(source=data, keyring=keyring,
                            encryption_context={"tenant": "42", "purpose": "invoice"})
pt, dheader = client.decrypt(source=ct, keyring=keyring)
assert dheader.encryption_context["tenant"] == "42"      # check context on decrypt
```

## Key commitment

Without key commitment, a ciphertext could be crafted to decrypt validly
under two different data keys to two different plaintexts (invisible
salamanders / partitioning attacks on GCM). SDK 2.0+ uses committing
algorithm suites and the commitment policy controls enforcement:

| Policy | Encrypt | Decrypt |
|---|---|---|
| `FORBID_ENCRYPT_ALLOW_DECRYPT` | old suites | anything (migration step 1) |
| `REQUIRE_ENCRYPT_ALLOW_DECRYPT` | committing | old and new (step 2) |
| `REQUIRE_ENCRYPT_REQUIRE_DECRYPT` | committing | committing only (default, target) |

Migrate readers first, then writers, then require on decrypt.

## Other safety settings

- **Strict mode**: decrypt keyrings list explicit KMS key ARNs. "Discovery"
  keyrings decrypt with whatever key the message names - restrict with a
  discovery filter (account ids, partition) if you must use them.
- **max_encrypted_data_keys**: bounds work when decrypting attacker-supplied
  messages with many wrapped keys (DoS); set to your expected count.
- **Encryption context**: not secret (stored in the header, logged in
  CloudTrail); verify expected keys/values after decrypt, or use the required
  encryption context CMM.
- Signing algorithm suites (default) add an ECDSA signature so holders of the
  data key cannot forge messages; disable only for performance when all
  decryptors are also trusted encryptors.

## Verify

- [ ] Commitment policy is `REQUIRE_ENCRYPT_REQUIRE_DECRYPT` everywhere after migration.
- [ ] Decrypt uses strict keyrings or filtered discovery; context checked.
- [ ] `max_encrypted_data_keys` configured.
