---
id: computing-software.cloud-infrastructure-engineering.aws.asg-scaling-on-sqs-backlog-per-instance
name: asg-scaling-on-sqs-backlog-per-instance
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-scaling, backlog-per-instance, custom-metric-scaling, metric-math, sqs, target-tracking, consumer-scaling]
level: advanced
status: docs-checked
description: "Scale an EC2 worker fleet on SQS backlog per instance with target tracking on a metric-math expression, choosing the target from processing time and latency goals."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-target-tracking-metric-math.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-metrics.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Scaling workers on SQS backlog per instance

**Why not queue depth alone:** `ApproximateNumberOfMessagesVisible` of 1,000 means very
different things for 2 workers and 200 workers. Track **backlog per instance** =
visible messages / in-service instances, against a target derived from how fast one
instance processes messages.

## 1. Pick the target value
- Measure average processing time per message per instance, e.g. 0.2 s, with 10
  concurrent consumers per instance: throughput 50 msgs/s per instance.
- Decide acceptable latency (how long a message may wait), e.g. 20 s.
- Acceptable backlog per instance = latency / time per message = 20 / (0.2/10) = 1,000.
That 1,000 is the target-tracking target value.

## 2. Target tracking with metric math (no custom publisher needed)
```json
{
  "TargetValue": 1000,
  "CustomizedMetricSpecification": {
    "Metrics": [
      {"Id": "m1", "ReturnData": false, "Label": "visible",
       "MetricStat": {"Metric": {"Namespace": "AWS/SQS", "MetricName": "ApproximateNumberOfMessagesVisible",
         "Dimensions": [{"Name": "QueueName", "Value": "jobs"}]}, "Stat": "Sum"}},
      {"Id": "m2", "ReturnData": false, "Label": "inservice",
       "MetricStat": {"Metric": {"Namespace": "AWS/AutoScaling", "MetricName": "GroupInServiceInstances",
         "Dimensions": [{"Name": "AutoScalingGroupName", "Value": "workers"}]}, "Stat": "Average"}},
      {"Id": "e1", "ReturnData": true, "Label": "backlog per instance",
       "Expression": "m1 / IF(m2 > 0, m2, 1)"}
    ]
  }
}
```
```bash
aws autoscaling enable-metrics-collection --auto-scaling-group-name workers --granularity 1Minute
aws autoscaling put-scaling-policy --auto-scaling-group-name workers \
  --policy-name backlog-tt --policy-type TargetTrackingScaling \
  --target-tracking-configuration file://tt.json
```
Group metrics collection must be on for `GroupInServiceInstances` (group metrics are off by default and free at one-minute granularity once enabled). The docs example uses `m1 / m2`; the `IF` (a CloudWatch metric math function) guards against divide-by-zero when the group is at 0.

## 3. Scaling from zero
Target tracking cannot compute a ratio meaningfully at 0 instances with the expression
above (it treats in-service as 1, so backlog = visible, and scales out once visible
exceeds the target). If any message must start a worker immediately, add a step scaling
policy on `ApproximateNumberOfMessagesVisible >= 1` when the group is at 0, or keep min 1.

## 4. Tuning
- Target tracking is driven by CloudWatch alarms over several periods, so expect a delay of minutes before capacity changes.
- `DefaultInstanceWarmup` so new instances are not counted before they consume.
- Scale-in protection for instances mid-job: workers call
  `set-instance-protection --protected-from-scale-in` while processing a long job and clear
  it afterwards, or use lifecycle hooks to drain.
- Visibility timeout longer than max processing time, otherwise scale-in plus timeouts
  cause duplicate processing.

## Gotchas
- `ApproximateNumberOfMessagesVisible` excludes in-flight messages; a fleet working hard
  on long jobs shows low backlog. Add `ApproximateNumberOfMessagesNotVisible` if jobs are long.

## Verify
- [ ] The metric math expression graphs sensibly in CloudWatch (backlog per instance).
- [ ] Load test: enqueue a burst; group scales out until backlog per instance approaches the target, then scales in after drain.
- [ ] No messages exceed max receive count due to scale-in interruptions.

## Checked

Checked 2026-10-27 against the Amazon EC2 Auto Scaling User Guide (SQS backlog per instance, target tracking with metric math, group metrics) and the CloudWatch metric math documentation.
- Confirmed: metric names and namespaces (`ApproximateNumberOfMessagesVisible`, `GroupInServiceInstances`), Sum/Average statistics, `put-scaling-policy` with `TargetTrackingScaling`, backlog-per-instance target calculation, scale-in protection pattern, metric math `IF(condition, trueValue, falseValue)`.
- Removed: unsupported statements about SQS metric lag, ECS and Lambda consumers, and FIFO consumer limits.

Method: documentation only; no commands were run.
