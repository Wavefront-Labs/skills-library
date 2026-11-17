---
id: computing-software.cloud-infrastructure-engineering.aws.inspector-suppression-rules-and-inspector-score
name: inspector-suppression-rules-and-inspector-score
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, inspector, inspector-suppression, inspector-score, vulnerability-management, epss]
level: advanced
status: docs-checked
description: "Prioritise Amazon Inspector findings with the Inspector score, EPSS and exploit/fix filters, and create suppression rules for accepted risk without deleting findings."
sources: ["https://docs.aws.amazon.com/inspector/latest/user/findings-managing-supression-rules.html", "https://docs.aws.amazon.com/inspector/latest/user/findings-understanding-score.html", "https://docs.aws.amazon.com/cli/latest/reference/inspector2/create-filter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspector suppression rules and Inspector score

## 1. Inspector score
Starts from the NVD/vendor CVSS base score and is adjusted with environment data: network
reachability data and exploitability data. Use it plus the EPSS score to rank.
```bash
aws inspector2 list-findings --filter-criteria '{
  "inspectorScore":[{"lowerInclusive":8.0,"upperInclusive":10.0}],
  "exploitAvailable":[{"comparison":"EQUALS","value":"YES"}],
  "fixAvailable":[{"comparison":"EQUALS","value":"YES"}],
  "findingStatus":[{"comparison":"EQUALS","value":"ACTIVE"}]}' \
  --sort-criteria field=INSPECTOR_SCORE,sortOrder=DESC --max-results 50
```
`epssScore` is also a filter field. Patch "score >= 8, exploit available, fix available" first.

## 2. Suppression rule
```bash
aws inspector2 create-filter --name accept-cve-in-sandbox --action SUPPRESS \
  --reason "Sandbox only, risk accepted until 2027-01" \
  --filter-criteria '{"vulnerabilityId":[{"comparison":"EQUALS","value":"CVE-2024-12345"}],
    "resourceTags":[{"comparison":"EQUALS","key":"env","value":"sandbox"}]}'
aws inspector2 list-filters --action SUPPRESS
```
- Matching findings are suppressed and hidden from view; Inspector stores them until they
  are remediated. Rules only hide findings: they cannot close or remediate them.
- Only standalone accounts and the delegated administrator can create and manage suppression
  rules; members do not see the option.
- A new rule may take up to 24 hours to take effect.
- Suppressing in Security Hub CSPM is a separate step (an EventBridge rule).

## Gotchas
- Suppress narrowly (CVE + tag/resource), never by severity alone.
- Put the expiry date in `--reason` and review rules on a schedule.

## Verify
- [ ] `list-findings` with `findingStatus=SUPPRESSED` shows the expected set.
- [ ] Top-20 by Inspector score has owners and tickets.

## Checked

2026-10-28. Confirmed against AWS documentation: score uses NVD/vendor source plus reachability and exploitability data, suppression rule behaviour (hidden, stored until remediated, delegated admin/standalone only, up to 24 hours, Security Hub separate), filter fields and SUPPRESS action and sort fields via botocore inspector2 model.
Removed: EPSS 30-day definition, rules-apply-to-members and Security Hub workflow-sync claims, reappear-on-delete and no-expiry claims, port-exposure detail.
Method: documentation only; no commands were run.
