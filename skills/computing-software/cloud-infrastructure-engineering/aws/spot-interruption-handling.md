---
id: computing-software.cloud-infrastructure-engineering.aws.spot-interruption-handling
name: spot-interruption-handling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, spot-instances, spot-interruption, rebalance-recommendation, interruption-handling, capacity-rebalancing, graceful-shutdown]
level: practitioner
status: docs-checked
description: "Handle Spot interruptions gracefully: two-minute notices via IMDS and EventBridge, rebalance recommendations, ASG Capacity Rebalancing, draining, checkpointing and FIS testing."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/rebalance-recommendations.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-capacity-rebalancing.html", "https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html", "https://karpenter.sh/docs/concepts/disruption/", "https://raw.githubusercontent.com/aws/aws-node-termination-handler/main/README.md", "https://raw.githubusercontent.com/aws/amazon-ecs-agent/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling Spot interruptions

## 1. Signals
| Signal | When | Where |
|---|---|---|
| **Rebalance recommendation** | elevated risk; may arrive earlier than, or together with, the interruption notice | IMDS `/latest/meta-data/events/recommendations/rebalance`, EventBridge `EC2 Instance Rebalance Recommendation` |
| **Interruption notice** | 2 minutes before stop/terminate (hibernate: notice only, no 2-minute lead) | IMDS `/latest/meta-data/spot/instance-action`, EventBridge `EC2 Spot Instance Interruption Warning` |

Poll IMDS every 5 s on the instance:
```bash
TOKEN=$(curl -sX PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 300')
while sleep 5; do
  code=$(curl -s -o /tmp/ia -w '%{http_code}' -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/spot/instance-action)
  [ "$code" = 200 ] && { logger "spot interruption: $(cat /tmp/ia)"; /usr/local/bin/drain.sh; break; }
done
```

## 2. What drain should do (in < 2 min)
- Deregister from load balancer target groups (keep the target group deregistration delay well inside the 2-minute window).
- Stop taking new work (stop polling SQS; in-flight messages return after visibility timeout).
- Checkpoint long jobs to S3; flush logs.
- Kubernetes: AWS Node Termination Handler (Queue Processor) or Karpenter's native interruption
  handling cordons and drains the node. ECS: set `ECS_ENABLE_SPOT_INSTANCE_DRAINING=true`.

## 3. Auto Scaling Capacity Rebalancing
```bash
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web --capacity-rebalance
```
On a rebalance recommendation, the ASG launches a replacement first, then terminates the
at-risk instance (running lifecycle hooks) — proactive rather than reactive. Pair with a
termination lifecycle hook for draining.

## 4. Test it
AWS FIS action `aws:ec2:send-spot-instance-interruptions` sends a real rebalance + interruption
notice to chosen instances (`durationBeforeInterruption` 2 to 15 minutes). Run it in a game day.

## Gotchas
- Interruption behaviour `stop`/`hibernate` (persistent requests) vs `terminate`.
- The 2-minute notice is best effort; design for sudden loss anyway (stateless workers, idempotent jobs).
- Don't use Spot for single-instance stateful services without a failover plan.

## Verify
- [ ] FIS interruption experiment: the instance drains, LB shows target `draining`, no 5xx spike, replacement launched.
- [ ] EventBridge rule records interruption warnings to a log/metric for rate tracking.
- [ ] Batch jobs resume from checkpoint after interruption.

## Checked

Checked 2026-10-28 against the EC2 Spot interruption notices and rebalance recommendation pages, the EC2 Auto Scaling Capacity Rebalancing page, the AWS FIS actions reference, the Karpenter disruption page and the Node Termination Handler and ECS agent READMEs.
- Confirmed: two-minute notice, best effort, 5-second polling advice, IMDS paths `spot/instance-action` and `events/recommendations/rebalance`, EventBridge detail types, FIS `aws:ec2:send-spot-instance-interruptions` and its 2 to 15 minute `durationBeforeInterruption`, Capacity Rebalancing launch-then-terminate behaviour and lifecycle hooks, Karpenter interruption handling.
- Corrected: hibernation gets a notice without the two-minute lead; rebalance recommendations can arrive together with the notice.
- Removed: the 90 s deregistration figure and the claim that terminate is the default interruption behaviour for fleets and ASGs.

Method: documentation only; no commands were run.
