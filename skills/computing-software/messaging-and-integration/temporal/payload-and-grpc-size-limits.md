---
id: computing-software.messaging-and-integration.temporal.payload-and-grpc-size-limits
name: payload-and-grpc-size-limits
category: computing-software
field: messaging-and-integration
product: temporal
tags: [blob-size-limit, payload-size, grpc-message-size, payloads-too-large, claim-check, external-storage, batching]
level: practitioner
status: docs-checked
description: "Temporal size limits: 2 MB payload limit versus 4 MB gRPC message limit, error causes, SDK behavior by version, claim check and batching fixes."
sources:
  - https://docs.temporal.io/troubleshooting/blob-size-limit-error
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two distinct limits apply.

Payload size: 2 MB per payload (Cloud, and the self-hosted default; configurable there via `limit.blobSize.error`). Typical errors: `WORKFLOW_TASK_FAILED_CAUSE_PAYLOADS_TOO_LARGE`, `[TMPRL1103] Attempted to upload payloads with size that exceeded the error limit.`, and `... exceeds size limit` on schedule-activity input or complete-result attributes.
- Newer SDKs (Go 1.43.0+, Python 1.23.0+, TypeScript 1.21.0+, .NET 1.18.0+, Ruby 1.7.0+, Rust 0.6.0+) fail the Workflow Task, keep the Workflow open so you can deploy a fix, and fail Activity Tasks explicitly.
- Older SDKs: oversized inputs make the Service reject the command and terminate the Workflow; an oversized Activity result fails the Activity; an oversized Workflow result loops forever because replay reproduces it.

gRPC message size: 4 MB per request, covering all commands from one Workflow Task. Many modest Activity inputs, or hundreds of tiny ones, can exceed it while each payload is small.
- Workflow Task: cause `WORKFLOW_TASK_FAILED_CAUSE_GRPC_MESSAGE_TOO_LARGE`; the Service ends the Execution as `TERMINATED` (no automatic retry) because replay repeats the problem. Fix the Worker, then restart.
- Activity Task: the Activity runs successfully but the result cannot be delivered, so it retries until `ScheduleToCloseTimeout` (indefinitely if unset). `ResourceExhausted` appears only in Worker logs.

Fixes:
1. Claim check: store large data in an object store and pass references; built into SDKs as External Storage (pre-GA), or implement through a custom Payload Codec.

2. Batch: process Activities or Child Workflows in smaller groups, waiting between batches, or sleep between groups inside a Workflow Task.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: troubleshooting/blob-size-limit-error, references/dynamic-configuration (limit.blobSize.error) (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
