---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-alarm-evaluation-tuning-and-fatigue
name: cloudwatch-alarm-evaluation-tuning-and-fatigue
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, evaluation-periods, alarm-fatigue, m-out-of-n, alarm-tuning, slo-alerting]
level: practitioner
status: docs-checked
description: "Tune CloudWatch alarms so they page for real problems: period, evaluation periods and M-out-of-N, statistics and percentiles, thresholds from baselines, and reducing alarm noise."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/alarm-evaluation.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricAlarm.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch alarm evaluation tuning

## 1. The knobs
- **Period**: aggregation window per datapoint (10 s, 30 s for high-res; 60 s multiples).
- **Statistic**: `Average`, `Sum`, `Minimum`, `Maximum`, `SampleCount`, percentiles
  (`p99`), trimmed means (`tm99`).
- **Evaluation periods (N)** and **datapoints to alarm (M)**: alarm when M of the last N
  datapoints breach. M-out-of-N tolerates blips without long delays.
- **Threshold** and comparison; or anomaly detection band.
- **Missing data** treatment.
Time to alarm is at least M periods plus the delay before the metric is published.

## 2. Patterns that work
| Signal | Setup |
|---|---|
| Error rate | metric math `errors/requests*100`, period 60 s, 3 of 5 datapoints > 2% |
| Latency | `p99` (not Average) over 60 s, 5 of 5 > SLO; Average hides tail latency |
| Saturation (CPU) | Average 5 min, 3 of 3 > 80%; short CPU spikes are rarely actionable |
| Hard failure (health check, queue age) | 1 of 1 or 2 of 2 at 60 s; page fast |
| Low-traffic services | use `Sum` of errors rather than rate, or require minimum `SampleCount` with metric math `IF(requests > 50, errors/requests, 0)` |
| Disk/storage | threshold with enough lead time to act; an anomaly detection band for unusual change |
Base thresholds on observed baselines (two weeks of data, p99 of normal), not guesses.

## 3. Reducing fatigue
- Page only on **symptoms users feel** (errors, latency, availability, queue age); route
  causes (CPU, memory) to tickets/dashboards.
- **Composite alarms** combine: page when `error-rate AND NOT deploy-in-progress`, or when
  several regional alarms fire together; suppress children with
  `ActionsSuppressor` during known events.
- Use **alarm mute rules** for maintenance windows instead of disabling actions manually.
- Every alarm has an owner, runbook link (in `AlarmDescription`) and severity tag.
- Review weekly: alarms that fired without action needed get tuned or deleted.

## 4. Commands
```bash
aws cloudwatch put-metric-alarm --alarm-name checkout-5xx-rate \
  --metrics '[{"Id":"e","Expression":"100*m1/m2","Label":"5xx %","ReturnData":true},
     {"Id":"m1","MetricStat":{"Metric":{"Namespace":"AWS/ApplicationELB","MetricName":"HTTPCode_Target_5XX_Count","Dimensions":[{"Name":"LoadBalancer","Value":"app/web/abc"}]},"Period":60,"Stat":"Sum"},"ReturnData":false},
     {"Id":"m2","MetricStat":{"Metric":{"Namespace":"AWS/ApplicationELB","MetricName":"RequestCount","Dimensions":[{"Name":"LoadBalancer","Value":"app/web/abc"}]},"Period":60,"Stat":"Sum"},"ReturnData":false}]' \
  --evaluation-periods 5 --datapoints-to-alarm 3 --threshold 2 \
  --comparison-operator GreaterThanThreshold --treat-missing-data notBreaching \
  --alarm-description "Runbook: https://wiki/runbooks/checkout-5xx" --alarm-actions <sns>
aws cloudwatch describe-alarm-history --alarm-name checkout-5xx-rate --history-item-type StateUpdate
```
Alarm history shows how often it flapped: the main tuning input.

## Gotchas
- Percentile alarms need enough samples; with few requests p99 is noisy (`put-metric-alarm` has an `--evaluate-low-sample-count-percentile` setting for this case).
- Metrics published less often than every minute (for example daily metrics) need periods that match; do not alarm
  on 1-minute periods for them.
- Alarms on `AWS/DynamoDB` metrics always ignore missing data whatever `--treat-missing-data` says.
- `treat-missing-data breaching` on sparse metrics causes false alarms.

## Verify
- [ ] Each paging alarm has M-of-N tuned, runbook link, and fired correctly in a game day.
- [ ] Alarm history shows no flapping alarms over the last 30 days.
- [ ] Composite alarms or mute rules used for deploys/maintenance.

## Checked
Checked 2026-10-27 against the live CloudWatch docs (current release) and the botocore cloudwatch 2010-08-01 model.
- Alarm evaluation page: datapoints to alarm (M) of evaluation periods (N), non-consecutive breaching datapoints.
- Metrics concepts page: 10 s and 30 s high-resolution alarm periods; statistics page: percentile and tm forms.
- PutMetricAlarm API reference and botocore model: --metrics, --evaluation-periods, --datapoints-to-alarm, --threshold, --comparison-operator, --treat-missing-data (breaching, notBreaching, ignore, missing), --alarm-description, --evaluate-low-sample-count-percentile, DynamoDB missing-data note. DescribeAlarmHistory: StateUpdate history item type.
- PutCompositeAlarm API reference: ActionsSuppressor; PutAlarmMuteRule API reference: mute rules exist. Metric math page: IF and FILL functions.
- Removed unconfirmed claims: 1 to 3 minute metric delay, linear trend alarms, named delayed metrics.

Method: documentation only; no commands were run.
