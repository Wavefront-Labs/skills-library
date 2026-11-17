---
id: computing-software.cloud-infrastructure-engineering.aws.route53-traffic-flow-policies
name: route53-traffic-flow-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, route53, traffic-flow, traffic-policy, policy-records, geoproximity]
level: advanced
status: docs-checked
description: "Build Route 53 Traffic Flow policies that nest failover, latency, geo and weighted rules, version them, and attach them to names with policy records."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/traffic-flow.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/traffic-policies.html", "https://docs.aws.amazon.com/cli/latest/reference/route53/create-traffic-policy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route 53 Traffic Flow

**Use when** routing needs nesting (latency between Regions, then failover inside each, then weighted
across endpoints) that would otherwise be many hand-linked records.

## 1. Policy document
A traffic policy is a JSON document (rules and endpoints, with a start rule) that you can build in
the Traffic Flow visual editor or write by hand against the traffic policy document format in the
Route 53 API Reference. The fastest correct start is to build the tree in the visual editor, then
export the document with `aws route53 get-traffic-policy --id <ID> --version 1` and keep it in
version control. Typical nesting: geolocation or latency at the top, failover inside each branch,
weighted across endpoints at the leaves.

## 2. Create, version, attach
```bash
TP=$(aws route53 create-traffic-policy --name web --document file://policy.json --query TrafficPolicy.Id --output text)
aws route53 create-traffic-policy-instance --hosted-zone-id Z123 --name www.example.com --ttl 60 \
  --traffic-policy-id $TP --traffic-policy-version 1
aws route53 create-traffic-policy-version --id $TP --document file://policy-v2.json
aws route53 update-traffic-policy-instance --id <INSTANCE_ID> --ttl 60 --traffic-policy-id $TP --traffic-policy-version 2
```
The policy record (instance) creates and owns the records for that name; do not hand-edit them.

## 3. Cost and alternatives
Traffic policies themselves are free to create; there is a monthly charge for each traffic policy record
(see the Traffic Flow section of Route 53 pricing). Alias records in a hosted zone can reference a policy
record to reduce that charge. For a single routing type, plain records with routing policies are enough
(geoproximity is also a record-level routing policy).

## Verify
- [ ] `aws route53 get-traffic-policy-instance --id <ID>` shows `State: Applied`.
- [ ] `dig www.example.com` from two continents returns the expected Regional endpoints.

## Checked

Checked 2026-10-27 against the Route 53 Developer Guide (Traffic Flow, traffic policies, geoproximity), the aws-cli route53 reference and the botocore route53 model.
- Confirmed: create-traffic-policy, create-traffic-policy-version, create-traffic-policy-instance and update-traffic-policy-instance parameters; instance `State` value Applied; monthly charge per traffic policy record, policies themselves free, alias records can reference a policy record.
- Removed: the hand-written policy document, because the document-format reference page could not be read; the skill now points to the visual editor and `get-traffic-policy` export instead.

Method: documentation only; no commands were run.
