---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.gpl-source-offer-and-distribution
name: gpl-source-offer-and-distribution
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [gpl-source-offer-and-distribution, gpl-obligations-and-faq, gpl-compliance, corresponding-source, written-offer, conveying, build-scripts, source-release, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Satisfy GPL when shipping binaries: provide corresponding source, build scripts, licence texts and a valid written offer."
sources:
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPL source offer and distribution compliance

Goal: ship GPL code lawfully.

Method:
1. Identify every GPL component in the product image or installer.
2. Include a copy of the licence with the program. A URL is not enough: the FAQ says the only way to be sure recipients can still read the licence later is to include a copy.
3. Provide the complete corresponding source with the binaries, or a written offer to supply it. Distributing binaries without source is allowed only via that offer route; a modified version may not be released in binary form only.
4. Make the written offer valid for any third party: anyone who requests the source is entitled to it, and recipients who redistribute binaries non-commercially must pass the offer on. Anyone holding a copy of the binary may use the offer.
5. Include your modifications and patches. A modified version must be released as a whole under the GPL.
6. Include the scripts used to control compilation and installation (GPLv2 requires this; GPLv3 requires the fuller "Installation Information" for User Products, so its requirement is stronger).
7. Choose the delivery route. GPLv3 option 6(b) allows binaries on physical media with source offered over the network. Under GPLv2, offering source by FTP is fine but you must also supply source on physical media if a recipient asks. If you distribute binaries by FTP, distribute source by FTP.

Gotchas:
- Source for a different version than shipped does not satisfy the licence: give clear instructions for getting the source of the exact object code downloaded. A version-control link is acceptable if checkout is not burdensome or restrictive and uses a publicly available free client.
- Binaries and source may sit on different sites (see the FAQ entry on that question).
- GPLv3 termination is more permissive than GPLv2; see the licence text for the cure terms.

Verify: build the source offer package from scratch in a clean environment.

## Checked

2026-11-08. Confirmed against the GNU GPL FAQ (gpl-faq.html): including a copy of the licence, binaries-only rules, the written-offer entries, FTP and physical media rules for GPLv2 versus GPLv3 option 6(b), the installation-information comparison, the version-control-link answer and the GPLv3 termination comparison. Removed as unconfirmed because the licence texts were not readable in this session: the "3 years" offer duration, the 30-day cure period for a first violation, and the "scripts to control compilation (GPL-3.0 wording)" detail beyond the FAQ's statement for GPLv2.
Method: documentation only; no commands were run.
