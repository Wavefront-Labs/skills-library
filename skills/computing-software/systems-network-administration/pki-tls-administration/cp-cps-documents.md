---
id: computing-software.systems-network-administration.pki-tls-administration.cp-cps-documents
name: cp-cps-documents
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cp-cps-documents, pki-policy-docs, pki, cp, cps, rfc3647, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Write a Certificate Policy and Certification Practice Statement using the RFC 3647 outline, scoped to an internal or public CA."
sources:
  - https://www.rfc-editor.org/rfc/rfc3647
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate Policy and CPS documents
Goal: a document set auditors and relying parties can use to judge what a certificate means.
- A CP is a named set of rules for the applicability of a certificate to a community or class of applications. A CPS describes the practices a CA uses to issue and manage certificates and is generally more detailed than the CP; a CP is more general.
- One CP can be supported by several CPSs (for example one per agency or CA), each explaining how it meets the CP requirements.
- Use the RFC 3647 skeleton: 1 Introduction, 2 Publication and Repository Responsibilities, 3 Identification and Authentication, 4 Certificate Life-Cycle Operational Requirements, 5 Facility, Management, and Operational Controls, 6 Technical Security Controls, 7 Certificate, CRL, and OCSP Profiles, 8 Compliance Audit and Other Assessments, 9 Other Business and Legal Matters.
- Include every component, even if only to state "no stipulation": RFC 3647 recommends this so readers know the omission was a conscious decision, and it eases comparison of policies.
- Reference the policy in issued certificates through the certificatePolicies extension; RFC 5280 defines the CPS pointer qualifier (a URI string) for that extension.
- Give the document a version and effective date and assign a policy OID (practice, not mandated by the RFC).
Gotcha: copying another CA's CPS verbatim claims controls you do not run. Every sentence should map to a procedure or be deleted.
Verify:
- [ ] All nine RFC 3647 sections present or marked "no stipulation".
- [ ] Policy OID in issued certs matches the document and the CPS URL resolves.

## Checked
Method: docs-checked 2026-11-09 against RFC 3647 (introduction, section on drafting style, outline) and RFC 5280 (certificatePolicies CPS qualifier) text, read in full where cited.
Removed: Baseline Requirements source (documents index page, unread) and the claim that public CAs must update the CPS at least yearly.
