---
id: computing-software.messaging-and-integration.apache-pulsar.tiered-storage-offload
name: tiered-storage-offload
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [tiered-storage, offload, managed-ledger-offload-driver, offload-threshold, offload-status, offloaders]
level: practitioner
status: docs-checked
description: "Offload sealed Pulsar ledger segments to S3, GCS or a filesystem: install offloaders, set the driver and bucket, thresholds, manual offload, status and read priority."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/tiered-storage-overview.md
  - https://github.com/apache/pulsar-site/blob/main/docs/cookbooks-tiered-storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep a very long topic backlog cheaply by moving old segments out of BookKeeper while consumers and readers still see them.

How it works: a topic's managed ledger is an ordered list of segments; only the last is written. Sealed segments are immutable, so offloading copies them one by one (all except the current segment) to long-term storage, then they remain readable transparently. Uses Apache jclouds (S3, GCS, Azure, Aliyun) or Hadoop for filesystems.

Install: offloaders ship as a separate tarball. Untar it and move the `offloaders` directory into the Pulsar directory (on every broker for bare metal). The apachepulsar/pulsar Docker image includes the offloader NARs except the filesystem (Hadoop) one.

Broker config (`broker.conf`), at minimum driver, bucket and credentials:
```conf
managedLedgerOffloadDriver=aws-s3
s3ManagedLedgerOffloadBucket=pulsar-topic-offload
s3ManagedLedgerOffloadRegion=eu-west-3
```
Drivers: `aws-s3`, `google-cloud-storage`, `filesystem`, and `s3` (needs an endpoint URL in `s3ManagedLedgerOffloadServiceEndpoint`, for S3-compatible stores). The bucket must already exist or offload fails. AWS credentials come from the DefaultAWSCredentialsProviderChain (for example instance profile), not a Pulsar setting.

Automatic and manual offload:
```bash
bin/pulsar-admin namespaces set-offload-threshold --size 10M my-tenant/my-namespace
bin/pulsar-admin topics offload --size-threshold 10M my-tenant/my-namespace/topic1
bin/pulsar-admin topics offload-status -w my-tenant/my-namespace/topic1
```
Manual offload does not wait; `offload-status` reports progress and `-w` waits.

Read priority: default `-orp` is `tiered-storage-first`; switch to bookkeeper-first with `bin/pulsar-admin namespaces set-offload-policies my-tenant/my-namespace -orp bookkeeper-first` (also available for topics). Precedence is topic over namespace over broker.

Gotchas: automatic offload only runs when a new segment is added, so a quiet topic will not offload until its segment fills. Upload uses multi-part objects, so add a bucket lifecycle rule to expire incomplete multi-part uploads after a day or two.

## Checked

2026-11-03. Confirmed against the pulsar-site pages tiered-storage-overview and cookbooks-tiered-storage: segment mechanism, offloader install and Docker note, driver names and the `s3` endpoint setting, bucket must exist, credential chain, thresholds, offload and offload-status commands, read priority, precedence and the multi-part lifecycle advice. Removed the invented Verify step.

Method: documentation only; no commands were run.
