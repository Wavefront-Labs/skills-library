---
id: computing-software.cryptography-implementation.crypto-libraries.pyca-pkcs12-and-pkcs7-serialization
name: pyca-pkcs12-and-pkcs7-serialization
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, pyca-pkcs12, pyca-pkcs7, python, pkcs12, pkcs7, pyca-cryptography]
level: practitioner
status: verified
description: "Load and build PKCS#12 and PKCS#7 with pyca/cryptography: load_key_and_certificates, serialize_key_and_certificates with modern encryption, and PKCS7 signing."
sources: ["https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#pkcs12", "https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#pkcs7"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pyca PKCS#12 and PKCS#7

## Load PKCS#12
```python
from cryptography.hazmat.primitives.serialization import pkcs12
key, cert, extra = pkcs12.load_key_and_certificates(data, b"password")
p12 = pkcs12.load_pkcs12(data, b"password")      # friendly names: p12.cert.friendly_name
```
A bundle written by `openssl pkcs12 -legacy` (RC2/3DES) loaded on 50.0.2 with the bundled OpenSSL; a certificate-only bundle returns `None` for the key, so read the certificate from the third return value (`additional_certs`).

## Build PKCS#12
```python
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import PrivateFormat
enc = (PrivateFormat.PKCS12.encryption_builder()
       .kdf_rounds(50000)
       .key_cert_algorithm(pkcs12.PBES.PBESv2SHA256AndAES256CBC)
       .hmac_hash(hashes.SHA256())
       .build(b"password"))
blob = pkcs12.serialize_key_and_certificates(b"api-server", key, cert, [intermediate], enc)
```
Use `PBESv1SHA1And3KeyTripleDESCBC` (with `hmac_hash(hashes.SHA1())`) only for consumers that cannot read the AES default; the pyca docs warn that with OpenSSL 3.0+ defaults some versions of Windows and macOS cannot read the new format, and that PKCS#12 encryption is not a security mechanism, so wrap the blob if you need confidentiality. Both variants built and reloaded on 50.0.2; `PBES` has exactly these two members.

## PKCS#7
```python
from cryptography.hazmat.primitives.serialization import pkcs7
certs = pkcs7.load_pem_pkcs7_certificates(p7b)     # or load_der_pkcs7_certificates
sig = (pkcs7.PKCS7SignatureBuilder().set_data(msg)
       .add_signer(cert, key, hashes.SHA256())
       .sign(serialization.Encoding.SMIME, [pkcs7.PKCS7Options.DetachedSignature]))
```
The `pkcs7` module has no signature-verification function (checked), only loading of certificates, signing, encryption and decryption; use OpenSSL `cms -verify` or another library to verify.

## Verify
- [ ] Generated P12 imports into the actual target (for example `keytool -list` or `certutil -dump`; not run here) with the chain intact.
