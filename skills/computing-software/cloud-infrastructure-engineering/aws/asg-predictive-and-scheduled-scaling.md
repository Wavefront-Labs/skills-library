---
id: computing-software.cloud-infrastructure-engineering.aws.asg-predictive-and-scheduled-scaling
name: asg-predictive-and-scheduled-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-scaling, predictive-scaling, scheduled-scaling, asg, forecast-only]
level: practitioner
status: docs-checked
description: "Add scheduled actions and predictive scaling policies to an EC2 Auto Scaling group, start predictive in forecast-only mode, and combine with dynamic scaling."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scheduled-scaling.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/scheduled-scaling-create-scheduled-action.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-predictive-scaling.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/predictive-scaling-policy-overview.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/predictive-scaling-create-policy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASG predictive and scheduled scaling

**Goal:** pre-provision capacity for load that is cyclical or known in advance, instead of reacting after metrics breach.

## Scheduled scaling (known events)
```bash
aws autoscaling put-scheduled-update-group-action --scheduled-action-name my-recurring-action \
  --auto-scaling-group-name my-asg --recurrence "0 9 * * *" --desired-capacity 3 \
  --time-zone "America/New_York"
```
One-off: `--start-time "2021-03-31T08:00:00Z" --desired-capacity 3` with no `--recurrence`.
- A scheduled action sets desired, minimum and maximum capacity at the given time; you can set just one, but include min and max when the desired value would fall outside current limits. Desired must be between min and max.
- Recurrence is a five-field cron expression: minute hour day-of-month month day-of-week. Default time zone is UTC; `--time-zone` takes IANA names, and location-based zones adjust for DST (Etc/UTC does not).
- With the CLI or SDK, start and end times must be in UTC. A start time runs the action then continues on the recurrence. An end time stops repetition and the action does not persist after it; a recurrence exactly at the end time is not run.
- Scale-out or scale-in is chosen by comparing current capacity to the new desired capacity. Scaling policies keep working after the action, but within the min and max the action set.
- Limits: action names unique per group; one action per scheduled time (a duplicate time is rejected); 125 scheduled actions per group. Identical cron expressions give undefined order. Actions can be delayed up to two minutes. Updates can change any setting except the name. Suspend the `ScheduledActions` process to turn them off without deleting.

## Predictive scaling (recurring load)
A scaling policy of type `PredictiveScaling` on a CloudWatch metric that has at least 24 hours of data. It analyses up to the past 14 days and produces an hourly forecast for the next 48 hours, updated every 6 hours. Two weeks of history gives better forecasts.
```bash
aws autoscaling put-scaling-policy --policy-name cpu40-predictive-scaling-policy \
  --auto-scaling-group-name my-asg --policy-type PredictiveScaling \
  --predictive-scaling-configuration file://config.json
```
config.json (forecast only, the default when `Mode` is omitted):
```json
{"MetricSpecifications":[{"TargetValue":40,"PredefinedMetricPairSpecification":{"PredefinedMetricType":"ASGCPUUtilization"}}]}
```
1. Start in forecast only; view forecasts with the `GetPredictiveScalingForecast` API (CLI `get-predictive-scaling-forecast`) or the console, and the console recommendations. Add `"Mode":"ForecastAndScale"` once satisfied. Several predictive policies per group are allowed, but only one can actively scale.
2. `ALBRequestCount` needs `ResourceLabel` set to the target group label and an attached Application Load Balancer target group. Console metrics: CPU, Network In, Network Out, ALB request count, or a custom metric pair.
3. By default it scales at the start of each hour for that hour's forecast. `SchedulingBufferTime` (console: Pre-launch instances) launches earlier. Enabling default instance warmup is strongly recommended.
4. In forecast-and-scale mode it only scales out; to remove capacity you need dynamic scaling policies. With several policies, each computes desired capacity and the maximum wins.
5. Max capacity: policies cannot exceed the group maximum by default. `"MaxCapacityBreachBehavior":"IncreaseMaxCapacity"` with `"MaxCapacityBuffer":10` allows a 10 percent buffer over predicted capacity (predicted 50, max 40 gives effective max 55). The raised maximum stays until you lower it manually.

## Gotchas
- A new group (for example after replacing the old one) needs 24 hours of data before forecasts resume; custom metrics can aggregate across old and new groups.
- Assumes a homogeneous group; forecasts can be wrong for mixed instance types when the metric depends on vCPUs or network bandwidth.
- Good fit: daily or weekly recurring patterns, batch or periodic workloads, slow-initialising applications.
- Custom metric queries must return data points; check with the CloudWatch console or GetMetricData. A wrong group name in a query gives an empty forecast.

## Checked
Date: 2026-11-07
Method: documentation only; no commands were run.
Read in full: "Scheduled scaling", "Create a scheduled action", "Predictive scaling", "How predictive scaling works" and "Create a predictive scaling policy". `get-predictive-scaling-forecast` is named from the GetPredictiveScalingForecast API on those pages, not from its own CLI page.
Removed: the sample `--min-size 4 --max-size 20` example values and `SchedulingBufferTime` 300 (the pages give no unit or value), the "raise min-size so scale-in cannot undo the pre-warm" advice, "never scales in below dynamic policies" wording, "Unconfirmed" note, and the root-only source.
