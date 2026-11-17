---
id: computing-software.cloud-infrastructure-engineering.aws.trusted-advisor-organizational-view-reports
name: trusted-advisor-organizational-view-reports
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, trusted-advisor, ta-organizational-view, organizations, trusted-advisor-reports, check-summary]
level: practitioner
status: draft
description: "Get Trusted Advisor results for every account in an organization: enabling organizational view, generating and reading reports, support plan limits and the newer TA APIs."
sources: ["AWS Support User Guide - Organizational view for AWS Trusted Advisor", "AWS Support User Guide - Trusted Advisor check reference", "AWS Trusted Advisor API Reference - ListOrganizationRecommendations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trusted Advisor organizational view reports

## Enable
1. Organization with **all features**; sign in to the management account.
2. Trusted Advisor console > Preferences > Organizational view > Enable trusted access
   (registers `reporting.trustedadvisor.amazonaws.com` with Organizations).
3. Wait for data collection (can take hours); member accounts need checks refreshed at least once.

Full check coverage (cost optimization, security beyond the basics, fault tolerance, performance,
service limits) requires Business, Enterprise On-Ramp or Enterprise Support on the accounts; Basic/Developer accounts report only core checks.

## Reports
- Create a report: choose accounts/OUs, check categories, specific checks, status (red/yellow), format **JSON or CSV**.
- Reports are generated asynchronously and downloaded as a zip (summary plus per-check files with affected resources and account ids).
- Schedule: there is no built-in schedule; regenerate monthly, or use the APIs below.

## APIs
```bash
aws trustedadvisor list-organization-recommendations --region us-east-1 \
  --query 'organizationRecommendationSummaries[?status==`error`].[name,pillars[0],resourcesAggregates]'
aws trustedadvisor list-organization-recommendation-accounts --organization-recommendation-identifier "$ARN"
aws trustedadvisor list-organization-recommendation-resources --organization-recommendation-identifier "$ARN"
```
- The Trusted Advisor API (`trustedadvisor`) supports organization-level recommendations and lifecycle updates (acknowledge, dismiss with reason) from the management/delegated account.
- The older `support` API (`describe-trusted-advisor-checks`) works per account only.
- Trusted Advisor Priority (Enterprise) adds account-team-curated recommendations with owners.

## Using the results
- Feed into a monthly hygiene review per OU: open security groups, IAM keys not rotated, idle load balancers, low-utilisation instances, service limits > 80%.
- Export to S3 and query in Athena / QuickSight for trends.
- Suppress false positives per account (exclude resources) so reports stay actionable.

## Gotchas
- Organizational view data lags behind individual account refreshes.
- Disabling trusted access deletes org view data.
- Security Hub and Config cover many security checks with better automation; use TA for cost and limits breadth.

## Verify
- [ ] Organizational report lists all active accounts; spot-check one finding in a member account.
- [ ] Monthly review produces tickets per owning team.
