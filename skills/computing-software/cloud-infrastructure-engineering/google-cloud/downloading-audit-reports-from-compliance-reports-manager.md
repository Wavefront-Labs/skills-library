---
id: computing-software.cloud-infrastructure-engineering.google-cloud.downloading-audit-reports-from-compliance-reports-manager
name: downloading-audit-reports-from-compliance-reports-manager
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compliance, audit-reports, soc2, iso-27001, vendor-risk, compliance-reports-download, soc2-iso-report-access]
level: practitioner
status: docs-checked
description: "Get Google Cloud SOC, ISO and PCI DSS audit evidence from Compliance Reports Manager for vendor reviews, and check services in scope."
sources: ["https://cloud.google.com/security/compliance/compliance-reports-manager", "https://cloud.google.com/security/compliance/offerings", "https://cloud.google.com/security/compliance/services-in-scope"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Downloading audit reports from Compliance Reports Manager

Auditors and vendor-risk teams ask for Google's third-party attestations. Compliance Reports Manager provides
on-demand access to compliance resources at no additional cost; key resources include the latest ISO/IEC
certificates, SOC reports and self assessments. The Compliance offerings page covers certifications plus
region- or sector-specific regulations. The manager page loads its catalogue dynamically, so which reports need
sign-in or terms acceptance is not stated in the page text: follow what the console shows you.

## Use them properly
1. Check the **services in scope** page: it has one row per service and columns for ISO 27001/27017/27018,
   SOC 1/2/3 reports, PCI DSS and penetration testing. Some rows are partial (for example "ISO 27001 only" or
   "SOC 2/3 only"). Confirm every service you use is in scope for every report you rely on.
2. If a SOC report lists user entity controls (controls you are expected to operate), map each to your own
   control owner and evidence.
3. Note any exceptions or qualified opinions and how they were handled.
4. Record report version and period in your vendor register and refresh when a new one is published.

## Gotchas
- Reports cover Google's controls, not your configuration; your auditors still test your side.
- Check regional or sector scope on the offerings page for region-specific requirements.
- Respect any confidentiality terms attached to reports you download.

## Verify
- [ ] Vendor file holds current reports, a services-in-scope check, and control mapping with owners.

## Checked
2026-10-28. Confirmed on the three pages: no-cost on-demand access, ISO certificates, SOC reports, self assessments,
the certifications covered by the services-in-scope table and its partial-scope markers. Removed (not confirmable;
the manager page is a stub): which reports are public versus confidential, NDA and billing-relationship
requirements, filter options, bridge letters, and the PCI AOC, ISO SoA and C5 report names.
Method: documentation only; no commands were run.
