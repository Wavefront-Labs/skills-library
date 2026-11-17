---
id: computing-software.cryptography-implementation.crypto-libraries.pyca-building-certificates-and-csrs
name: pyca-building-certificates-and-csrs
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, python, pyca-cryptography, pyca-x509, x509, csr, certificate-builder]
level: practitioner
status: verified
description: "Build CSRs and certificates in Python with CertificateSigningRequestBuilder and CertificateBuilder: SANs, critical extensions, serials, validity and verifying the result."
sources: ["https://cryptography.io/en/latest/x509/tutorial/", "https://cryptography.io/en/latest/x509/reference/", "https://www.rfc-editor.org/rfc/rfc5280"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building certificates and CSRs in Python (pyca/cryptography)

## CSR
```python
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

key = ec.generate_private_key(ec.SECP256R1())
csr = (x509.CertificateSigningRequestBuilder()
       .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "api.example.com")]))
       .add_extension(x509.SubjectAlternativeName([x509.DNSName("api.example.com")]), critical=False)
       .sign(key, hashes.SHA256()))
pem = csr.public_bytes(serialization.Encoding.PEM)
assert csr.is_signature_valid
```
Always add a SAN: RFC 9525 says the Common Name must not be used to identify a service, and the pyca verifier rejects a leaf with no matching SAN even when the CN matches (checked).

## Certificate signed by a private CA
```python
import datetime as dt
now = dt.datetime.now(dt.timezone.utc)
cert = (x509.CertificateBuilder()
    .subject_name(csr.subject)
    .issuer_name(ca_cert.subject)
    .public_key(csr.public_key())
    .serial_number(x509.random_serial_number())          # 159 bits at most (checked), positive
    .not_valid_before(now - dt.timedelta(minutes=5))      # allow clock skew
    .not_valid_after(now + dt.timedelta(days=90))
    .add_extension(csr.extensions.get_extension_for_class(x509.SubjectAlternativeName).value, critical=False)
    .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
    .add_extension(x509.KeyUsage(digital_signature=True, key_encipherment=False, content_commitment=False,
        data_encipherment=False, key_agreement=False, key_cert_sign=False, crl_sign=False,
        encipher_only=False, decipher_only=False), critical=True)
    .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
    .add_extension(x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False)
    .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_cert.public_key()), critical=False)
    .sign(ca_key, hashes.SHA256()))
```
- Copy only the CSR extensions you approve (SAN); never blindly copy all requested extensions,
  or a requester can ask for `BasicConstraints(ca=True)`.
- Ed25519/Ed448 CA keys: pass `algorithm=None` to `sign` (passing `hashes.SHA256()` raises `ValueError`; checked).
- A CA certificate needs `BasicConstraints(ca=True, path_length=0)` and `KeyUsage(key_cert_sign=True, crl_sign=True)`.

## Verify what you built
```python
from cryptography.x509.verification import PolicyBuilder, Store
verifier = PolicyBuilder().store(Store([root])).build_server_verifier(x509.DNSName("api.example.com"))
chain = verifier.verify(cert, [intermediate])             # 42.0+ per the changelog, raises VerificationError
```
`cert.verify_directly_issued_by(ca_cert)` (40.0+ per the changelog) checks only the signature and issuer name. Both calls and `openssl verify -CAfile root.pem -untrusted inter.pem leaf.pem` accepted a chain built exactly as above.

## Verify
- [ ] `openssl x509 -text -noout` shows the SAN, critical BasicConstraints and KeyUsage.
- [ ] The issued cert validates with the PolicyBuilder verifier and with `openssl verify`.
- [ ] Unapproved CSR extensions are dropped.
