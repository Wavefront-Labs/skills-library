---
id: computing-software.systems-network-administration.patch-management.cisa-emergency-and-binding-directives
name: cisa-emergency-and-binding-directives
category: computing-software
field: systems-network-administration
product: patch-management
tags: [emergency-directive, binding-operational-directive, cisa-kev, bod-26-04, vulnerability-intelligence, patch-management]
level: practitioner
status: docs-checked
description: "Respond to CISA Emergency Directives and BOD 26-04 (which replaced BOD 22-01) KEV deadlines: map required actions to assets, meet deadlines and keep evidence even when not bound."
sources:
  - https://www.cisa.gov/news-events/directives
  - https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk
  - https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk
  - https://www.cisa.gov/news-events/directives/bod-23-01-improving-asset-visibility-and-vulnerability-detection-federal-networks
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CISA emergency and binding operational directives

**Scope:** Emergency Directives (ED) and Binding Operational Directives (BOD) are mandatory for US federal civilian (FCEB) agencies; everyone else uses them as a strong signal of active exploitation and a defensible deadline.

## Types
- **ED**: urgent, product-specific, short deadlines. Current examples on the CISA directives page: ED 25-03 "Identify and Mitigate Potential Compromise of Cisco Devices" (with a supplemental "Core Dump and Hunt Instructions") and ED 26-03 "Mitigate Vulnerabilities in Cisco SD-WAN Systems". Expect required actions beyond patching (evidence collection, hunting), and expect versions and supplements to replace earlier text.
- **BOD 26-04** "Prioritizing Security Updates Based on Risk" (issued 10 June 2026): supersedes and revokes BOD 22-01 and BOD 19-02. Remediate each vulnerability within the Table 1 timelines, which depend on four variables: asset exposure, KEV status, exploit automatability and technical impact. The KEV `dueDate` is set from those timelines. CISA's guidance gives a 3-day example for an exposed asset with total technical impact and an automatable exploit. The old fixed rule of two weeks for new CVEs and six months for pre-2021 CVEs (BOD 22-01) no longer applies to FCEB agencies; a 3-day timeline also exists for items marked for forensic triage. The day counts in Table 1 are in BOD 26-04 Appendix A: read them there.
- BOD 26-04 no longer requires CVSS for FCEB prioritisation. Use KEV, automatability and exposure; keep CVSS only as one input.
- **BOD 23-01**: per its page, automated asset discovery every 7 days and vulnerability enumeration every 14 days. Check the directives page for its current status.
- **BOD 26-02** "Mitigating Risk From End-of-Support Edge Devices" is also listed; see end-of-life detection skills.

## Pull KEV and match to inventory
```sh
curl -s https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json \
 | jq -r '.vulnerabilities[] | [.cveID,.vendorProject,.product,.dateAdded,.dueDate,.knownRansomwareCampaignUse,.forensicTriage] | @tsv' > kev.tsv
```
Feed fields (read from the feed on 2026-10-27): `cveID`, `vendorProject`, `product`, `vulnerabilityName`, `dateAdded`, `shortDescription`, `requiredAction`, `dueDate`, `knownRansomwareCampaignUse` (values `Known` or `Unknown`), `forensicTriage`, `notes`, `cwes`. The gap between `dateAdded` and `dueDate` varies by entry (observed from 1 day to about 6 months), so do not assume a constant.
Join on CVE to scanner findings; anything matched gets the KEV due date (or your shorter SLA).

## Working an ED
1. Read every required action literally; list them as checklist rows.
2. Identify all instances, including lab, DR and appliances nobody owns.
3. Run the vendor's integrity or hunt instructions before and after patching; a clean patch on a compromised box leaves the attacker in.
4. Follow the mandated sequence exactly.
5. Report via the required channel by the deadline; keep timestamps, screenshots and tool output.

## Gotchas
- Supplemental directions get issued mid-ED; subscribe to updates and re-check the page.
- Workarounds can be reverted by a later upgrade; re-verify after every change.
- A `dueDate` can already be in the past or only days away when a CVE is added; treat as immediate.

## Verify
Every ED action has evidence attached, KEV-matched findings are zero past due, and the asset list was reconciled against discovery data, not just the CMDB.

## Checked
Date: 2026-10-27. Documentation: CISA directives page, BOD 26-04 and its implementation guidance, BOD 23-01 page, live KEV JSON feed (catalogVersion 2026.10.26). Confirmed: BOD 22-01 revoked by BOD 26-04; four risk variables; KEV dueDate role; 3-day example; CVSS no longer required for FCEB; BOD 23-01 7/14 days; KEV field names and values. Removed unconfirmed ED 24-01 and ED 21-01 examples. Table 1 day counts were not readable and are not stated.
Method: documentation only; no commands were run.
