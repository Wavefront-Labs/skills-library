---
id: computing-software.cloud-infrastructure-engineering.aws.global-accelerator-pricing-and-dt-premium
name: global-accelerator-pricing-and-dt-premium
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, global-accelerator, dt-premium, accelerator-pricing, data-transfer-costs]
level: practitioner
status: docs-checked
description: "Estimate and track Global Accelerator cost: hourly fixed fee plus Data Transfer-Premium per GB on the dominant direction, on top of normal data transfer."
sources:
  - https://aws.amazon.com/global-accelerator/pricing/
  - https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-pricing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global Accelerator pricing and DT-Premium

## 1. The parts of the bill
1. **Fixed fee** per accelerator per hour, charged for each provisioned accelerator whether
   enabled or disabled, until you delete it. The pricing page showed $0.025 per full or
   partial hour at the time of checking.
2. **Data Transfer-Premium (DT-Premium)**: an incremental per-GB charge on traffic in the
   **dominant direction** (inbound to your application or outbound to users), calculated
   hourly. The rate depends on the AWS Region serving the request (source) and the edge
   location where responses are directed (destination). Example from the page: US and Canada
   Regions to European edge locations at $0.015/GB.
3. Standard EC2 Data Transfer Out charges still apply in addition to DT-Premium for your
   application endpoints.
4. Standard public IPv4 address charges apply to IPv4 addresses used with accelerators.

## 2. Estimate
`hours x fixed fee + dominant-direction GB per source/destination pair x DT-Premium rate`,
plus normal data transfer and IPv4 charges. The pricing page works an example: a North
American accelerator running all month (about $18 fixed) with 6,000 GB of billable outbound
traffic comes to about $128 per month including DT-Premium. Model your top geographies from
load balancer logs and look up each pair's rate on the pricing page.

## 3. Operating tips
- Because the hourly fee accrues while the accelerator exists, even if disabled, delete test
  accelerators instead of leaving them disabled.
- Compare actual monthly Global Accelerator spend per accelerator in Cost Explorer against
  the estimate.

## Verify
- [ ] Monthly Global Accelerator spend per accelerator is compared with the estimate.

## Checked
Method: docs-checked 2026-11-09 against the AWS Global Accelerator pricing page and the developer guide pricing page, read via summarising fetch. Dropped unconfirmed: usage-type names, CloudWatch metric names, CloudFront-vs-Global-Accelerator guidance, the Asia-vs-North-America cost claim, and the 20% tolerance.
