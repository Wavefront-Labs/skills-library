---
id: computing-software.systems-network-administration.pki-tls-administration.certificate-policies-oids
name: certificate-policies-oids
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [certificate-policies-oids, pki-constraints, pki, certificatepolicies, policy-oid, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Register a private OID arc, set certificatePolicies, policyConstraints and mappings, and use policy OIDs to control which certs are acceptable."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate policies and OIDs
Goal: tag certificates with the policy they were issued under and let relying parties require it. Source: RFC 5280 sections 4.2.1.4 and 4.2.1.11.

## certificatePolicies (RFC 5280 4.2.1.4)
- A sequence of policy terms, each an OID plus optional qualifiers. A policy OID MUST NOT appear more than once in one extension.
- In an end-entity certificate the terms say which policy it was issued under and the permitted purposes. In a CA certificate they limit the set of policies for paths that include it. A CA that does not want to limit policies MAY assert `anyPolicy` (2.5.29.32.0).
- Relying applications with policy requirements keep a list of accepted policy OIDs and compare them with those in the certificate. If the extension is critical, path validation software that cannot interpret it MUST reject the certificate.
- The profile RECOMMENDS terms consist of an OID only. The two defined qualifiers are the CPS Pointer (a URI to the CA's Certification Practice Statement) and User Notice.

## policyConstraints (RFC 5280 4.2.1.11)
- Used in CA certificates to prohibit policy mapping (`inhibitPolicyMapping`) or to require that every certificate in the path carry an acceptable policy (`requireExplicitPolicy`). The value is the number of additional certificates allowed before the rule applies.
- An acceptable policy is one the user requires or one declared equivalent through policy mapping.
- Conforming applications MUST process requireExplicitPolicy. CAs MUST NOT issue an empty policyConstraints; one of the two fields must be present.

## Practitioner advice (not from RFC 5280)
- Define a private policy OID arc under an enterprise number you hold (IANA assigns these) rather than inventing numbers, and document each OID in your CP/CPS.
- OpenSSL config example for an issuing CA:
```
certificatePolicies = @pol
[pol]
policyIdentifier = 1.3.6.1.4.1.99999.1.2
CPS.1 = https://pki.example.com/cps
```
- Policy checking in OpenSSL and Windows application policy depends on the tool's options; test that a chain without the required policy fails.
- Do not stamp the public TLS baseline-requirement policy OIDs on private certificates; they are meant for publicly trusted issuance under CA/Browser Forum rules (not read here).
- Use anyPolicy only on CAs that do not discriminate between policies.

## Verify
- [ ] Inspect the issued certificate's certificatePolicies and confirm the OID and CPS URI.
- [ ] A chain lacking the required policy fails validation in your chosen validator.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read RFC 5280 sections 4.2.1.4 and 4.2.1.11 (policy terms, anyPolicy, qualifiers, requireExplicitPolicy, inhibitPolicyMapping). RFC 3647 was not read, so it was dropped as a source. Removed as unsupported: the specific `.1`/`.1.1`/`.1.2` arc layout, the OpenSSL `-policy` and `-policy_check` flags and the 2.23.140.1.2.x reservation claim as fact. The OpenSSL configuration snippet and the other practitioner lines were not run.
