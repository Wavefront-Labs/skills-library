---
id: computing-software.qa-testing-engineering.test-case-design.jira-test-management-xray-zephyr
name: jira-test-management-xray-zephyr
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [xray, zephyr, test-management-tools, jira, test-executions, test-case-management, junit-xml-import, results-import]
level: practitioner
status: draft
description: "Manage tests inside Jira with Xray or Zephyr: test issue types, test sets/plans/executions, coverage per story, and importing automated JUnit/Cucumber results."
sources:
  - https://docs.getxray.app/display/XRAYCLOUD/Import+Execution+Results+-+REST+v2
  - https://support.smartbear.com/zephyr/docs/en/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jira-native test management: Xray and Zephyr

**Goal:** tests, executions and requirement coverage visible in the same tool as stories and defects.

## Xray concepts
- Issue types: **Test**, **Pre-Condition**, **Test Set** (grouping), **Test Plan** (scope for a release), **Test Execution** (a run, with environment).
- Tests link to stories via "tests" relation; **requirement coverage** status per story per version/test plan (OK / NOK / NOTRUN).
- Test environments on executions give per-environment status.

## Importing automation results (Xray Cloud)
```bash
TOKEN=$(curl -s -H "Content-Type: application/json" -X POST \
  --data "{\"client_id\":\"$XRAY_ID\",\"client_secret\":\"$XRAY_SECRET\"}" \
  https://xray.cloud.getxray.app/api/v2/authenticate | tr -d '"')
curl -H "Authorization: Bearer $TOKEN" -H "Content-Type: text/xml" -X POST \
  --data @results.xml "https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey=SHOP&testPlanKey=SHOP-100"
```
Tests are matched by name or created automatically; link to stories via annotations (e.g. JUnit `@Requirement`, or Cucumber tags `@SHOP-123`).

## Zephyr (Scale/Squad)
Test cases, cycles (executions) and folders inside Jira; similar REST import of JUnit results; traceability via issue links.

## Practices
- Use Test Plans per release for the dashboard; executions per CI run or per manual cycle.
- Agree a naming/linking convention for automated tests before importing, or you get duplicate Test issues.

## Gotchas
- Every import creating new Test issues floods Jira; match by key/annotation.
- Jira permissions and issue-type schemes need admin setup; plan it.

## Verify
Story view shows linked tests and latest execution status; a CI import updates existing Tests instead of creating new ones.
