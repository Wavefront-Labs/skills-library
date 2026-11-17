---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.attack-surface-management
name: attack-surface-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, security-foundations, attack-surface-management, external-exposure, asset-discovery, easm]
level: practitioner
status: docs-checked
description: "Manage the cloud attack surface: inventory exposed assets from inside, discover unknowns from outside with EASM, reconcile owners, fix dangling DNS and review reachability."
sources: ["https://learn.microsoft.com/azure/external-attack-surface-management/overview", "https://docs.aws.amazon.com/inspector/latest/user/findings-types.html", "https://owasp.org/www-project-amass/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attack surface management

## Steps
1. **Inventory exposure from the inside**: public IPs, load balancers, API gateways, CDN distributions, storage with public access and security groups allowing 0.0.0.0/0, across all accounts using cloud asset inventory queries.
2. **Discover from the outside**: external attack surface management (EASM) finds assets that are not in your accounts.
   - Microsoft Defender EASM starts from known legitimate assets (discovery seeds), recursively follows observed connections and infers relationships, and indexes what it finds (domains, IP address blocks, hosts, email contacts, ASNs, Whois organisations) as recent or historic assets.
   - OWASP Amass is an open source Apache 2.0 framework for network mapping of attack surfaces and external asset discovery using open source intelligence and reconnaissance techniques.
3. **Reconcile**: every exposed asset needs an owner and a reason; investigate unknowns.
4. **Dangling DNS**: a CNAME that still points at a deleted cloud resource (storage, app service, CDN) is a takeover risk; scan zones for records that point at unclaimed endpoints and remove the record when you delete the resource. (Practitioner guidance, not a vendor claim.)
5. **Review network reachability**: Amazon Inspector network reachability findings flag open network paths to EC2 instances, where TCP and UDP ports are reachable from VPC edges such as an internet gateway (including behind load balancers), a VPC peering connection or a VPN. They highlight overly permissive security groups, network ACLs or gateways. Inspector scans every 12 hours once enabled, and only for EC2 instances. Package vulnerability findings cover EC2 instances, ECR images and Lambda functions.
6. **Reduce** with private endpoints, removing public IPs and restricting admin ports, and enforce with preventive policy.
7. **Keep it continuous**: scheduled discovery and alerting on new public exposure. Defender EASM dashboards summarise vulnerabilities, compliance and security hygiene.

## Gotchas
- Deleting a resource but leaving its DNS record is the common takeover vector.
- Test and dev environments are the usual shadow exposure.
- Defender EASM resources cannot be accessed across tenants, including through Azure Lighthouse.

## Verify
- [ ] Every internet-exposed asset has an owner and justification.
- [ ] Dangling DNS scan clean.

## Checked
2026-11-08. Confirmed on the Defender EASM overview (discovery seeds, asset kinds, dashboards, cross-tenant limit), the Amazon Inspector finding types page (package vulnerability scope, network reachability, 12-hour scan, EC2 only) and the OWASP Amass project page (purpose, Apache 2.0). Removed: the Google Security Command Center attack exposure source (404), the Defender CSPM and SCC attack-path claim, certificate transparency logs and generic WAF/CDN advice (no source), and the claim that Amass does DNS enumeration (the page says network mapping and asset discovery).
Method: documentation only; no commands were run.
