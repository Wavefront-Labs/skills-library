---
id: computing-software.cloud-infrastructure-engineering.google-cloud.firewall-rule-priority-and-implied-rules
name: firewall-rule-priority-and-implied-rules
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-firewall, firewall-rule-priority, implied-rules, firewall-policy-evaluation, goto-next]
level: practitioner
status: docs-checked
description: "Predict which GCP firewall rule wins: priority numbers, deny-wins ties, implied rules and always-allowed traffic, and evaluation order across hierarchical, network and VPC policies."
sources: ["https://cloud.google.com/firewall/docs/firewalls", "https://cloud.google.com/firewall/docs/firewall-policies-rule-eval-order", "https://cloud.google.com/firewall/docs/firewall-policies-overview", "https://cloud.google.com/sdk/gcloud/reference/compute/networks/update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall rule priority and implied rules

## 1. Within one VPC rule set
- Priority 0 (highest) to 65535 (lowest); default 1000.
- The highest-priority matching rule decides. At the **same** priority, a deny beats an allow.
- Rules are stateful: an allowed connection's return traffic is allowed regardless of rules.

## 2. Implied rules (last step of evaluation; can't be logged)
- **Implied allow egress** to any IP address.
- **Implied deny ingress** from any source.
Override them with explicit allow or deny rules. The **default** network also has pre-populated rules
(`default-allow-internal`, `-ssh`, `-rdp`, `-icmp`, priority 65534): delete them in real projects.

## 3. Always allowed / always blocked
- Always allowed: traffic between a VM and its metadata server 169.254.169.254 (DHCP, DNS resolution, instance metadata, NTP); VPC firewall rules and hierarchical policies do not apply to it.
- **Not** automatically allowed: load balancer health check probes. Add an ingress allow for the probe ranges in the firewall-rules-for-health-check-iap-and-google-ranges skill (35.191.0.0/16 for most backends).
- Blocked or limited by default regardless of rules: egress to TCP port 25 on external IP addresses (SMTP), unless external SMTP egress is allowed for the project. See "Blocked and limited traffic" in the docs.

## 4. Across policy types (default order, `AFTER_CLASSIC_FIREWALL`)
1. Hierarchical firewall policies: organisation, then folders (top-down). Actions: allow, deny, `goto_next`, `apply_security_profile_group`.
2. Regional system firewall policies (Google-managed, created when a Google service needs rules).
3. VPC firewall rules.
4. Global network firewall policies, then regional network firewall policies.
5. Implied actions.
`gcloud compute networks update VPC --network-firewall-policy-enforcement-order=BEFORE_CLASSIC_FIREWALL` moves VPC firewall rules after the network policies (step 3 after step 4).
A hierarchical **allow** is terminal: lower levels can't deny it. Use `goto_next` to delegate.

## Gotchas
- Two rules at priority 1000 (allow from 0.0.0.0/0 and deny from a bad range): deny wins only for traffic both match, and only because the priorities are equal. Give denies a lower number (higher priority) explicitly. Rules with the same priority and the same action give the same result, but which one is reported is indeterminate.
- Target tags/SAs: a rule with no target applies to all instances in the VPC.

## Verify
- [ ] `gcloud compute networks get-effective-firewalls VPC` or `gcloud compute instances network-interfaces get-effective-firewalls VM --zone=ZONE` lists the effective rules; Connectivity Tests names the deciding rule.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (firewalls page): priority range 0-65535, deny beats allow only at equal priority, stateful tracking, default-network rules at priority 65534, metadata server always allowed (DHCP, DNS, metadata, NTP), TCP 25 external egress blocked unless allowed.
- Confirmed (rule evaluation page): default AFTER_CLASSIC_FIREWALL order (hierarchical, regional system, VPC rules, global network, regional network, implied) and BEFORE_CLASSIC_FIREWALL; goto_next and apply_security_profile_group actions.
- Confirmed (gcloud reference): `networks update --network-firewall-policy-enforcement-order`, `networks get-effective-firewalls`, `instances network-interfaces get-effective-firewalls --zone`.
- Removed: the implied-rule priority number and ::/0 wording (not stated on the current pages) and the 130.211.0.0/22 range.

Method: documentation only; no commands were run.
