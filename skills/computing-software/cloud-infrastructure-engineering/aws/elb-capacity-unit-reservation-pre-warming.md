---
id: computing-software.cloud-infrastructure-engineering.aws.elb-capacity-unit-reservation-pre-warming
name: elb-capacity-unit-reservation-pre-warming
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-load-balancing, lcu-reservation, pre-warming, capacity-planning, alb]
level: advanced
status: docs-checked
description: "Reserve a minimum ALB or NLB capacity with LCU reservations before launches, spikes or migrations: sizing from PeakLCUs or ProcessedBytes, request, status, update and cancel."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/application/capacity-unit-reservation.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/request-capacity-unit-reservation.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/update-capacity-unit-reservation.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/monitor-capacity-unit-reservation.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/capacity-unit-reservation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LCU capacity reservation (pre-warming)

An LCU reservation sets a static minimum capacity for a load balancer. It keeps scaling up and down with traffic as usual but
never drops below the minimum. The pages suggest it for an event with a sudden unusual traffic spike, short unpredictable
spikes, a service cut-over at a fixed start time, or migrating between load balancers and matching the source's scale.

## 1. Size it
- Load test, or review historical data that represents the expected traffic. The console can estimate from a reference period.
- ALB: the pages recommend the `PeakLCUs` metric (a per-minute Sum), not `ConsumedLCUs`, which covers only the billing
  dimensions.
- NLB: capacity is reserved in LCUs of 2.2 Mbps each; take Max of `ProcessedBytes` per minute and convert at 2.2 Mbps = 1 LCU.
- Without data, the pages point to the LCU reservation calculator, built from AWS-observed workloads that may not match yours.
- Minimum request: ALB at least 100 LCU; NLB at least 2,750 LCU per Availability Zone. The maximum comes from your account quotas.
- NLB reservations are available only in the Regions the NLB page lists (ten at the time of reading, including us-east-1,
  us-east-2, us-west-2, eu-west-1, eu-central-1).

## 2. Request (ALB page)
```bash
aws elbv2 modify-capacity-reservation --load-balancer-arn <LB_ARN> \
  --minimum-load-balancer-capacity CapacityUnits=100
aws elbv2 describe-capacity-reservation --load-balancer-arn <LB_ARN>
```
- Capacity is reserved at Region level and spread evenly across Availability Zones, so have enough evenly distributed targets
  in each AZ first.
- Requests are first come, first served and depend on available capacity in the zone. Most complete within minutes but can
  take up to a few hours, so request well ahead.
- To update, the previous request must be `provisioned` or `failed`. Increases are unlimited; decreases are allowed twice a day.
- You pay for reserved or provisioned capacity until it is cancelled.

## 3. Status and monitoring
- Status values: `pending`, `provisioned`, `failed`, `rebalancing` (an AZ was added or removed).
- `ReservedLCUs` is reported per minute but reserved hourly: a reservation of 6,000 gives 6,000 per hour and 100 per minute.
  Compare the per-minute Sum of `PeakLCUs` with the reservation, or the hourly Sum of `ReservedLCUs`, with CloudWatch alarms.

## 4. Update or cancel
Status must be `provisioned`. In the console use Edit LCU Reservation or Cancel Capacity on the Capacity tab; in the CLI:
```bash
aws elbv2 modify-capacity-reservation --load-balancer-arn <LB_ARN> --reset-capacity-reservation
```

## Gotchas
- This skill does not cover backend scaling; the reservation applies only to the load balancer.
- The NLB request, update and monitor pages were not opened; the CLI above comes from the ALB pages and the botocore
  `ModifyCapacityReservation` input, which is not ALB specific.

## Verify
- [ ] `describe-capacity-reservation` shows `provisioned` before the event.

## Checked
Date: 2026-11-07. Read in full: ALB "Capacity reservations" overview, "Request reservation", "Update or cancel
reservation", "Monitor reservation" (CloudFormation tab of the request page was empty in the stripped text), and NLB
"Capacity reservations" overview. Botocore elbv2 `ModifyCapacityReservation` checked for the flag names.
Removed because no page read states them: the 10x spike framing, the dimension list for sizing, "billed whether used or
not" wording beyond the stated charges, "NLB reservations are spread across enabled AZs" (NLB request page unread),
`RejectedConnectionCount` and `HTTPCode_ELB_5XX_Count` monitoring, 24-hour lead time, warm-ASG advice, and failure reasons
appearing in `describe-capacity-reservation`.
Method: documentation only; no commands were run.
