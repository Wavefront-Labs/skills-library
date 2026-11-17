---
id: computing-software.cloud-infrastructure-engineering.google-cloud.firewall-rules-logging
name: firewall-rules-logging
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-firewall, firewall-logging, firewall-rules-logging, firewall-insights, logs-explorer]
level: practitioner
status: docs-checked
description: "Turn on firewall rules logging for VPC rules and firewall policies, query allowed and denied connections in Logs Explorer, control cost with metadata and scope, and use Firewall Insights."
sources: ["https://cloud.google.com/firewall/docs/firewall-rules-logging", "https://cloud.google.com/firewall/docs/using-firewall-rules-logging", "https://cloud.google.com/network-intelligence-center/docs/firewall-insights/concepts/overview", "https://cloud.google.com/sdk/gcloud/reference/compute/firewall-rules/update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall rules logging

## 1. Enable per rule
```bash
gcloud compute firewall-rules update allow-ssh-iap --enable-logging --logging-metadata=exclude-all
gcloud compute network-firewall-policies rules update 1000 --firewall-policy=prod-fw --global-firewall-policy --enable-logging
```
- Logging is per rule; the **implied** deny-ingress/allow-egress rules can't log. To see denied traffic,
  add an explicit low-priority `deny all` ingress rule (priority 65534) with logging on.
- `--logging-metadata` accepts `exclude-all` or `include-all` (only with `--enable-logging`); omitting metadata fields saves storage cost.

## 2. Query
```
resource.type="gce_subnetwork"
logName="projects/PROJECT_ID/logs/compute.googleapis.com%2Ffirewall"
```
Add `resource.labels.subnetwork_name="SUBNET_NAME"` to narrow to one subnet. Each entry records the disposition (allow or deny) and the matching rule.

## 3. Firewall Insights
Network Intelligence Center → Firewall Insights reports shadowed rules, overly permissive rules (including allow rules with no hits or unused attributes) and deny rules with no hits during the observation period. Use it to find dead rules.

## Gotchas
- Firewall policy rules logging records only TCP and UDP connections, written when a connection is established (not per packet); it is not a packet capture.
- VPC firewall rules logging can incur cost, so use it selectively: log denies and sensitive allows.
- Logs go to the project that hosts the network containing the VMs; for Shared VPC look in the host project.

## Verify
- [ ] A blocked test connection shows up as a deny entry with the expected rule.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (firewall policy rules logging overview): implied deny ingress and implied allow egress rules cannot be logged; only TCP and UDP connections are recorded, per connection not per packet.
- Confirmed (using logging page): Logs Explorer query with resource.type gce_subnetwork and the compute.googleapis.com%2Ffirewall log name; logs live in the host project for Shared VPC; metadata fields are optional to save storage cost.
- Confirmed (gcloud reference): `firewall-rules update --enable-logging --logging-metadata` (exclude-all or include-all) and `network-firewall-policies rules update --enable-logging` with `--global-firewall-policy`.
- Confirmed (Firewall Insights overview): shadowed rule, overly permissive and no-hit insights. Removed: the jsonPayload field names (not documented on the pages read).

Method: documentation only; no commands were run.
