---
id: computing-software.cloud-infrastructure-engineering.aws.route53-health-check-types
name: route53-health-check-types
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, route53, calculated-health-check, health-check-alarm, endpoint-health-check, string-matching, failover-routing]
level: practitioner
status: docs-checked
description: "Choose and configure Route 53 health checks: endpoint (HTTP/HTTPS/TCP, string match), calculated parent checks, CloudWatch-alarm checks for private resources, and alerting."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-types.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-creating-values.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/monitoring-cloudwatch.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/route-53-ip-addresses.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route 53 health check types

## 1. Endpoint health checks
Health checkers in multiple regions probe your endpoint.
```bash
aws route53 create-health-check --caller-reference $(date +%s) --health-check-config '{
  "Type": "HTTPS_STR_MATCH", "FullyQualifiedDomainName": "api.example.com", "Port": 443,
  "ResourcePath": "/health", "SearchString": "\"status\":\"ok\"",
  "RequestInterval": 10, "FailureThreshold": 3, "MeasureLatency": true,
  "Regions": ["us-east-1","eu-west-1","ap-southeast-1"], "EnableSNI": true}'
```
- Types: `HTTP`, `HTTPS`, `HTTP_STR_MATCH`, `HTTPS_STR_MATCH`, `TCP`.
- HTTP/HTTPS: TCP connect within 4 s and a 2xx/3xx status within 2 s after connecting; TCP
  checks need a connection within 10 s; string match must find the string entirely in the first
  5,120 bytes of the body (body received within 2 s of the status).
- Interval 30 s (standard) or 10 s (fast; an additional charge applies and the interval cannot
  be changed after creation). Failure threshold 1-10.
- Healthy = more than 18% of checkers report healthy (so a few regions failing do not flip it).
- HTTPS checks do **not** validate the certificate.
- The endpoint must be reachable from the internet; allow Route 53 checker IP ranges
  (`ip-ranges.json`, service `ROUTE53_HEALTHCHECKS`) in SGs/WAF. Checker `Regions` must be chosen
  from the eight health-check Regions (`us-east-1`, `us-west-1`, `us-west-2`, `eu-west-1`,
  `ap-southeast-1`, `ap-southeast-2`, `ap-northeast-1`, `sa-east-1`).
- With the "Enable SNI" option the endpoint's certificate must match the domain name, or the check can fail even though certificate validity is otherwise not checked.
- Point at a deep `/health` that checks dependencies only if failing over actually helps;
  a shared dependency failing everywhere causes all records to fail (Route 53 then treats
  all as healthy, "fail open").

## 2. Calculated health checks
A parent check that is healthy when at least N of its child checks are healthy:
```bash
aws route53 create-health-check --caller-reference calc-$(date +%s) --health-check-config '{
  "Type": "CALCULATED", "ChildHealthChecks": ["hc-web-a","hc-web-b","hc-db"],
  "HealthThreshold": 2, "Inverted": false}'
```
A parent can monitor up to 255 child checks (Route 53 quotas page, read 2026-10-27; an account has 200 active health checks by default). Use it to fail a region only when several components fail, or to add
a manual "maintenance switch" child (an inverted check you toggle).

## 3. CloudWatch alarm health checks
For **private** resources (internal ALB, on-prem service via VPN) that health checkers
cannot reach, base health on a CloudWatch alarm:
```bash
aws route53 create-health-check --caller-reference cw-$(date +%s) --health-check-config '{
  "Type": "CLOUDWATCH_METRIC",
  "AlarmIdentifier": {"Region": "eu-west-1", "Name": "internal-alb-unhealthy-hosts"},
  "InsufficientDataHealthStatus": "LastKnownStatus"}'
```
The alarm must use standard-resolution metrics (high-resolution metrics are not supported), must
not use metric math across multiple metrics, and must be in the same account (cross-account alarms
are not supported). Route 53 reads the alarm's data stream, so `SetAlarmState` cannot force the
check. Choose `InsufficientDataHealthStatus` carefully (`Healthy`, `Unhealthy`, `LastKnownStatus`).

## 4. Attaching to records
- Failover, weighted, latency, geolocation and multivalue records take `HealthCheckId`.
- Alias records to ELB/CloudFront etc. use **Evaluate Target Health** instead of (or in
  addition to) a health check.
- Health checkers sit outside your VPC: for private hosted zone records either give the endpoint
  a public IP or base the check on a CloudWatch alarm.

## 5. Alerting on the check itself
Health checks publish `HealthCheckStatus` (1/0) and `HealthCheckPercentageHealthy` in
**us-east-1** (US East N. Virginia; the metrics are not available in other Regions). Create alarms there:
```bash
aws cloudwatch put-metric-alarm --region us-east-1 --alarm-name api-hc \
  --namespace AWS/Route53 --metric-name HealthCheckStatus \
  --dimensions Name=HealthCheckId,Value=<id> --statistic Minimum --period 60 \
  --evaluation-periods 2 --threshold 1 --comparison-operator LessThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:<ACCOUNT_ID>:oncall
```

## Gotchas
- Prefer checking each regional endpoint directly (IP or regional hostname) rather than the shared name the records answer for.
- A disabled child check (`Disabled: true`) is treated as healthy by a calculated parent unless you also invert it.
- A new check is considered healthy until Route 53 has enough data (unhealthy if inverted).
- Check Route 53 pricing for optional features (fast interval and others); prices are not stated here.

## Verify
- [ ] `aws route53 get-health-check-status --health-check-id <id>` shows checker regions reporting Success.
- [ ] Breaking the endpoint (return 500) turns the check unhealthy within interval x threshold and DNS fails over.
- [ ] us-east-1 alarm on `HealthCheckStatus` notifies on-call.

## Checked

Checked 2026-10-27 against the Route 53 Developer Guide (health check types and values, how health is determined, private hosted zone failover, CloudWatch metrics, IP ranges, quotas) and the botocore route53 2013-04-01 model.
- Corrected: CloudWatch-alarm health checks do not support high-resolution metrics, metric-math alarms over several metrics or cross-account alarms; a calculated parent monitors up to 255 children (quotas page; the values page says 256).
- Confirmed: 4 s connect plus 2 s response (TCP 10 s), 5,120-byte string match, more than 18% of checkers healthy, intervals 10/30 s, failure threshold 1-10, the eight health-check Regions, HTTPS checks do not validate certificates, `ROUTE53_HEALTHCHECKS` ranges, metrics only in US East (N. Virginia), `HealthCheckStatus` and `HealthCheckPercentageHealthy`.
- Removed: unconfirmed claims that private hosted zone records may use only calculated or alarm checks and that health checks resolve through Route 53 itself; placeholder account ID in the alarm ARN.

Method: documentation only; no commands were run.
