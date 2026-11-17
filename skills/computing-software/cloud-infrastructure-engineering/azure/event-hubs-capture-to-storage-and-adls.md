---
id: computing-software.cloud-infrastructure-engineering.azure.event-hubs-capture-to-storage-and-adls
name: event-hubs-capture-to-storage-and-adls
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, event-hubs, eh-capture, capture-setup, avro, parquet, adls-gen2, blob-storage, time-window, size-window, managed-identity, raw-archive, data-lake]
level: practitioner
status: docs-checked
description: "Enable Event Hubs Capture to Blob/ADLS Gen2: time and size windows, naming format, managed identity, empty-file behaviour, reading Avro, and Parquet via the no-code editor."
sources: ["https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-overview", "https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-enable-through-portal", "https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-managed-identity", "https://learn.microsoft.com/en-us/azure/event-hubs/explore-captured-avro-files", "https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-quotas", "https://learn.microsoft.com/en-us/azure/event-hubs/monitor-event-hubs-reference", "https://learn.microsoft.com/en-us/cli/azure/eventhubs/eventhub"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event Hubs Capture to Storage / ADLS Gen2

**Goal:** every event automatically archived to the lake, partitioned by time, as a replayable
raw layer — no consumer code to maintain.

## 1. Enable
```bash
az role assignment create --assignee <eh-namespace-msi> --role "Storage Blob Data Contributor" --scope <storage-id>
az eventhubs eventhub update -g rg-stream --namespace-name evhns-prod -n telemetry \
  --enable-capture true --capture-interval 300 --capture-size-limit 314572800 \
  --destination-name EventHubArchive.AzureBlockBlob --storage-account <storage-id> --blob-container raw-telemetry \
  --archive-name-format "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}" \
  --skip-empty-archives true --mi-system-assigned true
```
- Tiers: Standard (capture priced separately), Premium and Dedicated (included). Capture needs a non-premium storage account that allows block blobs; premium storage accounts are not supported.
- **Window**: first wins of time (60-900 s, shown as 1-15 min) or size (10-500 MB; the portal default is 300 MB); each partition captures independently. Small
  windows = many small files (bad for analytics).
- By default Event Hubs writes empty files when no events arrive in a window (a predictable cadence marker); `--skip-empty-archives true` suppresses them.
- Managed identity (system or user-assigned) is the preferred way to authenticate to the destination; give it **Storage Blob Data Contributor** on the storage account.
- Destination can be an ADLS Gen2 account through the Azure Storage provider (`EventHubArchive.AzureBlockBlob`). Data Lake Storage Gen1 is retired and no longer supported for Capture.

## 2. Format and reading
- Native capture writes **Avro**: each record has `SequenceNumber`, `Offset`, `EnqueuedTimeUtc`,
  `SystemProperties`, `Properties`, `Body` (bytes — your payload, decode JSON yourself).
- The Avro schema is `Microsoft.ServiceBus.Messaging` with fields `SequenceNumber` (long), `Offset` (string), `EnqueuedTimeUtc` (string), `SystemProperties` and `Properties` (maps) and `Body` (nullable bytes); any Avro reader (or Avro Tools) can convert the files.
- **Parquet**: the portal no-code editor (Stream Analytics) can capture Event Hubs data to a Data Lake Storage account in Parquet format.

## 3. Operate
- Metrics `CapturedMessages`, `CapturedBytes`, `CaptureBacklog` (alert when backlog grows — destination unreachable or throttled).
- Capture reads from internal storage and bypasses the TU/PU/CU egress quotas, so it does not use up egress needed by other readers.
- Add a lifecycle management policy on the container that matches your retention requirements.

## Gotchas
- Changing the archive name format later breaks downstream path patterns; decide once (all tokens must be present, any order).
- Capture writes per partition, so ordering is only guaranteed within a partition file.
- Capture is not a substitute for consumer retention: if capture is disabled during an outage beyond retention, data is gone.

## Verify
- [ ] Files appear under the expected path within one window, one per active partition.
- [ ] A sample Avro decodes to the original JSON payloads with matching counts to `IncomingMessages` for that window.
- [ ] `CaptureBacklog` alert exists and stays at 0 in normal operation.

## Checked
Checked 2026-10-24 against azure-docs Event Hubs pages (capture overview, enable capture, capture with managed identity, explore captured Avro files, tier limits and features includes, monitoring reference) and the azure-docs-cli eventhubs reference (flag names and ranges). Confirmed: capture window 60-900 s and 10-500 MB, first wins, portal default 300 MB; all archive-name tokens mandatory in any order; Avro schema fields; Gen1 retired; Storage Blob Data Contributor for the managed identity; metrics CapturedMessages, CapturedBytes, CaptureBacklog; capture priced separately on Standard and included on Premium and Dedicated. Found wrong and fixed: capture was said to count against namespace egress (docs say it bypasses egress quotas). Removed unconfirmed: trusted-services firewall behaviour, lifecycle day counts, Spark and Python snippets, the 5 minute default.

Method: documentation only; no commands were run.
