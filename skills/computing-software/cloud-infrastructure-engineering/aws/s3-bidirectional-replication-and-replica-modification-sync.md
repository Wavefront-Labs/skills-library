---
id: computing-software.cloud-infrastructure-engineering.aws.s3-bidirectional-replication-and-replica-modification-sync
name: s3-bidirectional-replication-and-replica-modification-sync
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, bidirectional-replication, replica-modification-sync, s3-replication, multi-region]
level: advanced
status: docs-checked
description: "Set up two-way S3 replication between buckets for active-active Regions, with replica modification sync for metadata and safe handling of loops and deletes."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-for-metadata-changes.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/mrap-create-two-way-replication-rules.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-what-is-isnot-replicated.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bidirectional replication and replica modification sync

## 1. Two rules, one per direction
Both buckets versioned. Bucket A replicates to B, bucket B replicates to A:
```json
{"Role":"arn:aws:iam::<ACCOUNT_ID>:role/s3-repl",
 "Rules":[{"ID":"a-to-b","Priority":1,"Status":"Enabled","Filter":{},
   "DeleteMarkerReplication":{"Status":"Enabled"},
   "SourceSelectionCriteria":{"ReplicaModifications":{"Status":"Enabled"}},
   "Destination":{"Bucket":"arn:aws:s3:::app-data-euw1","Metrics":{"Status":"Enabled"},
     "ReplicationTime":{"Status":"Enabled","Time":{"Minutes":15}}}}]}
```
Mirror the config on the other bucket, with `ReplicaModifications` enabled on both rules (it must be enabled on both sides to sync replica metadata changes). The buckets can be in the same or different Regions.

## 2. Why no infinite loop
Objects created by replication have status `REPLICA` and are not replicated again as new objects.
**Replica modification sync** lets metadata changes made to a replica (tags, ACLs, Object Lock retention)
flow back to the source (tags, ACLs, annotations and Object Lock settings); without it, a tag set on the B copy stays only on B.

## 3. Conflicts
Replication is asynchronous and the replication documentation does not describe conflict resolution for
the same key written in both Regions at about the same time. Design keys so one Region owns each key
(application-level routing).

## 4. With Multi-Region Access Points
In the console, a Multi-Region Access Point's **Replication and failover** tab offers the
**Replicate objects among all specified buckets** template, which creates two-way rules (each bucket
versioned and in a different Region). The template replaces any existing replication rules on those
buckets. Enabling RTC, metrics, delete marker replication and replica modification sync is recommended.

## 5. Existing objects
Replication only covers new writes; use S3 Batch Replication for the backlog.

## Verify
- [ ] Put in A appears in B; tag change on the B replica appears on the A object.
- [ ] `ReplicationLatency` and `OperationsFailedReplication` metrics alarmed in both directions.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: two rules (one per direction) form two-way replication; `ReplicaModifications` must be enabled on both sides; which metadata syncs; MRAP template name and its replace-existing-rules warning; replicas are not re-replicated. Removed the unsupported timestamp-wins conflict claim and the conditional-writes suggestion.

Method: documentation only; no commands were run.
