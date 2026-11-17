---
id: computing-software.data-engineering.databricks.auto-loader-file-notification-mode
name: auto-loader-file-notification-mode
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, autoloader, file-notification-mode, directory-listing, file-events, sqs, event-grid, pubsub, cloudfiles-usenotifications]
level: practitioner
status: docs-checked
description: "Choose Auto Loader directory listing vs file notification or managed file events, set up the cloud queue permissions, backfill missed events and clean up notification resources."
sources:
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-detection-modes
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-notification-mode
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto Loader: directory listing vs file notification

**Goal:** discover new files cheaply and quickly even when the landing path holds millions of files.

## 1. The modes
| Mode | How new files are found | Good for |
|---|---|---|
| Directory listing (default) | lists the input path each micro-batch | up to ~hundreds of thousands of files, or lexically ordered paths |
| Managed file events (`cloudFiles.useManagedFileEvents`, newer) | Unity Catalog external location with file events enabled; Databricks manages the queue | recommended on UC when available |
| Classic file notification (`cloudFiles.useNotifications = true`) | Auto Loader creates a cloud notification + queue per stream | large directories without managed file events |
Listing cost grows with the number of files in the path (API calls + time); notification cost is roughly per new file.

## 2. Managed file events
1. On the external location (Catalog Explorer > External location > enable file events), grant the storage credential the permissions the docs list (queue/event subscription creation).
2. In the stream: `.option("cloudFiles.useManagedFileEvents", "true")`.
One queue serves all streams on that location — avoids per-stream queue limits.

## 3. Classic file notification
```python
.option("cloudFiles.useNotifications", "true")
# AWS: creates SNS topic + SQS queue subscribed to the S3 prefix
.option("cloudFiles.region", "eu-west-1")
# Azure: Event Grid subscription + storage queue; needs service principal
#   cloudFiles.subscriptionId / tenantId / clientId / clientSecret / resourceGroup
# GCP: Pub/Sub topic + subscription; cloudFiles.projectId
```
- The cluster identity needs rights to create these resources the first time — or pre-create the queue and pass `cloudFiles.queueUrl` (AWS) / `cloudFiles.queueName` (Azure) / `cloudFiles.subscription` (GCP) so the job only needs read/delete-message rights.
- Limits: S3 allows a limited number of event notification configs per bucket and prefixes cannot overlap; Azure caps Event Grid subscriptions per storage account. Many streams on one bucket → pre-created shared queues or managed file events.

## 4. Backfills: notifications are not perfect
Events can be missed (permissions changed, queue retention exceeded while the stream was stopped, files copied before setup).
```python
.option("cloudFiles.backfillInterval", "1 day")   # periodic full listing to catch anything missed
```
The initial start always does a full listing for existing files (unless `includeExistingFiles=false`).

## 5. Clean up
Notification resources outlive a deleted stream. List and tear down:
```scala
import com.databricks.sql.CloudFilesAWSResourceManager
val mgr = CloudFilesAWSResourceManager.newManager.option("cloudFiles.region", "eu-west-1").create()
mgr.listNotificationServices().show(false)
mgr.tearDownNotificationServices("<stream-id>")
```
(Azure/GCP managers exist with the same methods.)

## Verify
- [ ] Batch duration no longer grows with total file count in the landing path.
- [ ] A file landed while the stream was stopped is ingested after restart.
- [ ] `backfillInterval` is set for notification mode.
- [ ] No orphaned queues/topics remain for retired streams.

## Checked

2026-10-28. Confirmed: cloudFiles.useManagedFileEvents, includeExistingFiles, listNotificationServices and tearDownNotificationServices on the Auto Loader pages. Removed: an SQS retention figure.

Method: documentation only; no commands were run.
