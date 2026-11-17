---
id: computing-software.cybersecurity-defensive.nessus.pci-asv-external-scans
name: pci-asv-external-scans
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, pci-asv-scan, pci-dss, asv, external-scanning, compliance, tenable-vulnerability-management, scan-configuration]
level: practitioner
status: draft
description: "Run PCI DSS quarterly external vulnerability scans with an Approved Scanning Vendor (Tenable PCI ASV): scope, scanning, disputes, passing criteria and attestation."
sources: ["https://docs-prv.pcisecuritystandards.org/Guidance%20Document/ASV/ASV_Program_Guide_v4.0.pdf", "https://docs.tenable.com/vulnerability-management/Content/PCIASV/PCIASV.htm", "https://www.pcisecuritystandards.org/document_library/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# PCI DSS quarterly external (ASV) scans

PCI DSS 11.3.2 requires external vulnerability scans at least once every three months by a PCI SSC
Approved Scanning Vendor (ASV), and after significant changes; a passing scan each quarter.

## Scope
- All internet-facing IPs/hostnames in or connected to the cardholder data environment (CDE),
  including load balancers, WAF, remote access, and cloud-hosted components.
- Customer attests scope; under-scoping is the most common audit finding.

## Pass criteria (ASV Program Guide)
- No vulnerabilities with CVSS base score 4.0 or higher.
- Automatic failures regardless of score: e.g. SQL injection/XSS found, default credentials,
  unsupported OS/software, and other listed conditions.
- Components behind a WAF/IPS that blocks the ASV scanner: the scanner must be allowlisted
  (interference produces an inconclusive scan).

## Tenable PCI ASV workflow
1. Run a "PCI Quarterly External Scan" template from Tenable cloud scanners against scope.
2. Submit the scan for attestation in the PCI ASV workbench.
3. For each failing finding, remediate and rescan, or **dispute** with evidence (false positive,
   compensating control, out of scope). Tenable ASV reviews disputes.
4. Once accepted, download the Attestation of Scan Compliance (AOSC) and executive/detailed reports.

## Practice
- Scan early in the quarter, leaving time for remediation and rescans.
- Run your own internal scan of the same scope weekly so ASV results are no surprise.
- Keep evidence for disputes (version banners backported, vendor advisories).

## Gotchas
- Four consecutive quarterly passes are needed for annual compliance; a missed quarter is a gap.
- Load balancers hiding many backends: scan each backend or ensure consistent versions.

## Verify
Four passing AOSCs per year in the evidence repository with scope matching the CDE network diagram.
