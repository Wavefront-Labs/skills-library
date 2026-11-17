---
id: computing-software.cloud-infrastructure-engineering.google-cloud.storage-transfer-service-jobs-agents-and-permissions
name: storage-transfer-service-jobs-agents-and-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, storage-transfer-service, transfer-jobs-scheduling, transfer-manifest, transfer-service-iam, transfer-permissions, hdfs-to-gcs, hadoop-transfer, s3-to-gcs]
level: practitioner
status: docs-checked
description: "Run Storage Transfer Service jobs: scheduled and manifest-driven transfers from S3, GCS and on-prem or HDFS via agent pools, with the right service agent and user roles."
sources: ["https://cloud.google.com/storage-transfer/docs/create-transfers", "https://cloud.google.com/storage-transfer/docs/manifest", "https://cloud.google.com/storage-transfer/docs/iam-cloud", "https://cloud.google.com/sdk/gcloud/reference/transfer/jobs/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Transfer Service: jobs, agents and permissions

## 1. Permissions first
```bash
gcloud transfer authorize                      # inspect existing permissions, print missing roles
gcloud transfer authorize --add-missing        # grant the missing roles to the user and the service agent
# service agent: project-<NUMBER>@storage-transfer-service.iam.gserviceaccount.com
```
`--add-missing` is the simple route but broad: it grants the user (or user-managed service account) roles
including `roles/owner` and `roles/storagetransfer.admin`, and the service agent `roles/storage.admin`
and `roles/storagetransfer.serviceAgent`. For least privilege grant manually instead:
- User creating jobs: `roles/storagetransfer.user` (create, get, update, list; no delete) or
  `roles/storagetransfer.admin`, plus `resourcemanager.projects.getIamPolicy` (for example through
  `roles/iam.roleViewer`) so the service agent's permissions can be checked.
- Service agent, destination bucket: `roles/storage.legacyBucketWriter`; add `roles/storage.objectViewer`
  when the job overwrites only when different, or never.
- Service agent, Cloud Storage source bucket: `roles/storage.legacyBucketReader` and `roles/storage.objectViewer`.
- Cross-project buckets: grant the **job project's** service agent on both buckets. Legacy roles can
  only be granted at bucket level. Domain restriction (`constraints/iam.allowedPolicyMemberDomains`) or
  `constraints/iam.disableCrossProjectServiceAccountUsage` may need updating, and so may VPC Service Controls.
- On-prem agent identities need `roles/storagetransfer.transferAgent`.

## 2. Scheduled cloud-to-cloud job
```bash
gcloud transfer jobs create s3://legacy-media gs://<DST>/media/ --name=s3-media-daily \
  --source-creds-file=aws-creds.json \
  --schedule-starts=2026-10-17T01:00:00Z --schedule-repeats-every=1d \
  --include-prefixes=2026/ --overwrite-when=different --delete-from=destination-if-unique \
  --notification-pubsub-topic=projects/<P>/topics/sts-events
```
Event-driven jobs copy data as it is added or changed, from Cloud Storage (Pub/Sub subscription),
Amazon S3 (an SQS queue ARN) or Azure Blob Storage. Pub/Sub notification events are `success`,
`failed` and `aborted`; unset means all three.

## 3. Manifests (exact file lists)
A manifest is a CSV in Cloud Storage (or on the source/destination file system) whose first column lists
file paths relative to the job's root (or object names within one bucket):
```bash
gcloud transfer jobs create gs://<SRC> gs://<DST> --manifest-file=gs://<B>/manifests/batch-0412.csv
```
The service agent needs `storage.objects.get` on the manifest bucket. Do not modify a manifest while a
transfer runs. Use for reprocessing a known set or migrating in controlled waves.

## 4. On-prem POSIX and HDFS via agents
```bash
gcloud transfer agent-pools create dc1-pool --display-name="DC1 agents"
gcloud transfer agents install --pool=dc1-pool --count=3 --mount-directories=/mnt/nas   # on each agent host
gcloud transfer jobs create posix:///mnt/nas/projects gs://<DST>/projects/ --source-agent-pool=dc1-pool
gcloud transfer jobs create hdfs:///data/warehouse gs://<DST>/warehouse/ --source-agent-pool=hdfs-pool
```
Agents see only mounted directories: keep any file-system manifest inside one. Cap bandwidth per pool
with `gcloud transfer agent-pools update dc1-pool --bandwidth-limit=<LIMIT>` (units in the command reference).

## 5. Monitor
```bash
gcloud transfer operations list --job-names=s3-media-daily --format='table(name,metadata.status,metadata.counters.bytesCopiedToSink)'
gcloud transfer operations describe <OP>      # errorBreakdowns
```

## Gotchas
- `--delete-from=destination-if-unique` deletes destination files absent at source (makes the destination
  match the source exactly): dangerous on shared prefixes.
- Metadata preservation is opt-in per field: `--preserve-metadata=storage-class,uid` style; set it explicitly.

## Verify
- [ ] Last operation status `SUCCESS` with no `errorBreakdowns`; object counts match a source listing.
- [ ] Pub/Sub notifications arrive for the events you selected.

## Checked
2026-10-31. Confirmed against "Agentless transfer permissions", "Transfer using a manifest", "Create
transfers", the `gcloud transfer jobs create` reference and the Storage Transfer v1 discovery document
(TransferOperation fields). Removed: the "prefer federated identity for S3" advice, HDFS Hadoop/Kerberos
setup (its page returned 404), the 500 bandwidth figure and the small-files note; the destination bucket
grant changed from `storage.admin` to the documented legacy bucket roles.
Method: documentation only; no commands were run.
