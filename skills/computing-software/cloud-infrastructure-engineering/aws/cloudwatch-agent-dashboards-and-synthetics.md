---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-agent-dashboards-and-synthetics
name: cloudwatch-agent-dashboards-and-synthetics
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-agent, dashboards, synthetics, canaries, cloudwatch-synthetics, statsd, collectd, procstat, memory-metrics, disk-metrics, container-insights, application-signals, rum, cross-account-observability, oam, dashboard-json, heartbeat-canary, api-canary]
level: practitioner
status: draft
description: "Collect host metrics and logs with the CloudWatch agent (memory, disk, procstat), build dashboards as code with cross-account views, and probe endpoints with Synthetics canaries."
sources: ["Amazon CloudWatch User Guide - Collect metrics, logs and traces with the CloudWatch agent", "Amazon CloudWatch User Guide - Using Amazon CloudWatch dashboards", "Amazon CloudWatch User Guide - Using synthetic monitoring (Synthetics canaries)", "Amazon CloudWatch User Guide - CloudWatch cross-account observability"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CloudWatch agent, dashboards and Synthetics — see inside the box and outside the door

**Goal:** EC2/on-prem hosts report memory, disk and process metrics plus application logs;
one dashboard per service built from JSON in IaC; canaries hit the real user path every
minute and alarm before customers call.

## 1. CloudWatch agent
Install via SSM (`AWS-ConfigureAWSPackage` → `AmazonCloudWatchAgent`) or the package; config in
SSM Parameter Store so fleets share it:
```json
{"agent":{"metrics_collection_interval":60,"run_as_user":"cwagent"},
 "metrics":{"namespace":"Host","append_dimensions":{"InstanceId":"${aws:InstanceId}","AutoScalingGroupName":"${aws:AutoScalingGroupName}"},
   "aggregation_dimensions":[["AutoScalingGroupName"]],
   "metrics_collected":{
     "mem":{"measurement":["mem_used_percent"]},
     "disk":{"measurement":["used_percent"],"resources":["/","/data"],"ignore_file_system_types":["tmpfs","devtmpfs"]},
     "procstat":[{"pattern":"nginx","measurement":["cpu_usage","memory_rss","pid_count"]}],
     "statsd":{"service_address":":8125"}}},
 "logs":{"logs_collected":{"files":{"collect_list":[
   {"file_path":"/var/log/app/*.json","log_group_name":"/prod/app","log_stream_name":"{instance_id}","timestamp_format":"%Y-%m-%dT%H:%M:%S","retention_in_days":30}]}}}}
```
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c ssm:AmazonCloudWatch-linux
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
tail /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log
```
- Instance role: `CloudWatchAgentServerPolicy` (+ `ssm:GetParameter` on the config).
- `aggregation_dimensions` gives ASG-level metrics without per-instance cardinality cost;
  drop `InstanceId` from `append_dimensions` for big fleets if per-host is not needed.
- Windows: `LogicalDisk`, `Memory`, `Paging File` counters; Event Log collection in `logs`.
- The agent also ships **OpenTelemetry/X-Ray traces** and **Application Signals** data
  (`traces` section) and runs on-prem with an IAM user/role via `-m onPremise`.
- Container Insights (ECS/EKS) uses the agent as a DaemonSet/sidecar; EKS add-on
  `amazon-cloudwatch-observability` is the current path.

## 2. Dashboards as code
```bash
aws cloudwatch put-dashboard --dashboard-name prod-api --dashboard-body file://dash.json
```
- Body: `widgets[]` with `type` (`metric`, `log`, `alarm`, `text`, `explorer`), `x/y/width/height`
  (24 columns), `properties.metrics` arrays (`["AWS/ApiGateway","Latency","ApiName","shop",{"stat":"p99"}]`),
  metric math `[{"expression":"m2/m1*100","label":"error %"}]`, `annotations` for SLO lines.
- Layout rule: top row = user-facing (requests, error rate, p99), middle = saturation
  (CPU/mem/connections), bottom = dependencies and logs widget with an Insights query.
- `period` auto vs fixed; `stat` per metric; `view: "singleValue"` for KPIs; `region` per
  widget for multi-region in one board.
- **Cross-account observability** (OAM): a monitoring account sinks metrics/logs/traces from
  source accounts (`oam:CreateSink` + link); dashboards then reference `"accountId"` in the
  metric array. Share read-only dashboards via Cognito or a public link (avoid).
- Keep dashboards in CDK (`cloudwatch.Dashboard` + `GraphWidget`) or Terraform; console edits get overwritten.

## 3. Synthetics canaries
- Runtime `syn-nodejs-puppeteer-*` / `syn-nodejs-playwright-*` / `syn-python-selenium-*`;
  blueprints: **heartbeat** (load URL, screenshot), **API canary** (HTTP steps with
  assertions), broken link checker, visual monitoring (screenshot diff), GUI workflow.
- Schedule `rate(1 minute)` for prod front doors, `rate(5 minutes)` for internal APIs;
  run from a VPC (subnets/SG) to test private endpoints.
- Metrics `SuccessPercent`, `Duration`, `Failed`; alarm `SuccessPercent < 100` for 2 of 3
  datapoints. Artifacts (HAR, screenshots, logs) to S3 with lifecycle rules.
- Multi-step API example:
  ```js
  const synthetics = require('Synthetics');
  exports.handler = async () => {
    await synthetics.executeHttpStep('login', {hostname:'api.example.com', method:'POST', path:'/login', ...}, (res) => { if (res.statusCode !== 200) throw new Error(`login ${res.statusCode}`); });
    await synthetics.executeHttpStep('cart', {...});
  };
  ```
- Identify canary traffic by `User-Agent` (`CloudWatchSynthetics`) and exclude it from
  business metrics / rate limits; use a dedicated test account in the app.
- Cost: per run; 1-min canaries ≈ 43 k runs/month each — keep the count small and the
  steps meaningful. Each canary is a Lambda in your account (IAM role, logs).

## 4. RUM and Application Signals (when you need more)
- **CloudWatch RUM**: JS snippet collects page load, JS errors, Core Web Vitals per route/browser.
- **Application Signals**: auto-instrumented services (Java/Python/.NET/Node) report
  latency/error/fault per operation with SLOs and dependency maps — a lighter path than hand-built dashboards.

## Gotchas
- Agent config in Parameter Store must be *fetched* (`fetch-config`) — editing the parameter
  does nothing until the agent re-fetches (State Manager association on a schedule fixes this).
- `mem_used_percent` on Linux counts cache as free; `used_percent` for disk ignores reserved blocks — thresholds ~85/90 %.
- Dashboards do not alarm; the `alarm` widget only shows state. Pair with composite alarms.
- Canaries in a VPC need a NAT or endpoints for `monitoring`, `s3`, `logs` or they fail silently with timeouts.
- Puppeteer runtimes deprecate on a schedule; pin and plan upgrades (canary fails with runtime-unsupported).
- Unconfirmed: current canary runtime names and Application Signals language coverage — check the console.

## Verify
- [ ] `amazon-cloudwatch-agent-ctl -a status` → running; `Host` namespace shows `mem_used_percent` for the instance.
- [ ] Disk-full test (fallocate a big file) raises `used_percent` within one interval and trips the alarm.
- [ ] Dashboard JSON is applied from IaC; manual console edits are overwritten on next deploy.
- [ ] Canary fails when the endpoint returns 500 (temporarily point it at a failing path) and the alarm pages within 3 min.
- [ ] Monitoring account dashboard shows metrics from a linked source account.
