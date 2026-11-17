---
id: computing-software.cloud-infrastructure-engineering.aws.network-performance-monitoring-infrastructure-performance
name: network-performance-monitoring-infrastructure-performance
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, network-monitoring, infrastructure-performance, network-latency-metrics, ena, network-flow-monitor]
level: advanced
status: docs-checked
description: "Monitor network performance with Infrastructure Performance inter-Region/AZ latency subscriptions, ENA allowance counters and Network Flow Monitor."
sources: ["https://docs.aws.amazon.com/network-manager/latest/infrastructure-performance/what-is-nmip.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/enable-aws-network-performance-metric-subscription.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-network-performance-ena.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-NetworkFlowMonitor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network performance monitoring

## 1. Is it AWS's network? Infrastructure Performance
Infrastructure Performance (AWS Network Manager) gives near real-time and historical latency
between Regions, between AZs and within an AZ, with no data before 26 Oct 2022. It is an
overview of normal or degraded performance, not a root-cause tool, and it excludes paths
through VPC resources such as transit gateways, NAT gateways, VPC endpoints, load
balancers and network interfaces. There is no cost for Infrastructure Performance itself;
CloudWatch charges may apply to subscriptions.
```bash
aws ec2 enable-aws-network-performance-metric-subscription \
  --source us-east-1 --destination eu-west-1 --metric aggregate-latency --statistic p50
aws ec2 describe-aws-network-performance-metric-subscriptions
aws ec2 get-aws-network-performance-data --data-queries \
  'Id=q1,Source=use1-az1,Destination=use1-az2,Metric=aggregate-latency,Statistic=p50,Period=five-minutes' \
  --start-time 2026-10-17T00:00:00Z --end-time 2026-10-18T00:00:00Z
```
Source/destination are Regions or AZ IDs; with AZ IDs both must be in the same Region. The
only metric is `aggregate-latency` and the only statistic is `p50`. Periods are
`five-minutes`, `fifteen-minutes`, `one-hour`, `three-hours`, `one-day`, `one-week`.
Subscriptions publish to CloudWatch so you can graph AWS latency beside your app latency.

## 2. Is it the instance? ENA allowance counters
Needs ENA driver 2.2.10 or later on Linux (2.2.2 on Windows).
```bash
ethtool -S eth0
```
| Counter | Meaning |
|---|---|
| `bw_in_allowance_exceeded` / `bw_out_allowance_exceeded` | packets queued or dropped because inbound / outbound aggregate bandwidth exceeded the instance maximum |
| `pps_allowance_exceeded` | packets queued or dropped because bidirectional PPS exceeded the instance maximum |
| `conntrack_allowance_exceeded` | packets dropped because connection tracking exceeded the instance maximum |
| `linklocal_allowance_exceeded` | packets dropped because PPS to local proxy services (Amazon DNS, IMDS, Time Sync) exceeded the per-interface maximum; custom DNS resolvers unaffected |
| `conntrack_allowance_available` | tracked connections still available (Nitro only, driver 2.8.1+) |
Counters are cumulative since the last driver reset. Use them to size instances and plan
scaling. To send them to CloudWatch, install the CloudWatch agent.

## 3. Is it flows between my workloads? Network Flow Monitor
Network Flow Monitor uses lightweight agents installed on your instances (EC2 and EKS) to
collect statistics from TCP connections. Monitors show packet loss and latency and a
network health indicator (NHI) that says whether AWS network issues affected the
monitored flows, so you can decide between an AWS issue and a workload issue.

## Verify
- [ ] A dashboard shows Infrastructure Performance latency, ENA allowance counters and app latency together.
- [ ] An alarm exists on growth of `bw_out_allowance_exceeded`.

## Checked
Date: 2026-11-07
Method: documentation only; no commands were run.
Read in full: "What is Infrastructure Performance", the enable-aws-network-performance-metric-subscription
CLI reference page, "Monitor network performance for ENA settings" (all sections, incl. ENA
Express/DPDK/FreeBSD, which are not used here) and "Using Network Flow Monitor" (the overview
only; its child pages were not opened). `get-aws-network-performance-data` data-query members,
periods and the single metric/statistic were confirmed in the botocore model, not on a page.
Removed: "If AWS latency is flat while yours spikes, the problem is in your stack" (the page
says it does not cover VPC paths), "cache DNS locally", the CloudWatch agent "ethtool plugin"
name, and the TCP RTT/retransmission/data-transferred claims (page says packet loss, latency,
NHI). `ethtool -S` grep filter dropped.
