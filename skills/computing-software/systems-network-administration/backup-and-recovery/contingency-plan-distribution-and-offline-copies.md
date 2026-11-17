---
id: computing-software.systems-network-administration.backup-and-recovery.contingency-plan-distribution-and-offline-copies
name: contingency-plan-distribution-and-offline-copies
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [plan-distribution, contingency-plan, offline-copy, iscp, document-control, business-continuity]
level: practitioner
status: docs-checked
description: "Control distribution of contingency and DR plans: who holds copies, offline and printed copies, encrypted portable copies and superseded versions."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plan distribution and offline copies

**Goal:** every person who must act has the current plan, even when the network, email and document system are gone.

## What NIST SP 800-34 Rev. 1 says (section 3.6)
- The plan holds sensitive operational and personnel information, so mark its distribution accordingly and control it.
- Copies typically go to recovery personnel for storage; a copy should also be stored at the alternate site and with the backup media, so it is available if local copies cannot be accessed.
- The ISCP Coordinator keeps a record of copies of the plan and to whom they were distributed.
- Store with the plan: vendor contracts (SLAs), software licences, system user manuals, security manuals and operating procedures.
- Strict version control: old plans or pages are returned to the Coordinator in exchange for new ones.
- Notification procedures can be copied and located securely at alternate locations (section 4.2.2).

## Distribution register (practice)
Keep copy number, holder role, format, location, version held and date issued. Typical holders: plan director, recovery team leads, alternates, alternate-site manager, service desk lead.

## Copy formats (practice)
| Format | Use | Control |
|---|---|---|
| Master in document system | edits, approval | versioned, access-controlled |
| Encrypted PDF on USB / laptop | ransomware, network loss | encrypted container, key in sealed envelope or password vault outside the domain |
| Printed binder | total power/IT loss | numbered copies, locked cabinet at each site |
| Out-of-band cloud copy | sites down | separate tenant/account, separate identity, MFA |

Include the runbooks, contact lists, network diagrams and credentials *references* (never plaintext passwords in the printout; point to the break-glass vault).

## Version control
- Version, date and change summary on page 1; footer on every page. NIST's record of changes lists page number, change comment, date and signature.
- On a new version: issue to all holders, collect or confirm destruction of the old copy, update the register.
- Review after every exercise and real activation (the guide says after-action reports feed plan updates).

## Gotchas
- A plan stored only on the file server that is encrypted by ransomware is no plan.
- Break-glass credentials and the decryption password for the encrypted copy must not depend on the AD that may be down.
- Contact lists contain personal data; limit copies and mark them.

## Verify
Pick a few holders at random on a regular cycle and ask them to open their copy without corporate network access; the version matches the master.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (PDF behind the csrc.nist.gov page), sections 3.6 and 4.2.2. Targeted reads, not the whole 149 pages. Confirmed: controlled and marked distribution, copies at alternate site and with backup media, record of copies, stored supporting documents, return-and-exchange version control, record-of-changes columns. Removed: the NIST SP 800-53 source and the "CP-2 requires distribution to key personnel" claim (800-53 not read), and the "each quarter" figure. Register and format table are labelled practice.

Method: documentation only; no commands were run.
