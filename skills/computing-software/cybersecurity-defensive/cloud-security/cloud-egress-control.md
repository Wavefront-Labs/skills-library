---
id: computing-software.cybersecurity-defensive.cloud-security.cloud-egress-control
name: cloud-egress-control
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-egress-control, egress-filtering, fqdn-filtering, nat-gateway, vpc-service-controls, data-exfiltration-prevention, cloud-network-security]
level: practitioner
status: draft
description: "Control outbound traffic from cloud workloads: central egress with FQDN allow-lists, private endpoints for cloud APIs, blocking IMDS-free exfil paths, and monitoring egress."
sources: ["https://docs.aws.amazon.com/network-firewall/latest/developerguide/stateful-rule-groups-domain-names.html", "https://learn.microsoft.com/en-us/azure/firewall/fqdn-filtering-network-rules", "https://cloud.google.com/vpc-service-controls/docs/overview", "https://cloud.google.com/secure-web-proxy/docs/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud egress control

Most cloud workloads have unrestricted internet egress by default (NAT gateway + allow-all egress rules),
which makes exfiltration, C2 and crypto-mining trivial.

## Design
1. **Central egress** through an inspection point: AWS Network Firewall (domain lists via SNI/Host), Azure Firewall (application rules with FQDN, FQDN tags for Windows Update/AKS), GCP Secure Web Proxy or Cloud NGFW with FQDN objects.
2. **Default deny** outbound; allow-list per workload: package repositories (or a mirror/proxy like Artifactory), SaaS APIs, partner endpoints.
3. **Private endpoints** for cloud provider APIs (VPC endpoints/PrivateLink, Private Endpoints, Private Google Access) so S3/Blob/GCS traffic does not need internet - and restrict them with endpoint policies to your own accounts/buckets (blocks exfil to attacker-owned buckets via the same service).
4. **Perimeter for managed services:** GCP VPC Service Controls (blocks copying data to projects outside the perimeter), AWS RCPs/endpoint policies with `aws:ResourceOrgID`, Azure storage network rules and private link.
5. Security groups/NSGs restrict egress at the instance level as a second layer.

## Endpoint policy example (S3 gateway endpoint)
```json
{"Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:*","Resource":"*",
  "Condition":{"StringEquals":{"aws:ResourceOrgID":"o-abc123"}}}]}
```

## Monitoring
VPC flow logs to unknown destinations, DNS logs (Route 53 Resolver query logs, DNS Firewall), firewall
alert logs; alert on new destinations from servers.

## Gotchas
- SNI-based filtering can be evaded with domain fronting on some CDNs; TLS inspection or strict allow-lists plus certificate checks help.
- Kubernetes pods share node egress IPs; use network policies/Cilium FQDN policies for per-workload control.

## Verify
- [ ] From a workload, `curl https://example.org` fails while allow-listed domains work.
- [ ] Copy to an external account's bucket via the endpoint is denied.
