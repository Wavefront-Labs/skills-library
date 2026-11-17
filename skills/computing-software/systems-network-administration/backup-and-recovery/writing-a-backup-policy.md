---
id: computing-software.systems-network-administration.backup-and-recovery.writing-a-backup-policy
name: writing-a-backup-policy
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-policy, policy-writing, governance, retention, rpo, rto, iso-27001]
level: practitioner
status: docs-checked
description: "Write an organisational backup policy: scope, roles, tiers with RPO/RTO, retention, copies, encryption, testing, monitoring and exceptions."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a backup policy

A policy states **what must be true**; standards and runbooks say how. Keep it short, approved by senior management, and reviewed on a schedule you set.

## What NIST SP 800-34 Rev. 1 says about backup policy (section 3.4.2)
Policies should specify the minimum frequency and scope of backups (for example daily or weekly, incremental or full) based on data criticality and how often new information is introduced. They should designate the location of stored data, file-naming conventions, media rotation frequency and the method for transporting data offsite. The method should reflect system and data availability and integrity requirements. The guide calls offsite storage good business practice, and lists offsite-vendor selection criteria: geographic area, accessibility, security, environment and cost. It also says backup tapes should be tested regularly to confirm data is stored correctly and retrievable without errors.

## Sections (practice; adapt to your organisation)
1. **Purpose and scope**: all production systems, SaaS data, endpoints (or explicitly excluded), cloud accounts. Name what is out of scope and why.
2. **Roles**: backup service owner, system owners (classify data and accept tier), backup operators, security (key custody), auditors.
3. **Protection tiers** with RPO, RTO, retention and copy rules (see the protection tiers skill). Every system in the CMDB must have an assigned tier. Derive RPO and RTO from the BIA (SP 800-34 defines MTD, RTO and RPO there).
4. **Backup frequency and scope**: per tier, full or incremental, as the guide lists above.
5. **Copies**: state the minimum number of copies, media types, off-site and immutable or offline requirements, and what counts as a verified restore (see the 3-2-1 skill).
6. **Retention**: operational vs legal/regulatory, linked to the records retention schedule; legal hold overrides deletion.
7. **Media handling**: location of stored data, naming, rotation and offsite transport, per the guide.
8. **Security**: encryption at rest and in transit, key management and escrow, separate admin identities and MFA for backup systems, no production-domain dependency.
9. **Testing**: restore tests per tier at a stated frequency, a DR exercise on a stated cycle, results recorded.
10. **Monitoring**: daily review, RPO compliance reporting, escalation times.
11. **Exceptions**: how a system owner requests a lower tier or exclusion; risk acceptance signed and time-limited.
12. **Compliance and review**: map controls to your own framework, set a review cycle and consequences.

## Writing rules
- Use "must" for requirements; measurable statements (state the frequency as a number), not "regularly".
- No product names in the policy; put them in the standard.
- Define terms (RPO, RTO, immutable, off-site).

## Verify
Every requirement maps to evidence an auditor could request (report, log, ticket), and each system owner has signed off their tier.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (PDF behind the csrc.nist.gov page), section 3.4.2 and the MTD/RTO/RPO definitions in 3.2.1. Targeted reads, not the whole 149 pages. Confirmed: backup policy contents, offsite criteria, tape testing. Removed: the CIS and ISO sources (not readable), the control mappings (ISO 27001 A.8.13, CIS Control 11, SOC 2 A1.2), "3-5 pages", "reviewed yearly", the 3-2-1-1-0 formula, and the example test frequencies. The section list is labelled practice.

Method: documentation only; no commands were run.
