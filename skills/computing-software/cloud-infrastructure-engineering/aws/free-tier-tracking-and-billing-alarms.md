---
id: computing-software.cloud-infrastructure-engineering.aws.free-tier-tracking-and-billing-alarms
name: free-tier-tracking-and-billing-alarms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, free-tier, billing-alarm, estimatedcharges, free-tier-usage-alerts, zero-spend-budget, aws-budgets, free-plan, credits, cost-control, new-account-setup, cloudwatch-billing]
level: intro
status: docs-checked
description: "Keep a new or personal AWS account from surprise bills: free vs paid account plan and credits, free tier usage alerts, zero-spend budget template and EstimatedCharges alarm."
sources: ["https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html", "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/tracking-free-tier-usage.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html", "https://docs.aws.amazon.com/cost-management/latest/userguide/budget-templates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Free tier tracking and billing alarms

**Goal:** a learning, sandbox or startup account never produces an unexpected bill: free allowances are tracked, alerts fire early, and the owner knows which plan the account is on.

## 1. Which free model applies
- At sign-up you choose a **Free account plan** or **Paid account plan**. A new AWS customer gets USD $100 in credits after creating an account regardless of plan, and can earn up to another USD $100 by completing activities (see the page "Earning additional credits"). Over 30 always-free services have monthly limits.
- **Free account plan**: no charges for up to six months until you upgrade; it ends after six months or when credits are fully used, whichever is first. It lacks some services that would burn the credits quickly, and has only Always Free offers active.
- **Paid account plan**: credits apply first; beyond the credit balance, or for services where credits do not apply, you pay standard pay-as-you-go prices. May have short-term trials and Always Free offers active.
- Offer types: Always Free (ongoing monthly allowance) and short-term trials (start when you activate the service). Browse them on the AWS Free Tier page.
- Credit amounts change; re-read the Free Tier page and FAQs before relying on them.

## 2. Track usage
```bash
aws freetier get-free-tier-usage --region us-east-1
```
- Free plan: expiry date, credit balance and days remaining show in the Billing console widget, console home, or via SDK/CLI, plus periodic email alerts.
- Paid plan: credits balance and expiry are on the Credits page; usage against trial and Always Free limits is on the Free Tier page and the free tier API.
- Free Tier usage alerts email the account root address when usage exceeds 85 percent of a service's Free Tier limit. They are automatic for individual accounts but a management account in AWS Organizations must opt in (Billing preferences, Alert preferences, Receive AWS Free Tier alerts). The email address is changeable in the same place.
- Alerts cover services with an active offer in the current month (page examples: first 25 GB of DynamoDB storage, first 10 custom CloudWatch metrics). Free Tier data may not show for Organizations member accounts, GovCloud Regions, services with no Free Tier, or an expired Free Tier.

## 3. Budgets from templates
In the Billing and Cost Management console: Budgets, Create budget, Use a template (simplified). Templates:
- Zero spend budget: notifies after spending exceeds Free Tier limits.
- Monthly cost budget: notifies when you exceed, or are forecast to exceed, the amount.
- Daily Savings Plans coverage budget and Daily reservation utilization budget.
Under Template settings choose JSON to download the template for CLI or CloudFormation use. For 100% of a Free Tier limit per service, use a usage budget filtered to that service.

## 4. CloudWatch billing alarm
1. Enable billing alerts once: Billing preferences, Alert preferences, Edit, Receive CloudWatch Billing Alerts. About 15 minutes later the data appears. You must be root or an IAM user permitted to view billing; for consolidated billing enable it in the payer account; APN accounts do not publish billing metrics. You cannot disable data collection afterwards.
2. Set the Region to US East (N. Virginia), where billing metrics are stored (they represent worldwide charges). Metric: Billing, Total Estimated Charge, `EstimatedCharges`, USD only.
3. The page's settings: statistic Maximum, period 6 hours, static threshold, Greater, 1 out of 1 datapoints, missing data treated as missing, notify an SNS topic on In alarm.
```bash
aws cloudwatch put-metric-alarm --region us-east-1 --alarm-name billing-over-5usd \
  --namespace AWS/Billing --metric-name EstimatedCharges --dimensions Name=Currency,Value=USD \
  --statistic Maximum --period 21600 --evaluation-periods 1 --threshold 5 \
  --comparison-operator GreaterThanThreshold --alarm-actions arn:aws:sns:us-east-1:<ACCOUNT_ID>:billing
```
The alarm triggers only when current billing exceeds the threshold; it does not use projections. If charges already exceed it at creation, it goes to ALARM immediately. Estimated charges are sent several times daily.

## Method
Rewritten from the four cited pages. The earlier claims about a July 2025 cutover, legacy 12-month tier details, surprise-cost sources, budget actions and Organizations free-tier sharing were not on the pages and were removed; the CLI command names were checked against the CLI models.

## Checked
Checked 2026-11-08 against the four cited pages (Free Tier overview, tracking Free Tier usage, CloudWatch billing alarm, budget templates).
Method: docs-only read of cited pages, 2026-11-08
