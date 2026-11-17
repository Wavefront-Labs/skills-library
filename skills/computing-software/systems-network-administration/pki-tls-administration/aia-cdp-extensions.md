---
id: computing-software.systems-network-administration.pki-tls-administration.aia-cdp-extensions
name: aia-cdp-extensions
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [aia-cdp-extensions, pki-extensions, pki, authorityinfoaccess, crldistributionpoints, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Set authorityInfoAccess (caIssuers, OCSP) and cRLDistributionPoints URLs correctly so clients can fetch issuers and revocation data."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AIA and CRL distribution points
Goal: every certificate points to reachable locations for its issuer certificate, OCSP and CRL. Source: RFC 5280 sections 4.2.1.13 and 4.2.2.1.

```
authorityInfoAccess = OCSP;URI:http://ocsp.example.com, caIssuers;URI:http://pki.example.com/issuing-g2.crt
crlDistributionPoints = URI:http://pki.example.com/issuing-g2.crl
```

## authorityInfoAccess (AIA)
- Describes how to reach services of the certificate's issuer: on-line validation and CA policy data. CRL locations are not given here; they come from cRLDistributionPoints. Conforming CAs MUST mark AIA non-critical.
- The profile defines two access methods: `id-ad-ocsp` and `id-ad-caIssuers`. caIssuers lists certificates issued to the CA that issued this certificate, to help clients build a path to a trusted point.
- For HTTP or FTP, the accessLocation MUST be a URI pointing to a single DER-encoded certificate or a "certs-only" CMS message. Clients supporting HTTP or FTP MUST accept single DER certificates. HTTP servers SHOULD send `application/pkix-cert` for one DER certificate and `application/pkcs7-mime` for a certs-only CMS message.
- LDAP is allowed: the LDAP URI MUST include the DN and attribute list and SHOULD include the host.

## cRLDistributionPoints (CDP)
- The extension SHOULD be non-critical, but the profile RECOMMENDS CAs and applications support it.
- A DistributionPoint must have distributionPoint or cRLIssuer. If the certificate issuer is also the CRL issuer, the CA MUST omit cRLIssuer and MUST include distributionPoint.
- Multiple names in one distribution point describe different mechanisms for the same CRL, such as LDAP and HTTP.
- For HTTP or FTP the URI MUST point to a single DER-encoded CRL; HTTP servers SHOULD send `application/pkix-crl`.

## Practitioner advice (not from RFC 5280)
- Many deployments publish AIA, OCSP and CRL over plain HTTP so that fetching revocation data does not itself require validating a TLS certificate.
- Use a stable DNS alias in the URLs, because already-issued certificates cannot be changed when a hostname changes.
- Make the hosts highly available; unreachable CRL or OCSP locations can stall clients.
- Do not rely on clients fetching caIssuers; send the intermediates from the server.
- Outside Active Directory environments, list HTTP URIs rather than LDAP.

## Verify
- [ ] Each URL in the issued certificate returns the right object and content type, and a certificate inspection shows both extensions.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read RFC 5280 sections 4.2.1.13 and 4.2.2.1 (criticality, access methods, URI rules, media types). Removed as unsupported by the RFC: the HTTPS chicken-and-egg claim as a requirement, "Windows follows caIssuers, many Linux clients do not", URI ordering behaviour, and the curl and openssl checks. Those that remain are marked practitioner advice.
