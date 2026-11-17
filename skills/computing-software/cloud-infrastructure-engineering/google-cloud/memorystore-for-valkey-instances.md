---
id: computing-software.cloud-infrastructure-engineering.google-cloud.memorystore-for-valkey-instances
name: memorystore-for-valkey-instances
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, memorystore, memorystore-valkey, valkey-cluster, psc, redis-compatible]
level: practitioner
status: docs-checked
description: "Create Memorystore for Valkey instances: cluster vs cluster-disabled mode, shards and replicas, service connection policies, auth, persistence and encryption flags."
sources: ["https://docs.cloud.google.com/memorystore/docs/valkey/create-instances", "https://docs.cloud.google.com/memorystore/docs/valkey/networking", "https://docs.cloud.google.com/sdk/gcloud/reference/memorystore/instances/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memorystore for Valkey

Valkey is the open-source Redis fork. Networking uses Private Service Connect endpoints that Memorystore
deploys automatically through a **service connection policy**.

## 1. Networking prerequisite
A policy is unique per project, network, region and service class; use the `gcp-memorystore` service class.
Leave the service instance scope at its default (custom scopes are not supported). In Shared VPC the
Network Admin defines the policy in the host project and Valkey Admins create instances in service projects.
```bash
gcloud network-connectivity service-connection-policies create valkey-policy \
  --network=<VPC> --region=<REGION> --service-class=gcp-memorystore \
  --subnets=projects/<HOST_PROJECT>/regions/<REGION>/subnetworks/<SUBNET>
```
Optionally set a connection limit: instances you plan in the region multiplied by two.

## 2. Create
```bash
gcloud memorystore instances create cache-prod --location=<REGION> \
  --endpoints='[{"connections":[{"pscAutoConnection":{"network":"projects/<NETWORK_PROJECT>/global/networks/<VPC>","projectId":"<PROJECT_ID>"}}]}]' \
  --shard-count=3 --replica-count=1 --node-type=highmem-medium --mode=cluster \
  --authorization-mode=iam-auth --transit-encryption-mode=server-authentication \
  --persistence-config-mode=aof --zone-distribution-config-mode=multi-zone
```
- `--mode=cluster-disabled` with `--shard-count=1` creates a cluster-mode-disabled instance. The mode cannot
  be changed after creation; Google recommends cluster mode enabled for its scaling characteristics.
- Replicas per shard: 0-5, default 1 in the console.
- `--authorization-mode`: `auth-disabled`, `iam-auth`, `token-auth`. `--persistence-config-mode`: `aof`,
  `rdb`, `disabled`. `--transit-encryption-mode` has `server-authentication`. The zone distribution
  mode defaults to multi-zone.
- By default in-transit encryption is disabled; IAM or token auth selects TLS automatically in the console.
- The `shared-core-nano` node type has no SLA: development and testing only.
- Fetch the CA for TLS clients with `gcloud memorystore instances get-certificate-authority`.

## Gotchas
- A missing service connection policy for the network, region and service class blocks creation.
- Assign ACL policies only to instances in the same region as the policy.

## Verify
- [ ] `gcloud memorystore instances describe cache-prod --location=<REGION>` shows the instance READY with the intended mode, shards and replicas.

## Checked
2026-10-28. Confirmed against the Memorystore for Valkey Create instances and Networking pages and the
gcloud `memorystore instances create` reference (flags and enum values). Removed: engine version
value, IAM role and token refresh claims, hash tag guidance, migration advice, and the online scaling
and "recommended successor to Redis" claims (not confirmed).
Method: documentation only; no commands were run.
