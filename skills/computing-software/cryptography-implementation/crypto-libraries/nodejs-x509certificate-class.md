---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-x509certificate-class
name: nodejs-x509certificate-class
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, node-x509certificate, node-crypto, nodejs, x509, certificate-inspection, checkhost, javascript]
level: practitioner
status: verified
description: "Inspect certificates in Node.js with crypto.X509Certificate: subject, SANs, validity, fingerprints, checkHost, checkIssued and verify, and its limits as a validator."
sources: ["https://nodejs.org/api/crypto.html#class-x509certificate", "https://www.rfc-editor.org/rfc/rfc5280", "https://www.rfc-editor.org/rfc/rfc9525"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js X509Certificate class

## Inspect
```js
import { X509Certificate } from "node:crypto";
const cert = new X509Certificate(fs.readFileSync("leaf.pem"));
cert.subject;            // "CN=api.example.com"
cert.subjectAltName;     // "DNS:api.example.com, DNS:www.example.com"
cert.issuer;
cert.validFrom; cert.validTo;          // strings; validFromDate/validToDate (Date) from v22.10 / v23.0 (undefined on Node 20)
cert.fingerprint256;     // "AB:CD:..." SHA-256 of DER
cert.serialNumber;
cert.ca;                 // basicConstraints CA flag
cert.keyUsage;           // extended key usage OIDs array, e.g. ['1.3.6.1.5.5.7.3.1'] (serverAuth)
cert.publicKey;          // KeyObject
```

## Checks
```js
cert.checkHost("api.example.com");          // returns the matched name or undefined (RFC 6125 rules, wildcards)
cert.checkIP("10.0.0.5");
cert.checkEmail("ops@example.com");
cert.checkIssued(issuerCert);               // issuer/subject and key identifier linkage (true for the CA, false the other way round; checked)
cert.verify(issuerCert.publicKey);          // signature check only (returns a boolean)
cert.checkPrivateKey(privateKeyObject);     // key matches certificate
```

## Limits
`X509Certificate` is an inspection tool, not a path validator: it does not build chains, check trust anchors, EKU,
name constraints or revocation. For TLS, let `tls`/`https` validate. For custom validation (e.g. signed documents),
use a PKI library (`pkijs`, `@peculiar/x509` with a chain builder) or call out to OpenSSL.

## Uses
- Expiry monitoring scripts (`new Date(cert.validTo) - Date.now()`).
- Pinning by SPKI: `createHash("sha256").update(cert.publicKey.export({type:"spki", format:"der"})).digest("base64")`.
- Debugging what certificate a peer presented (`socket.getPeerX509Certificate()`).

## Verify
- [ ] Monitoring script flags a certificate expiring within the threshold.
- [ ] Production validation still uses the TLS stack, not ad-hoc checks.
