---
id: computing-software.cryptography-implementation.crypto-libraries.pyca-x509-verification-api
name: pyca-x509-verification-api
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, pyca-x509-verification, pyca-cryptography, python, x509, path-validation, policybuilder, certificate-validation]
level: practitioner
status: verified
description: "Validate certificate chains in Python with cryptography.x509.verification: Store, PolicyBuilder, server and client verifiers, time and depth settings, and limits."
sources: ["https://cryptography.io/en/latest/x509/verification/", "https://www.rfc-editor.org/rfc/rfc5280#section-6", "https://cabforum.org/working-groups/server/baseline-requirements/documents/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pyca X.509 verification API

cryptography 42.0+ (changelog) ships a Rust path validator for CA/B Forum-style WebPKI validation.

## Server certificate
```python
from cryptography import x509
from cryptography.x509.verification import PolicyBuilder, Store, VerificationError
import datetime

store = Store(x509.load_pem_x509_certificates(open("roots.pem", "rb").read()))
verifier = (PolicyBuilder()
            .store(store)
            .time(datetime.datetime.now(datetime.timezone.utc))
            .max_chain_depth(4)
            .build_server_verifier(x509.DNSName("api.example.com")))
leaf = x509.load_pem_x509_certificate(open("leaf.pem", "rb").read())
intermediates = x509.load_pem_x509_certificates(open("chain.pem", "rb").read())
try:
    chain = verifier.verify(leaf, intermediates)        # list: leaf ... root
except VerificationError as e:
    reject(str(e))
```
`x509.IPAddress(ipaddress.ip_address("10.0.0.5"))` for IP SANs. `max_chain_depth` counts intermediates (0 means the leaf is issued directly by a store member; a chain with one intermediate passed with a limit of 2).

## Client certificates
`PolicyBuilder().store(store).build_client_verifier()` (cryptography 43.0+ per the changelog) returns a verifier whose result (`VerifiedClient`) has `.subjects` (the leaf's SANs, e.g. an `RFC822Name`) and `.chain`, so you can authorise by SAN. A leaf with only `serverAuth` EKU is rejected ("required EKU not found").

## What it checks
Chain building to the store, signatures, validity at the given time, basicConstraints and path length, key usage /
EKU for serverAuth or clientAuth, name constraints, SAN matching, and WebPKI profile rules (it is strict: malformed
private CA certificates may fail; a small test CA with SKI but no AKI on the CA certificates passed).

## What it does not do
The API takes no CRL or OCSP input, and it does not fetch missing intermediates (verification failed with "candidates exhausted" when the intermediate was not supplied); supply intermediates yourself.

## Verify
- [ ] Expired, wrong-name and wrong-EKU test certificates raise `VerificationError`.
- [ ] Private CA certificates pass (fix profile issues such as missing AKI/SKI if they do not).
