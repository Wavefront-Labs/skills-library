---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.regional-independence
name: regional-independence
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, fault-isolation, regional-independence, global-dependencies, region-isolation, multi-region, global-services]
level: advanced
status: docs-checked
description: "Keep regions independent: find global and cross-region dependencies (identity, DNS, config, registries, CI/CD), localise them and test a region-isolation scenario."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/global-services.html", "https://learn.microsoft.com/azure/well-architected/reliability/redundancy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regional independence and avoiding global dependencies

The AWS fault isolation boundaries paper explains that a small set of AWS services are global:
the control plane lives in a single Region while the data plane is distributed. If your recovery
path calls a global control plane (create, update, delete, list operations), a failure in that
Region can block recovery.

## Dependencies to check (AWS)
| Dependency | Risk | Mitigation (from the paper) |
|---|---|---|
| Partitional services: IAM, Organizations, Account Management (control plane us-east-1); Route 53 ARC, Network Manager (us-west-2) | Control-plane operations unavailable if that Region has an event | Rely on data-plane operations in the recovery path, not the control plane |
| Edge services: Route 53 public DNS, CloudFront, Global Accelerator and others | Same | Same; Route 53 record changes, Global Accelerator traffic-dial changes and CloudFront origin changes are listed as failover anti-patterns |
| Resources that create Route 53 records on provisioning (ELB, API Gateway, PrivateLink endpoints, ElastiCache, OpenSearch and others) | Creating them during recovery depends on the Route 53 control plane in us-east-1 | Pre-provision them |
| S3 bucket creation, deletion and configuration changes; Multi-Region Access Point control plane | Depend on us-east-1 (MRAP: us-west-2) | Pre-provision buckets with their configuration; MRAP failover controls use the data plane |
| STS default global endpoint | SDK and CLI default to us-east-1 | Configure the SDK and CLI to use Regional STS endpoints |
| SAML sign-in and an IdP hosted on AWS | IdP may be impaired in the same event | Accept SAML logins from multiple Regions in trust policies; pre-provision break-glass users |

## Steps
1. Inventory every endpoint each Region calls, and which of your recovery steps need a control-plane
   call (the paper's anti-patterns include editing Route 53 records, creating or updating IAM
   roles and policies, and creating ELBs or RDS instances during failover).
2. For each global dependency decide: pre-provision, move to the data plane, or accept the risk.
3. Cache control-plane data needed for recovery in a data store reached through its data plane,
   such as an SSM Parameter Store parameter, a DynamoDB table or an S3 bucket, optionally in
   another Region. For Route 53 ARC, hardcode or bookmark the five Regional cluster endpoints.
4. Use static stability: design so a failure needs no control-plane change to fail over.
5. Azure's guidance for the same goal: global services such as Microsoft Entra ID, Azure DNS and
   Key Vault provide redundancy transparently; with deployment stamps, make each stamp a
   complete, self-sufficient deployment that can handle its workload independently.

## Gotchas
- A "multi-region" app whose pipelines, images or secrets exist only in the primary Region has a
  hidden dependency; the sources do not name specific registry or key features, so check your own
  provider's documentation for replication options.

## Verify
- [ ] Recovery runbook contains no step that calls a global control plane.
- [ ] A region-isolation game day has been run and found no hidden dependency.

## Checked
2026-11-08. Confirmed against the AWS fault isolation boundaries "Global services" page (control
plane locations, STS default endpoint, SAML regional endpoints, break-glass users, S3 and Route 53
dependencies, anti-patterns, caching in data-plane stores, ARC cluster endpoints) and the Azure
Well-Architected redundancy page (global services with built-in redundancy, deployment stamps).
Removed: the Google Cloud DR page (about 165k characters; not read in full, so no claim relies on
it), registry and KMS replication product names, the AWS_STS_REGIONAL_ENDPOINTS variable, the
Terraform-state and telemetry gotchas and the table rows for global config and cross-region calls
(none stated in the sources).
Method: documentation only; no commands were run.
