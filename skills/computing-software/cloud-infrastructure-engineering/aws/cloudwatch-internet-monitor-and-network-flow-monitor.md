---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-internet-monitor-and-network-flow-monitor
name: cloudwatch-internet-monitor-and-network-flow-monitor
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, internet-monitor, network-flow-monitor, network-observability, health-events, tcp-retransmissions]
level: practitioner
status: gated
description: "See network problems outside and inside AWS: Internet Monitor for user-to-app internet health by city and ASN, and Network Flow Monitor agents for workload TCP flows."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-InternetMonitor.what-is-cwim.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-IM-inside-internet-monitor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internet Monitor and Network Flow Monitor

## Internet Monitor: users to your application
```bash
aws internetmonitor create-monitor --monitor-name web \
  --resources arn:aws:ec2:eu-west-1:111122223333:vpc/vpc-0abc \
              arn:aws:cloudfront::111122223333:distribution/E123 \
  --traffic-percentage-to-monitor 100 \
  --health-events-config AvailabilityScoreThreshold=95,PerformanceScoreThreshold=95 \
  --internet-measurements-log-delivery 'S3Config={BucketName=im-logs,LogDeliveryStatus=ENABLED}'
```
- Resources: VPCs, CloudFront distributions, Network Load Balancers and WorkSpaces directories (the docs note that VPCs, NLBs and WorkSpaces directories do not include last-mile latency).
- Uses AWS's global network measurements for the **city-networks** (client location + ASN, typically an ISP) your traffic comes from.
- **Health events** are raised when availability or performance scores drop; both global and local health events are sent to EventBridge. Measurements for the top 500 city-networks are also published to CloudWatch Logs every five minutes.
- Cap what is monitored with `--max-city-networks-to-monitor` (1 to 500000) or `--traffic-percentage-to-monitor` (1 to 100); see the Internet Monitor pricing page for cost.

Use it to answer "is it us or the internet?" during customer-reported slowness in one country or ISP.

## Network Flow Monitor: inside your VPCs
Network Flow Monitor uses agents on your workloads to report TCP flow statistics inside your VPCs. Read the Network Flow Monitor section of the CloudWatch User Guide for agent installation, the metrics it reports and the monitor scopes (gated: unconfirmed, source is paywalled or blocked).

## When to use which
| Question | Tool |
|---|---|
| Users in one region/ISP see errors | Internet Monitor |
| Service-to-service latency or packet loss between instances/AZs | Network Flow Monitor |
| Is traffic reaching a resource (allowed/denied) | VPC Flow Logs, Reachability Analyzer |

## Verify
- [ ] Internet Monitor shows client city-networks; a test EventBridge rule receives health events.
- [ ] Network Flow Monitor agents report flow metrics for a test pair.

## Checked

2026-10-28. Confirmed against: CloudWatch Internet Monitor pages (what it is, how it works: city-networks and ASNs, EventBridge health events, CloudWatch Logs publication of top 500 city-networks every five minutes, S3 publication, availability and performance scores, resource types) and the botocore CreateMonitor model (MonitorName, Resources, MaxCityNetworksToMonitor 1-500000, TrafficPercentageToMonitor 1-100, HealthEventsConfig thresholds, InternetMeasurementsLogDelivery S3Config); the CLI commands passed check_commands.

Removed or rewritten: the aws.internetmonitor event source string, cause-attribution wording, dashboard suggestions, cost statement, and all Network Flow Monitor specifics (agent types, metrics, setup steps), which could not be checked from fetched pages.

Gated: the Network Flow Monitor description is only a pointer to the User Guide and its specifics were not confirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
