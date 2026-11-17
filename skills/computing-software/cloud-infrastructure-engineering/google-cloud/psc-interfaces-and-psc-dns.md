---
id: computing-software.cloud-infrastructure-engineering.google-cloud.psc-interfaces-and-psc-dns
name: psc-interfaces-and-psc-dns
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-service-connect, psc-interfaces, psc-dns, network-attachments, service-directory]
level: advanced
status: docs-checked
description: "Use PSC interfaces so a producer VM can initiate connections into a consumer VPC via network attachments, and understand DNS for PSC endpoints with Service Directory."
sources: ["https://cloud.google.com/vpc/docs/about-private-service-connect-interfaces", "https://cloud.google.com/vpc/docs/create-manage-network-attachments", "https://cloud.google.com/vpc/docs/configure-private-service-connect-services"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSC interfaces and PSC DNS

## 1. PSC interfaces (producer to consumer)
A PSC endpoint lets a consumer VPC initiate connections to a producer. A **PSC interface** works
the other way: the producer's VM gets an extra network interface that connects to a **network
attachment** in the consumer VPC, so the producer can initiate connections into the consumer
network. The first interface of the VM stays in a producer subnet. When the consumer accepts the
connection, the interface receives an internal IP from the attachment's subnet. Interface
connections are transitive: producer workloads can reach other workloads connected to the consumer VPC.

Consumer creates the network attachment:
```bash
gcloud compute network-attachments create na-vendor --region=<R> \
  --subnets=attach-subnet --connection-preference=ACCEPT_MANUAL \
  --producer-accept-list=<PRODUCER_PROJECT_ID>
```
Producer creates a VM with an interface on it:
```bash
gcloud compute instances create agent-vm --zone=<Z> \
  --network-interface=network=producer-vpc,subnet=prod-subnet \
  --network-interface=network-attachment=projects/<CONSUMER_P>/regions/<R>/networkAttachments/na-vendor
```
The attachment's subnet must be in the same region as the attachment, and the attachment must be in
the same region as the interface's VM. One subnet can be shared by several attachments.

## 2. DNS for PSC endpoints (consumer side)
- Creating an endpoint registers it with Service Directory: the namespace you pass with
  `--service-directory-registration=projects/<P>/locations/<R>/namespaces/<NS>`, or the default
  namespace `goog-psc-default`. When the prerequisites for automatic DNS are met, a DNS zone named
  `NAMESPACE--REGION` is created.
- If they are not met, create DNS entries yourself (a private zone with a record for the endpoint
  IP), or create a Service Directory-backed DNS zone, after which endpoint entries appear automatically.
- Check a Service Directory namespace is empty before deleting it or its DNS zone: other services can use it.

## Verify
- [ ] `gcloud compute network-attachments describe na-vendor --region=<R>` lists the accepted connection; from the producer VM, a connection to a consumer internal IP succeeds.

## Checked
2026-10-28. Confirmed against About Private Service Connect interfaces, Create and manage network attachments (same-region rules, shared subnet) and Configure Private Service Connect services (Service Directory registration, `goog-psc-default`, `NAMESPACE--REGION` zone, manual alternatives); NetworkAttachment fields via the Compute discovery document; gcloud flags via check_commands.py. Removed: managed-product examples, `--domain-names` automatic-DNS claim (its page returned 404), firewall advice, per-VPC zone and deletion claims.
Method: documentation only; no commands were run.
