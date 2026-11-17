---
id: computing-software.cybersecurity-defensive.cloud-security.route53-resolver-dns-firewall
name: route53-resolver-dns-firewall
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-network-security, route53-dns-firewall, dns-filtering, aws-managed-domain-lists, firewall-manager, dns-exfiltration, vpc]
level: practitioner
status: docs-checked
description: "Filter VPC DNS with Route 53 Resolver DNS Firewall: managed and custom domain lists, rule priorities, test domains, Network Firewall pairing and Firewall Manager rollout."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-dns-firewall.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-dns-firewall-managed-domain-lists.html", "https://docs.aws.amazon.com/waf/latest/developerguide/dns-firewall-policies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route 53 Resolver DNS Firewall

DNS Firewall filters outbound DNS queries from VPCs that route through the Route 53 VPC Resolver. A primary use is preventing DNS exfiltration, where a compromised instance sends data out via lookups to an attacker domain. You can deny known-bad domains and allow the rest, or deny everything except explicitly trusted domains. It can also block resolution of private hosted zone names, VPC endpoint names and EC2 instance names. No extra Resolver setup is needed.

## Building blocks
- **Rule groups**: reusable collections of filtering rules, associated to VPCs; activity is visible in DNS Firewall logs and metrics. Rules reference domain lists; blocked queries can return custom responses.
- **AWS managed domain lists** (free, auto-updated, can't be viewed or edited, available in listed Regions): malware (`AWSManagedDomainsMalwareDomainList`), botnet/C2 (`AWSManagedDomainsBotnetCommandandControl`), aggregate threat list (`AWSManagedDomainsAggregateThreatList`, includes the others) and GuardDuty threat list (`AWSManagedDomainsAmazonGuardDutyThreatList`, tied to specific GuardDuty domain-reputation findings). They are not a replacement for GuardDuty or other controls.
- Log records name the rule group, action and managed list (`firewall_domain_list_id`).

## Rollout practice (from the managed-lists page)
Test a managed list in non-production first with the rule action set to `Alert`; evaluate with CloudWatch metrics plus sampled requests or logs, then change the action. AWS provides test domains per list (for example `controldomain1.malwarelist.firewall.route53resolver.us-east-1.amazonaws.com`); unblocked, they resolve to 1.2.3.4, blocked they return the rule's block response (for example NODATA).

False positives: find the rule group and list in the Resolver logs, add a rule with your own domain list that allows the domain, and give it a lower numeric priority than the blocking rule so it runs first.

## Network Firewall
DNS Firewall sees DNS queries via the VPC Resolver; Network Firewall filters network and application traffic but cannot see Resolver queries. They can be combined for resolved IP validation: Network Firewall checks that the VPC Resolver returned a connection's destination IP.

## Firewall Manager at scale
Firewall Manager DNS Firewall policies create rule group associations across accounts and VPCs in an organisation, and automatically add associations for VPCs that come into scope. Requirements: resource sharing enabled with AWS Organizations, and rule groups already defined in the Firewall Manager admin account. The policy sets "first" rule groups (priority 1-99) and "last" (9,901-10,000); account owners' own associations run between them. Associations are named `FMManaged_<policy id>`. Overrides by account owners make the policy non-compliant.

## Verify
Querying a test domain from an instance returns the block response and produces a log entry; an `Alert` rule logs without blocking.

## Checked
Method: 2026-11-08 read the three cited pages in full. Rewrote to the pages. Dropped as unsupported by these pages: DNS Firewall Advanced (DGA/tunnelling), the FirewallFailOpen setting and its default, the CLI sequence, the walled-garden recipe, hybrid outbound-endpoint behaviour, external-resolver/DoH bypass advice and the `srcids.instance` log field. Managed-list names and basic rule-group behaviour unchanged.
