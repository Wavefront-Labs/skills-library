---
id: computing-software.cloud-infrastructure-engineering.aws.global-accelerator-creating-standard-accelerators
name: global-accelerator-creating-standard-accelerators
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, global-accelerator, accelerator-listener, port-ranges, ga-endpoint-types, internal-alb-endpoint, anycast]
level: practitioner
status: gated
description: "Build a Global Accelerator: listeners and port ranges, endpoint groups per region, ALB/NLB/EC2/EIP endpoints including internal ALBs, DNS and health behaviour."
sources: ["https://docs.aws.amazon.com/global-accelerator/latest/dg/getting-started.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-listeners.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups-health-check-options.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups-traffic-dial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a standard Global Accelerator

**What you get:** static IP addresses that act as a single point of contact for clients (two IPv4
addresses, or four for a dual-stack accelerator: two IPv4 and two IPv6). A standard accelerator
distributes traffic across healthy endpoints in the endpoint groups you configure.

## 1. Accelerator and listener
The commands below pass `--region us-west-2` for Global Accelerator API calls (gated: unconfirmed, source is paywalled or blocked).
```bash
GA=$(aws globalaccelerator create-accelerator --region us-west-2 --name app \
  --ip-address-type DUAL_STACK --enabled --query Accelerator.AcceleratorArn --output text)
L=$(aws globalaccelerator create-listener --region us-west-2 --accelerator-arn $GA \
  --protocol TCP --port-ranges FromPort=443,ToPort=443 FromPort=80,ToPort=80 \
  --client-affinity NONE --query Listener.ListenerArn --output text)
```
- `--ip-address-type` is `IPV4` or `DUAL_STACK`; listener protocol is `TCP` or `UDP`.
- A listener takes 1 to 10 port ranges, each port 1-65535.
- Client affinity `SOURCE_IP` sends all requests from one client source IP to the same endpoint
  resource; `NONE` is the other value.
- Port overrides on an endpoint group map a listener port to an endpoint port (up to 10); you cannot
  set a port override for health check ports.

## 2. Endpoint groups (one per region)
```bash
aws globalaccelerator create-endpoint-group --region us-west-2 --listener-arn $L \
  --endpoint-group-region eu-west-1 --traffic-dial-percentage 100 \
  --health-check-protocol TCP --health-check-port 443 --health-check-interval-seconds 10 \
  --threshold-count 3 \
  --endpoint-configurations EndpointId=<ALB_ARN>,Weight=128,ClientIPPreservationEnabled=true
```
Repeat for each region; each endpoint group is tied to one Region and a group takes up to 10 endpoint
configurations. Health check interval is 10 to 30 seconds, threshold count 1 to 10, protocol `TCP`, `HTTP`
or `HTTPS`. The **traffic dial** (0-100, default 100) controls the share of traffic a group receives;
a change applies only to new connections and does not affect health checks.

## 3. Endpoint types
Endpoints can be Network Load Balancers, Application Load Balancers, EC2 instances or Elastic IP
addresses; a resource must be valid and active when you add it. A dual-stack accelerator accepts only
dual-stack endpoints (NLB, ALB and EC2 instances can be dual-stack). Endpoint weight is 0-255.
Health evaluation by type:
- **ALB:** healthy if every target group has at least one healthy target.
- **NLB:** healthy if at least one Availability Zone is healthy (an AZ is healthy if it has a healthy target in all target groups it is in).
- **EC2 / Elastic IP:** health check options from the endpoint group apply. With a UDP listener the check uses TCP on the listener port, so run a TCP server on the endpoint, and allow the Route 53 health checker IP ranges.

## 4. Health and failover
Global Accelerator monitors all endpoints in a standard endpoint group and routes only to healthy,
active endpoints. If there are no healthy endpoints, it routes traffic to all endpoints in the Region's group.

## Gotchas
- Health check options set in Global Accelerator do not affect ALB/NLB endpoints; configure those with Elastic Load Balancing target group health checks.
- If the health check port differs from the listener port, review security groups so the port admits only the Route 53 health checker ranges.
- See the vendor pricing page for costs; none are stated here.

## Verify
- [ ] `aws globalaccelerator describe-endpoint-group --region us-west-2 --endpoint-group-arn <ARN>` shows every endpoint `HEALTHY`.
- [ ] After changing a traffic dial, new connections follow the new split while existing ones continue.

## Checked
2026-10-28: Confirmed against the Global Accelerator Developer Guide (about-listeners, about-endpoints, about-endpoint-groups-health-check-options, about-endpoint-groups-traffic-dial, disaster-recovery-resiliency) and the botocore globalaccelerator model (CreateAccelerator, CreateListener, CreateEndpointGroup: enums, port ranges 1-65535 and max 10, weight 0-255, interval 10-30, threshold 1-10, 10 endpoint configurations, 10 port overrides, traffic dial 0-100). Read end to end. Gated: the claim that API calls go to us-west-2 (no readable page states it; the commands still pass --region us-west-2). Removed as unconfirmed: anycast/edge wording, client IP preservation table, internal ALB and ENI/security group notes, DNS name format, Route 53 alias, BYOIP, 30 s failover time, pricing remark, delete-order remark.

Method: documentation only; no commands were run.
