---
id: computing-software.cybersecurity-defensive.cloud-security.gcp-hierarchical-firewall-policies
name: gcp-hierarchical-firewall-policies
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [gcp-firewall-policies, hierarchical-firewall-policy, vpc-firewall, network-firewall-policy, secure-tags, cloud-network-security]
level: practitioner
status: docs-checked
description: "GCP Cloud NGFW firewall policies: hierarchical org/folder policies and goto_next, secure tags vs network tags, rule logging scope and caveats."
sources: ["https://docs.cloud.google.com/firewall/docs/firewall-policies-overview", "https://docs.cloud.google.com/firewall/docs/firewall-policies", "https://docs.cloud.google.com/firewall/docs/tags-firewalls-overview", "https://docs.cloud.google.com/firewall/docs/firewall-rules-logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCP hierarchical firewall policies

## Policy types
Cloud NGFW has four firewall policy types: hierarchical, global network, regional network and regional system (Google-managed; you can only change logging). Within a policy, higher-priority rules always take precedence. Regional system policy rules are evaluated immediately after hierarchical policy rules.

## Hierarchical policies
- Created at the organisation or folder level (not projects); creating one does nothing until it is **associated**. A policy can be associated with several resources, but a resource has only one policy. Swapping policies replaces rules atomically; avoid changing hierarchy and associations at the same time because of propagation delay.
- Applies to all VMs in all networks under the org or folder. Evaluation is top-down: org rules first, then the first folder level, and so on. **Lower-level rules cannot override higher-level rules.**
- Actions: `allow`, `deny`, `goto_next` (hand evaluation to lower-level policies or VPC network firewall rules; with targeting it creates exceptions for specific networks) and `apply_security_profile_group` (Layer 7 inspection via a firewall endpoint, for example intrusion prevention or URL filtering). Each new policy has predefined lowest-priority rules that pass unmatched connections down.
- Targets: VPC networks and service accounts, not instance tags. Rules can use secure tag keys as source or target. A rule uses IPv4 or IPv6 ranges, not both.
- IAM: create/modify needs `roles/compute.orgFirewallPolicyAdmin`; associating needs `roles/compute.orgSecurityResourceAdmin` on the target plus a policy admin or user role.
- Practical consequence: a broad `allow` at org or folder level cannot be tightened lower down; use `goto_next` unless the allow is final.

## Secure tags vs network tags
- **Secure tags** are Resource Manager tags under IAM control (Tag Admin creates, Tag User binds to VMs or uses in rules). Supported in hierarchical, global and regional network policies, not VPC firewall rules. Hierarchical policies accept only tag keys whose `purpose-data` specifies an organisation. Key needs `purpose=GCE_FIREWALL`; limits include 1,000 values per key, 10 tag values per VM network interface, one value per key per instance.
- **Network tags** are plain strings with no access controls, usable only in VPC firewall rules.

## Logging
- Enabled per rule, for hierarchical, global network, regional network and regional system policies. Not supported for implied rules or legacy networks.
- Only TCP and UDP connections are logged, in Cloud Logging, with IPs, ports, protocol, time and the matching rule. Allowed connections are logged once; denied traffic per unique 5-tuple, repeating every 5 seconds.
- Connections already active when logging is enabled are not logged until idle 10 minutes. Long-lived streams give one entry; use VPC Flow Logs for continuous visibility. Rule protocol cannot be `ALL` for logging.
- `apply_security_profile_group` logging is session-based and does not capture all sessions.

## Verify
- [ ] The VM's network interface details page shows the expected org-level rules.
- [ ] Logging enabled on deny rules; a test connection produces an entry.

## Checked
Method: 2026-11-08 read the four cited pages (now docs.cloud.google.com) in full. Removed unsupported claims: the full evaluation order including VPC rules, network policies and implied rules and the `networkFirewallPolicyEnforcementOrder` flag, all gcloud command examples, the 100/200 priority example and IAP range, `get-effective-firewalls`, Firewall Insights, and the claim that anyone editing a VM can set network tags. goto_next and hierarchy behaviour unchanged.
