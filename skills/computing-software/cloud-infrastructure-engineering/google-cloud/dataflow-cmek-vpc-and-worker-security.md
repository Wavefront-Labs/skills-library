---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataflow-cmek-vpc-and-worker-security
name: dataflow-cmek-vpc-and-worker-security
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataflow, dataflow-cmek, dataflow-security, private-ip-workers, shared-vpc]
level: advanced
status: docs-checked
description: "Lock down Dataflow jobs: dedicated worker service account, private-IP workers on a Shared VPC subnet, firewall for worker ports, CMEK for job state, and VPC Service Controls."
sources: ["https://cloud.google.com/dataflow/docs/concepts/security-and-permissions", "https://cloud.google.com/dataflow/docs/guides/customer-managed-encryption-keys", "https://cloud.google.com/dataflow/docs/guides/specifying-networks", "https://cloud.google.com/dataflow/docs/guides/routes-firewall"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataflow CMEK, VPC and worker security

## 1. Identities
- **Worker SA** (Python/Go `--service_account_email`, Java `--serviceAccount`): a user-managed account per pipeline, with `roles/dataflow.worker` plus only the data roles it needs, and read/write on the staging and temp locations. Google recommends this over the default Compute Engine service account.
- **Dataflow service agent** `service-<PROJECT_NUMBER>@dataflow-service-producer-prod.iam.gserviceaccount.com`: manages the job; on Shared VPC it needs the Compute Network User role on the subnet (granted in the host project).
- The Dataflow service agent and the Compute Engine service agent (`service-<PROJECT_NUMBER>@compute-system.iam.gserviceaccount.com`) need `iam.serviceAccountUser` on the worker SA (and `iam.serviceAccountTokenCreator` if it is in another project; cross-project use also requires `iam.disableCrossProjectServiceAccountUsage` not to be enforced).
- The submitting user may need `roles/dataflow.developer` (owners and editors already have it).

## 2. Network
```bash
--network=<VPC> \
--subnetwork=https://www.googleapis.com/compute/v1/projects/<HOST_P>/regions/<R>/subnetworks/<SUBNET> \
--no_use_public_ips      # Python and Go: --no_use_public_ips ; Java: --usePublicIps=false
```
- Subnet needs **Private Google Access** (or a Private Service Connect endpoint) so workers without external IPs reach Google APIs; reaching non-Google endpoints needs Cloud NAT. A Shared VPC subnetwork must be given as a complete URL and be in the worker region.
- Firewall: Dataflow adds the network tag `dataflow` to every worker; allow TCP 12345-12346 between VMs with that tag (ingress and egress rules).
- A job that gets public IPs while `constraints/compute.vmExternalIpAccess` is enforced fails with a constraint-violated error, so set `--no_use_public_ips`.

## 3. CMEK
```bash
--dataflow_kms_key=projects/<P>/locations/<R>/keyRings/df/cryptoKeys/df-key
```
Grant `roles/cloudkms.cryptoKeyEncrypterDecrypter` to both the Dataflow service agent and the Compute
Engine service agent. Covers worker Persistent Disks, Dataflow Shuffle and Streaming Engine state; job metadata (names, parameters, graph) is not encrypted with your key, and sources/sinks keep their own keys.

## 4. VPC Service Controls
Dataflow's dependent endpoints support VPC Service Controls. With a perimeter, workers need access to `restricted.googleapis.com` (or the `vpc-sc` bundle with Private Service Connect): firewall egress must allow that range and DNS must resolve `*.googleapis.com` to it.

## Gotchas
- Key region must equal the job region; use regional keys (not global or multi-region). Disabling or destroying the key cancels jobs using it.
- A temp location must be specified when using a Cloud KMS key; Dataflow cannot create a default one.
- Streaming jobs created before 2024-03-07 do not protect key-based operation data keys with CMEK until drained or cancelled and restarted.

## Verify
- [ ] Job details show no external IPs on workers; `gcloud dataflow jobs describe <ID>` output contains `serviceKmsKeyName`, and the console Encryption type reads Customer-Managed key.

## Checked
2026-10-27. Confirmed against Dataflow security and permissions, CMEK, specifying networks and routes/firewall pages and the gcloud dataflow jobs describe reference: worker and service-agent roles, service account flags, Shared VPC role and URL rules, no-external-IP flags per SDK, Private Google Access and Cloud NAT, the dataflow network tag and TCP 12345-12346, vmExternalIpAccess error, KMS grants to the Dataflow and Compute Engine service agents, regional-key rule, key disable behaviour, state locations covered, restricted.googleapis.com requirement. Removed: Flex Template launcher flag, Artifact Registry reader claim, specific VPC-SC service list and templates-bucket egress advice, ingress-to-self firewall note, the exact describe --format path.
Method: documentation only; no commands were run.
