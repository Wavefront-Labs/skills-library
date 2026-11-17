---
id: computing-software.cybersecurity-defensive.cloud-security.amazon-macie-sensitive-data-discovery
name: amazon-macie-sensitive-data-discovery
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-data-protection, amazon-macie, sensitive-data-discovery, pii-detection, automated-sensitive-data-discovery, custom-data-identifiers, data-classification, dspm]
level: practitioner
status: docs-checked
description: "Use Amazon Macie to find sensitive data in S3: automated discovery and sensitivity scores, custom data identifiers, allow lists and acting on the results."
sources: ["https://docs.aws.amazon.com/macie/latest/user/discovery-asdd-how-it-works.html", "https://docs.aws.amazon.com/macie/latest/user/custom-data-identifiers.html", "https://docs.aws.amazon.com/macie/latest/user/allow-lists.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensitive data discovery with Amazon Macie

**Goal:** know which S3 buckets hold personal, financial or credential data, so protections and
exposure decisions are based on content, not on bucket names.

## Set up
- Enable Macie in your accounts and Regions; as the Macie administrator for an organization you can cover member accounts' buckets (automated discovery includes them by default).
- Turn on **automated sensitive data discovery**: each day Macie evaluates your S3 inventory data, selects a sampling of representative objects, and analyses the latest version of each for sensitive data. Changed settings apply from the next daily cycle.
- Macie calculates a **sensitivity score** and label per S3 general purpose bucket. When you first enable discovery every bucket starts at score 50 with the label Not yet analyzed (empty buckets get 1 and Not sensitive). Scores and labels are reference points for finding risk, not a measure of how important a bucket is.
- Use **sensitive data discovery jobs** for full scans of specific high-risk buckets (one-time or scheduled).

## Identifiers
- Managed data identifiers are the built-in detection criteria that Macie provides; custom ones supplement them.
- **Custom data identifiers**: a regex plus optional keywords (must appear near the match, within a proximity rule) and ignore words (exclude matches), for formats such as employee IDs or customer account numbers. Findings from a custom identifier default to Medium severity unless you configure custom severity settings based on the number of occurrences.
- **Allow lists** tell Macie to ignore text: a predefined-text list (exact matches, such as public phone numbers or test sample data) or a regular expression list (text that completely matches the pattern).

## Act on findings
- Route findings by account owner and prioritise sensitive data that is also publicly or cross-account accessible, then sensitive data in unexpected places (logs, dev accounts).
- Remediate: move data, tighten policies, delete, or record as expected with classification tags.

## Gotchas
- Macie inspects S3 objects only. Databases and other clouds need other data security tooling.
- Large numbers of findings on log buckets usually mean applications log personal data: fix at the source.
- Check the Macie pricing page before scoping full-bucket jobs.

## Verify
- [ ] All accounts and Regions show Macie enabled with automated discovery.
- [ ] Planted test file with synthetic card numbers in a test bucket produces a finding.

## Checked
Checked 2026-11-09 against the Macie User Guide pages in `sources` (automated discovery daily sampling and sensitivity scores, custom data identifier criteria and default severity, allow list types). Removed unconfirmed claims: Security Hub/EventBridge routing, KMS decrypt requirement for the Macie role, cost behaviour, managed identifier categories by country, and the CompTIA and CIS control references.
Method: documentation only; no commands were run.
