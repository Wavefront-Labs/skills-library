---
id: computing-software.cloud-infrastructure-engineering.aws.incident-manager-response-plans
name: incident-manager-response-plans
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, incident-manager, ssm-incidents, ssm-contacts, response-plan, incident-manager-plan, escalation-plan, on-call-schedule, runbook-automation, chatbot, incident-response, post-incident-analysis]
level: practitioner
status: docs-checked
description: "Set up Systems Manager Incident Manager: replication set, contacts and escalation, response plans fired by alarms or EventBridge with runbooks, chat and post-incident analysis."
sources: ["https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html", "https://docs.aws.amazon.com/incident-manager/latest/userguide/response-plans.html", "https://docs.aws.amazon.com/incident-manager/latest/userguide/contacts.html", "https://docs.aws.amazon.com/incident-manager/latest/userguide/incident-creation.html", "https://docs.aws.amazon.com/incident-manager/latest/userguide/analysis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident Manager response plans

**Goal:** a critical alarm opens an incident with the right impact level, pages the on-call
engineer (and escalates if nobody acknowledges), starts a diagnostic runbook, opens a chat
channel, and ends with a post-incident analysis — all defined as code.

## 0. Availability
Confirm Incident Manager is available to your account before building on it.

## 1. Foundations
```bash
aws ssm-incidents create-replication-set --regions '{"us-east-1":{},"us-west-2":{}}'   # data in 2 Regions for resilience
aws ssm-contacts create-contact --alias alice --display-name "Alice" --type PERSONAL --plan '{"Stages":[]}'
aws ssm-contacts create-contact-channel --contact-id <ALICE_ARN> --name sms --type SMS --delivery-address SimpleAddress=+15555550100
aws ssm-contacts activate-contact-channel --contact-channel-id <CH_ARN> --activation-code <CODE>
```
- **Contacts** have channels (email, SMS or voice) and an engagement plan; Incident Manager
  sends an activation code to each defined channel.
- **On-call schedules / rotations** (`create-rotation`; up to 30 contacts per rotation) and
  **escalation plans** (contact type `ESCALATION`) define who gets paged; add contacts and
  on-call schedules as the escalation channels.
- Activate each channel with its activation code.
- The replication set needs at least two Regions for Incident Manager to fail over and create
  incidents in another Region.

## 2. Response plan
```bash
aws ssm-incidents create-response-plan --name checkout-sev1 --display-name "Checkout outage" \
  --incident-template '{"title":"Checkout outage","impact":1,"summary":"Checkout error rate high",
     "dedupeString":"checkout-5xx","notificationTargets":[{"snsTopicArn":"arn:aws:sns:us-east-1:<ACCOUNT_ID>:incident-updates"}]}' \
  --engagements arn:aws:ssm-contacts:us-east-1:<ACCOUNT_ID>:contact/payments-escalation \
  --chat-channel '{"chatbotSns":["arn:aws:sns:us-east-1:<ACCOUNT_ID>:chatbot-incidents"]}' \
  --actions '[{"ssmAutomation":{"roleArn":"arn:aws:iam::<ACCOUNT_ID>:role/im-runbook","documentName":"Checkout-Diagnostics",
       "targetAccount":"RESPONSE_PLAN_OWNER_ACCOUNT","parameters":{"Cluster":["checkout"]},"dynamicParameters":{"IncidentARN":{"variable":"INCIDENT_RECORD_ARN"}}}}]'
```
- Impact is an integer from 1 to 5.
- The dedupe string prevents the same root cause from creating multiple incidents.
- Start runbooks (SSM Automation) with read-only diagnostics, not auto-fixes.
- Creating an incident also creates a parent OpsItem in OpsCenter linked to the incident.

## 3. Triggers
- **CloudWatch alarm action**: CloudWatch creates an incident from a response plan when
  an alarm goes into alarm state (see the incident-creation page for prerequisites).
- **EventBridge rule** target: the response plan.
- Manual: `aws ssm-incidents start-incident --response-plan-arn <ARN> --title "..."`.

## 4. During and after
- Add notes with `create-timeline-event`. Resolve with `update-incident-record --status RESOLVED` (statuses `OPEN`, `RESOLVED`).
- **Post-incident analysis** from a template (a set of root-cause questions; action items are
  OpsItems linked to the analysis and incident). Make the analysis mandatory for impact 1-2.

## Gotchas
- Keep `dedupeString` stable per plan so repeated triggers do not open many incidents.
- Test each responder's contact channel.

## Verify
- [ ] `aws cloudwatch set-alarm-state --alarm-name checkout-5xx --state-value ALARM --state-reason test` opens exactly one incident.
- [ ] On-call engineer receives the page; escalation reaches stage 2 when unacknowledged.
- [ ] Runbook runs; chat channel receives updates.
- [ ] Post-incident analysis created with action items for the test incident.

## Checked

2026-10-28. Confirmed against the Incident Manager user guide pages (contacts, response plans, incident creation, analysis) and the ssm-incidents / ssm-contacts botocore models: contact types PERSONAL/ESCALATION/ONCALL_SCHEDULE, channel types and activation codes, up to 30 contacts per rotation, replication set needing two Regions for failover, impact 1-5, dedupe string purpose, parent OpsItem creation, alarm-triggered incidents, analysis templates and OpsItem action items, incident status enum. Removed (unconfirmed): availability change note, specific engagement timings, RAM sharing, alarm action ARN form, timeline auto-recording, acknowledgement and runbook-role gotchas, SMS timing. Read end to end.

Method: documentation only; no commands were run.
