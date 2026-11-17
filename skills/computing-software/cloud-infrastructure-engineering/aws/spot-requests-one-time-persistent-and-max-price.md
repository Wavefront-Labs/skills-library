---
id: computing-software.cloud-infrastructure-engineering.aws.spot-requests-one-time-persistent-and-max-price
name: spot-requests-one-time-persistent-and-max-price
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, spot-instances, spot-request, persistent-spot, max-price, interruption-behavior]
level: practitioner
status: docs-checked
description: "Launch Spot with one-time or persistent requests, pick interruption behaviour (terminate, stop, hibernate), avoid max-price pitfalls and clean up requests."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-requests.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/interruption-behavior.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-request-status.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-spot-instance-requests.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One-time and persistent Spot requests

## 1. Launch via run-instances
AWS documents `run-instances` for Spot as suitable only if you already launch On-Demand
this way and need one instance type. It is generally not recommended: you cannot give
multiple instance types or mix Spot and On-Demand. `request-spot-instances` is a legacy API
with no planned investment and is strongly discouraged. Preferred methods are fleets.
```bash
aws ec2 run-instances --launch-template LaunchTemplateName=worker,Version='$Latest' \
  --instance-market-options 'MarketType=spot,SpotOptions={SpotInstanceType=persistent,InstanceInterruptionBehavior=stop}'
```
| Type | After interruption |
|---|---|
| `one-time` (default) | the request is not resubmitted |
| `persistent` | the request is resubmitted to replenish the interrupted instance |

Interruption behaviour: default is terminate. `stop` requires a persistent request (and no
launch group); `hibernate` is also valid for persistent requests; one-time requests allow
only terminate. Keeping the default on a persistent request gives an error. A stopped
instance is restarted by EC2 when capacity is available in the same AZ for the same
instance type; while stopped you pay only for EBS volumes.

## 2. Max price
By default the Spot price applies, capped at the On-Demand price (console: "No maximum
price", the recommended choice). You are always charged the current Spot price whatever
maximum you set. A maximum price makes interruptions more frequent, and one below the
current Spot price means the instance will not launch. Leave it unset unless you need a cap.

## 3. Status codes
```bash
aws ec2 describe-spot-instance-requests --query 'SpotInstanceRequests[].{id:SpotInstanceRequestId,state:State,code:Status.Code,msg:Status.Message}'
```
Real codes include `capacity-not-available`, `price-too-low` (request stays open),
`instance-stopped-by-price`, `marked-for-stop` and `fulfilled`. Request states for the
`state` filter: open, active, closed, cancelled, failed.

## 4. Clean up persistent requests
Terminating a Spot Instance of a persistent request leaves the request open (closed only
for non-persistent requests), so cancel the request first. Cancelling does not stop running
instances (`request-canceled-and-instance-running`):
```bash
aws ec2 cancel-spot-instance-requests --spot-instance-request-ids sir-0abc
aws ec2 terminate-instances --instance-ids i-0abc
```

## 5. Prefer fleets for anything long-lived
AWS's preferred methods launch a fleet with multiple instance types, optionally mixing
Spot and On-Demand. See "Which is the best Spot request method to use?" in the EC2 User Guide.

## Verify
- [ ] No orphaned open requests: `describe-spot-instance-requests --filters Name=state,Values=open`.

## Checked
Date: 2026-11-07
Method: documentation only; no commands were run.
Read in full: Create a Spot Instance request (console, CLI, PowerShell tabs), Behavior of
Spot Instance interruptions, and Get the status of a Spot Instance request (full code list).
The describe-spot-instance-requests CLI page was searched for the `state` filter values, not
read in full; `MarketType`, `SpotOptions`, `SpotInstanceType`, `InstanceInterruptionBehavior`,
`LaunchTemplateName` and the response fields were confirmed in the botocore model.
Removed: "requires EBS root volumes", the "price-capacity-optimized" and ASG mixed-instances
recommendation (not on these pages), "never being fulfilled", and "run-instances preferred
over request-spot-instances" (the page discourages both).
