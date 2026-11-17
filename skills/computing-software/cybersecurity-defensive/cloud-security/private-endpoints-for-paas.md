---
id: computing-software.cybersecurity-defensive.cloud-security.private-endpoints-for-paas
name: private-endpoints-for-paas
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-network-security, private-endpoints, privatelink, vpc-endpoints, private-service-connect, public-network-access-disabled, private-dns-zones, data-exfiltration-prevention]
level: practitioner
status: draft
description: "Put PaaS services (storage, databases, key vaults) behind private endpoints with public access disabled, private DNS, endpoint policies and exfiltration controls."
sources: ["AWS Docs - AWS PrivateLink and VPC endpoint policies", "Microsoft Learn - Azure Private Link and private endpoint DNS configuration", "Google Cloud Private Service Connect and VPC Service Controls"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Private endpoints for PaaS

**Goal:** managed services holding data are reachable only from your networks, not from the
internet, and workloads cannot use the same private path to exfiltrate to other tenants' resources.

## AWS
- Gateway endpoints (S3, DynamoDB) and interface endpoints (most services, PrivateLink).
- **Endpoint policies** restrict which buckets/resources can be accessed through the endpoint (only your organisation's):
```json
{"Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:*","Resource":"*",
  "Condition":{"StringEquals":{"aws:ResourceOrgID":"o-abc123"}}}]}
```
- Bucket policies requiring `aws:SourceVpce` for sensitive buckets; RDS not publicly accessible.

## Azure
- Private endpoint per resource (storage, SQL, Key Vault, Cosmos DB, etc.), then **Public network access: Disabled** on the resource.
- **Private DNS zones** (`privatelink.blob.core.windows.net`, ...) linked to VNets; on-prem resolution via DNS forwarders / Private Resolver. DNS is where most deployments break.
- Azure Policy to deny public network access and require private endpoints.

## GCP
- Private Service Connect / Private Google Access; **VPC Service Controls** perimeters prevent data movement out of the perimeter even with valid credentials.

## Rollout
1. Create endpoint and DNS; verify resolution returns private IPs from all client networks (`nslookup mystorage.blob.core.windows.net`).
2. Switch clients; monitor access logs for public-path traffic.
3. Disable public access; keep firewall allow-lists only for exceptions with documented owners.

## Gotchas
- Portal/console data-plane operations from admin laptops fail once public access is disabled unless admins come through the private network.
- Services that need trusted Microsoft services or AWS service access (backups, logging) may need explicit exceptions.
- Endpoints without policies let compromised workloads reach any tenant's bucket over the private path.

## Verify
- [ ] Data-plane access from the internet returns denied/unreachable for each protected resource.
- [ ] Policy compliance shows public network access disabled across subscriptions/accounts.
