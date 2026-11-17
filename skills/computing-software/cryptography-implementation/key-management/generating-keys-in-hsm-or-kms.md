---
id: computing-software.cryptography-implementation.key-management.generating-keys-in-hsm-or-kms
name: generating-keys-in-hsm-or-kms
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-generation, hsm-key-generation, pkcs11, c-generatekeypair, aws-kms, cloud-kms, key-attestation, non-extractable-keys]
level: advanced
status: docs-checked
description: "Generate keys inside an HSM or cloud KMS with the right attributes from the start: PKCS#11 templates, KMS key specs and usage, attestation, and why import is second best."
sources: ["https://docs.oasis-open.org/pkcs11/pkcs11-spec/v3.1/os/pkcs11-spec-v3.1-os.html", "https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html", "https://cloud.google.com/kms/docs/attest-key"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating keys inside an HSM or KMS

A key generated inside an HSM with non-extractable attributes has never existed
in plaintext outside the boundary. Importing a key generated elsewhere loses
that property forever, because a copy may exist. Generate inside unless you
must interoperate with an existing key.

## PKCS#11 template (attributes are set at birth)

```c
CK_BBOOL t = CK_TRUE, f = CK_FALSE;
CK_ATTRIBUTE pub[] = {
  {CKA_TOKEN,&t,1},{CKA_VERIFY,&t,1},{CKA_EC_PARAMS,p256_oid,sizeof p256_oid},
  {CKA_LABEL,"sign-2026",9}};
CK_ATTRIBUTE prv[] = {
  {CKA_TOKEN,&t,1},{CKA_PRIVATE,&t,1},{CKA_SENSITIVE,&t,1},
  {CKA_EXTRACTABLE,&f,1},{CKA_SIGN,&t,1},{CKA_DECRYPT,&f,1},{CKA_DERIVE,&f,1},
  {CKA_LABEL,"sign-2026",9},{CKA_ID,id,idlen}};
CK_MECHANISM m = {CKM_EC_KEY_PAIR_GEN, NULL, 0};
C_GenerateKeyPair(h, &m, pub, 4, prv, 9, &hpub, &hprv);
```

- `CKA_SENSITIVE=TRUE` and `CKA_EXTRACTABLE=FALSE` cannot be reversed later
  (they are one-way by spec); set them now.
- Restrict usage flags to one purpose (`CKA_SIGN` only, not also `CKA_DECRYPT`).
- `CKA_TOKEN=TRUE` makes it persistent; session objects vanish at logout.
- Same `CKA_ID` on public and private objects so tools (pkcs11-tool, OpenSSL
  pkcs11 provider) can pair them.

Read the attributes back after generation and confirm them (sensitive, non-extractable, single usage).

## Cloud KMS

```bash
aws kms create-key --key-spec ECC_NIST_P256 --key-usage SIGN_VERIFY \
  --description "release signing 2026" --origin AWS_KMS
gcloud kms keys create sign-2026 --keyring ring --location global \
  --purpose asymmetric-signing --default-algorithm ec-sign-p256-sha256 --protection-level hsm
```

In AWS KMS, key spec, key usage and key material origin cannot be changed after creation; plan them. Use
`--protection-level hsm` (Cloud KMS) or a CloudHSM-backed custom key store (AWS) when policy requires an HSM.

## Attestation

Prove to auditors (or relying parties) the key was generated in hardware and
is non-exportable: Google Cloud KMS can attest HSM-protected keys (see its attest-key page); other vendors
have their own attestation formats. Store the attestation with the key record.

## Verify

- [ ] Private key attributes show sensitive=true, extractable=false, single usage.
- [ ] Key origin is the HSM/KMS (not EXTERNAL) unless import was justified.
- [ ] Attestation retrieved and verified against the vendor root.

## Checked

2026-11-01. Confirmed: `aws kms create-key` and `gcloud kms keys create` flags (check_commands), AWS KMS key spec,
key usage and origin are immutable and origin values include `AWS_KMS` and `EXTERNAL`, `AWS_CLOUDHSM` key stores
(create-keys page), PKCS #11 `CKA_SENSITIVE`/`CKA_EXTRACTABLE` semantics (v3.1), Cloud KMS attestation page.
Removed: pkcs11-tool commands, FIPS level wording, Azure/YubiHSM/Luna/nShield/TPM attestation list.
Method: documentation only; no commands were run.
