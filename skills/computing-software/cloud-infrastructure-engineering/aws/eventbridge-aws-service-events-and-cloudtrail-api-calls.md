---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-aws-service-events-and-cloudtrail-api-calls
name: eventbridge-aws-service-events-and-cloudtrail-api-calls
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, aws-service-events, aws-api-call-via-cloudtrail, default-event-bus, event-patterns, cloudtrail]
level: practitioner
status: docs-checked
description: "React to AWS service events and API calls on the EventBridge default bus: detail-type patterns, the CloudTrail trail requirement, read-only management events and forwarding rules."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge: AWS service events and API calls via CloudTrail

**Goal:** trigger automation from things AWS does (instance state changes, Health events,
GuardDuty findings) and from API calls anyone makes (CreateBucket, AuthorizeSecurityGroupIngress).

## Two kinds of AWS events on the default bus
| Kind | `detail-type` example | Needs |
|---|---|---|
| Service events | `EC2 Instance State-change Notification`, `ECS Task State Change`, `AWS Health Event`, `GuardDuty Finding` | nothing, emitted by the service |
| API calls | `AWS API Call via CloudTrail` | an enabled CloudTrail trail with logging |

## Patterns
```json
{"source":["aws.ec2"],"detail-type":["EC2 Instance State-change Notification"],
 "detail":{"state":["stopped","terminated"]}}
```
```json
{"source":["aws.ec2"],"detail-type":["AWS API Call via CloudTrail"],
 "detail":{"eventSource":["ec2.amazonaws.com"],
           "eventName":["AuthorizeSecurityGroupIngress"],
           "requestParameters":{"ipPermissions":{"items":{"ipRanges":{"items":{"cidrIp":["0.0.0.0/0"]}}}}}}}
```
- Find exact field names by looking at a real event: CloudTrail event history JSON, or the
  EventBridge sandbox/"Sample events" in the console.
- For API-call events `source` is the service namespace (the docs example uses `aws.ec2`) and `detail.eventSource` is the endpoint (`ec2.amazonaws.com`).
- Other CloudTrail detail-types: `AWS Console Signin via CloudTrail`, `AWS Console Action via CloudTrail`, `AWS Service Event via CloudTrail`, `AWS Insight via CloudTrail`, `AWS Network Activity Event via CloudTrail`.

## Requirements and limits
- You must enable a CloudTrail trail with logging to get any CloudTrail detail-type events. All CloudTrail events are delivered to the default event bus only; to use a custom bus, forward matching events from a default-bus rule.
- Write (mutating) management events match rules in the default `ENABLED` state. Data events also match `ENABLED` rules, but the trail must capture those data event types. Network activity events need a trail with network activity event selectors and a call made through a VPC endpoint.
- **Read-only management events** match only rules whose state is `ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS`:
  `aws events put-rule --name reads --event-pattern file://p.json --state ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS`
  If you forward read-only events to another bus, both the forwarding rule and the destination rule need that state.
- The same occurrence can be reported twice (for example EC2 sends `EC2 Instance State-change Notification` and CloudTrail sends the `StartInstances` API call event).
- If you build a pattern from a `Put*Events` event, keep the pattern under 1 MB.
- Per the EventBridge troubleshooting page, API-call events from global services such as IAM and Route 53 are available only in US East (N. Virginia), so put those rules there. Delivery latency is not covered here; check the CloudTrail and EventBridge guides.

## Gotchas
- Look at a real event before writing the pattern; nested objects must mirror the event structure.
- A rule whose remediation calls the same API can loop; exclude your remediation role in the pattern.

## Verify
- [ ] Rule `test-event-pattern` passes against a captured real event.
- [ ] Trigger the action (stop a test instance / make the API call); target receives the event.

## Checked
2026-10-27. Documentation: Amazon EventBridge User Guide, AWS service events delivered via AWS CloudTrail, read this date. Confirmed: the six CloudTrail detail-type values, trail-with-logging requirement, default-bus-only delivery, rule state ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS for read-only management events (also on both rules when forwarding), write/data/network-activity matching rules, duplicate service and CloudTrail events, 1 MB pattern note. Confirmed from the API model: RuleState enum. Removed unconfirmed claims about us-east-1 global-service events, delivery latency, per-region scope, errorCode filtering and event-history behaviour.
Method: documentation only; no commands were run.
