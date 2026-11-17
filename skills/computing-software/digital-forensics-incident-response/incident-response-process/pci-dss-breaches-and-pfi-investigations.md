---
id: computing-software.digital-forensics-incident-response.incident-response-process.pci-dss-breaches-and-pfi-investigations
name: pci-dss-breaches-and-pfi-investigations
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [pci-forensic-investigator, pci-dss, breach-notification, cardholder-data, dfir]
level: advanced
status: draft
description: "Handle suspected cardholder-data compromise: brand notification, engaging a PCI Forensic Investigator, preserving CDE evidence and common skimming artefacts."
sources: ["https://www.pcisecuritystandards.org/assessors_and_solutions/pci_forensic_investigators", "https://www.pcisecuritystandards.org/document_library/", "https://usa.visa.com/dam/VCOM/download/merchants/cisp-what-to-do-if-compromised.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PCI DSS breaches and PFI investigations

**Goal:** when card data may be compromised, card brands and acquirers drive a specific process.
Following it avoids fines and preserves evidence a PCI Forensic Investigator (PFI) needs.

## Immediate steps (per Visa "What To Do If Compromised" and brand rules)
1. Contain without destroying evidence: do not wipe or rebuild POS/e-commerce servers; isolate
   from the network but keep powered where memory matters.
2. Notify the **acquiring bank** promptly (brands typically expect within 24-72 h of discovery);
   the acquirer notifies brands.
3. Engage a **PFI** from the PCI SSC list if the brand/acquirer requires (usually required for
   Level 1-2 or confirmed compromise). The PFI must be independent of your QSA.
4. Preserve logs: web server, WAF, payment page change history, POS, firewall, FIM.

## What the PFI looks for
- **E-commerce skimming (Magecart):** injected JavaScript on checkout pages, modified third-party
  scripts, changes to `checkout`/`payment` templates; compare deployed files to source control.
- **POS RAM scrapers:** memory-scraping malware on POS terminals/servers, output files with track data.
- Window of intrusion (first and last date card data was at risk), number of accounts exposed,
  whether data was stored in violation of PCI DSS (full track, CVV2).

## Deliverables
- PFI preliminary and final reports to the brands and acquirer; at-risk account lists (PANs) to brands.
- Your remediation evidence and re-validation of PCI DSS compliance.

## Gotchas
- Internal IR may proceed but must not alter the CDE before the PFI images it; coordinate.
- Tokenised / P2PE environments shrink scope; document that card data never reached your systems.
- Legal privilege over PFI reports is limited: they go to the brands.

## Verify
Acquirer notification time, PFI engagement letter, and preserved CDE evidence are recorded in the case.
