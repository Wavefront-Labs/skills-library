---
id: computing-software.cryptography-implementation.crypto-libraries.go-crypto-x509-verification-options
name: go-crypto-x509-verification-options
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, golang, go-crypto, go-x509, certificate-verification, verifyoptions, revocation]
level: advanced
status: verified
description: "Verify certificates in Go with crypto/x509: VerifyOptions roots, intermediates, DNSName and KeyUsages, platform verifiers, SHA-1 and CN rules, and the lack of revocation checks."
sources: ["https://pkg.go.dev/crypto/x509", "https://pkg.go.dev/crypto/tls#Config", "https://pkg.go.dev/golang.org/x/crypto/ocsp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto/x509 verification options (Go)

Use this when you verify certificates outside the TLS handshake (signed documents, client
certificates in a custom protocol, SPIFFE, webhook signatures) or add checks inside
`VerifyConnection`.

## Verify a chain
```go
roots := x509.NewCertPool()
roots.AppendCertsFromPEM(rootPEM)            // returns false if nothing parsed: check it (checked with junk input)
inter := x509.NewCertPool()
for _, c := range intermediates { inter.AddCert(c) }

chains, err := leaf.Verify(x509.VerifyOptions{
    Roots:         roots,                     // nil = system roots
    Intermediates: inter,
    DNSName:       "api.example.com",          // empty = no hostname check
    KeyUsages:     []x509.ExtKeyUsage{x509.ExtKeyUsageClientAuth},
    CurrentTime:   time.Now(),                 // set only for historical verification
})
```
- `KeyUsages` defaults to `ServerAuth`. A client certificate verified with defaults fails with
  `x509: certificate specifies an incompatible key usage`; pass `ClientAuth` (both checked). `ExtKeyUsageAny`
  turns the check off, which is rarely right.
- Per the `VerifyOptions.KeyUsages` docs, a chain is accepted if it allows any of the listed usages; an empty list means `ServerAuth`.
- `chains` lists every valid path; use `chains[0]` for identity, but any is cryptographically valid.

## Rules Go enforces (and you can't turn off in current releases)
- Hostnames come from SANs only; the CN is ignored (a leaf with CN `api.example.com` and SAN `other.example.com` failed
  `DNSName: "api.example.com"`, checked).
- SHA-1 signed certificates are rejected (the `x509sha1` GODEBUG was removed in Go 1.24, per go.dev/doc/godebug).
- Malformed input fails at parse time (`x509.ParseCertificate` and `ParseRevocationList` return errors; `ParseRevocationList([]byte("x"))` did). Name constraints, serial-number limits and duplicate-extension handling are not exercised here; check the `crypto/x509` docs and the GODEBUG history for your Go version.

## Platform verifiers
With `Roots: nil` on macOS and Windows, Go calls the OS verifier (Security.framework, CryptoAPI),
which brings OS trust settings, enterprise roots and some revocation behaviour. On Linux it reads
the system bundle. `SSL_CERT_FILE` / `SSL_CERT_DIR` override the locations (`SystemCertPool` docs); since Go 1.27 setting
either on macOS or Windows also stops the platform APIs being used unless `GODEBUG=x509sslcertoverrideplatform=0`.
Behaviour can differ between platforms; test where you deploy.

## Revocation is your job
`Verify` does not check CRLs or OCSP. Options:
- OCSP: `golang.org/x/crypto/ocsp` to build a request, fetch from the AIA URL, `ocsp.ParseResponseForCert`,
  then check `Status`, `ThisUpdate`/`NextUpdate`.
- CRL: `x509.ParseRevocationList` and check the serial, after verifying the CRL signature with
  `rl.CheckSignatureFrom(issuer)`.
- Prefer short-lived certificates so revocation matters less.

## Other useful calls
- `leaf.VerifyHostname(name)` alone (after chain verification).
- `x509.ParseCertificate`/`ParseCertificates` for DER; `pem.Decode` loops for PEM bundles.
- `cert.CheckSignatureFrom(parent)` checks one link only; never use it as a substitute for `Verify`.

## Verify
- [ ] Tests: wrong root (`certificate signed by unknown authority`), expired leaf (`certificate has expired or is not yet valid`),
      wrong EKU and wrong hostname each fail (all four checked).
- [ ] `AppendCertsFromPEM` return value is checked.
- [ ] Revocation (or short lifetimes) is handled explicitly for client-certificate auth.
