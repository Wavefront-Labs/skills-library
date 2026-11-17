---
id: computing-software.cloud-infrastructure-engineering.aws.egress-filtering-domain-allowlists
name: egress-filtering-domain-allowlists
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, egress-filtering, domain-allowlist, egress-proxy, network-firewall, dns-firewall, data-exfiltration]
level: practitioner
status: docs-checked
description: "Restrict outbound internet to approved domains with Network Firewall domain lists, Route 53 DNS Firewall, or an explicit proxy, and build the allow-list from observed traffic."
sources: ["https://docs.aws.amazon.com/network-firewall/latest/developerguide/stateful-rule-groups-domain-names.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-dns-firewall.html", "https://aws.amazon.com/blogs/security/how-to-control-non-http-and-non-https-traffic-to-a-dns-domain-with-aws-network-firewall-and-aws-lambda/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Egress filtering with domain allow-lists

**Goal:** workloads can reach `pypi.org`, `api.stripe.com` and AWS APIs — nothing else —
limiting exfiltration and C2 callbacks.

## 1. Pick a layer (often two)
| Layer | Sees |
|---|---|
| **Route 53 Resolver DNS Firewall** | outbound DNS queries through the VPC Resolver; no view of traffic that skips it |
| **Network Firewall domain list** | TLS SNI (HTTPS) and HTTP Host (HTTP); no visibility into VPC Resolver queries |
An explicit proxy is a third option, not covered here. DNS Firewall (deny all but trusted domains)
and Network Firewall together can also do resolved IP validation: the `AWS_ROUTE_53_RESOLVED_DOMAIN`
target type checks that the destination IP was resolved for the domain.

## 2. Network Firewall domain list rule group
```bash
aws network-firewall create-rule-group --rule-group-name egress-allow --type STATEFUL --capacity <CAPACITY> \
  --rule-group '{"RulesSource":{"RulesSourceList":{"Targets":[".amazonaws.com","pypi.org",".pythonhosted.org","api.stripe.com"],"TargetTypes":["TLS_SNI","HTTP_HOST"],"GeneratedRulesType":"ALLOWLIST"}},"RuleVariables":{"IPSets":{"HOME_NET":{"Definition":["10.0.0.0/8"]}}}}'
```
A leading dot (`.example.com`) matches the domain and all its subdomains; `TLS_SNI` matches HTTPS
only and `HTTP_HOST` HTTP only. With the Allow action the firewall denies non-matching traffic of
that protocol only under default action order; under strict order that denial does not apply, so
add your own default drop. By default only traffic from the firewall VPC's CIDR is inspected: set
`HOME_NET` to include other VPC CIDRs (for example behind a transit gateway).

## 3. DNS Firewall
```bash
aws route53resolver create-firewall-domain-list --name allowed
aws route53resolver update-firewall-domains --firewall-domain-list-id <DOMAIN_LIST_ID> --operation ADD --domains <DOMAIN> <DOMAIN>
# rule group: ALLOW rule for the allowed list at a low priority number, then a BLOCK rule for all other domains
```
Rule actions are `ALLOW`, `BLOCK`, `ALERT`; a block can respond `NODATA`, `NXDOMAIN` or `OVERRIDE`.
Associate the rule group with each VPC (or use Firewall Manager across accounts in an organization).
`FirewallFailOpen` (`ENABLED` or `DISABLED`, set per VPC with `update-firewall-config`) controls
whether queries still resolve when the firewall cannot evaluate them.

## 4. Build the list from evidence
Run in alert-only mode first (the `Alert` action logs matching traffic without blocking by itself);
mine Network Firewall alert logs and DNS Firewall logs for distinct domains per workload; review; then enforce.

## Gotchas
- DNS Firewall can also block names of VPC endpoints and private hosted zones, so allow the ones you use explicitly.
- Do not combine Reject or Alert domain-list rule groups with Allow domain-list rule groups under default action order: the Allow group's default drop takes effect first.

## Verify
- [ ] `curl https://pypi.org` succeeds, `curl https://example.com` fails (and logs a drop/alert).
- [ ] `dig example.com` from a workload returns the configured block response with DNS Firewall enforcing.

## Checked
2026-10-28. Confirmed against the Network Firewall page "Domain name filtering" (TLS_SNI, HTTP_HOST, leading-dot wildcard, Allow behaviour under default versus strict order, HOME_NET default and override, resolved-domain target, rule-group combination warning), the Route 53 page "Using DNS Firewall to filter outbound DNS traffic" (scope, Network Firewall comparison, Firewall Manager, VPC endpoint names) and botocore (network-firewall GeneratedRulesType and TargetType; route53resolver UpdateFirewallDomains operations, rule actions, block responses, FirewallFailOpen). Removed unconfirmed claims: bypass-risk column, the 53/853 baseline, aws:drop_established, the managed malware list name, the 2-4 week window, CDN and certificate-pinning gotchas, and the domain format with trailing dots. The security blog was not relied on.
Method: documentation only; no commands were run.
