---
id: computing-software.devops-ci-cd.argo-events.argo-events-minio-eventsource-bucket-notifications
name: argo-events-minio-eventsource-bucket-notifications
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, minio-eventsource, bucket-notification, s3, secret, mc]
level: practitioner
status: docs-checked
description: "Trigger on Minio bucket notifications with the Minio EventSource, which works only with Minio servers and not AWS S3."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/setup/minio.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events minio eventsource bucket notifications

The Minio EventSource listens to Minio bucket notifications. It is exclusive to the Minio server; for AWS S3 notifications use the AWS SNS EventSource. The event `data` has a `notification` array holding the Minio notification (see the Minio bucket notification guide).

Setup:
1. Make the Minio server reachable from the EventSource, port-forwarding if local (`kubectl -n argo-events port-forward <minio-pod-name> 9000:9000`) and configure `mc` (`mc config host add minio http://localhost:9000 minio minio123`).
2. Create a Secret with keys `accesskey` and `secretkey` (example name `artifacts-minio`, values base64-encoded) that the EventSource references.
3. Create the bucket the example configures: `mc mb minio/input`.
4. Apply `examples/event-sources/minio.yaml` and the sensor `examples/sensors/minio.yaml`.
5. Upload a file such as `hello-world.txt` to `input`; the Sensor triggers a workflow; check with `argo list`.

Minio is listed as an Active-Passive source on the EventSource High Availability page.

## Checked

2026-11-04. Confirmed against the Minio EventSource page (exclusive to Minio, use AWS SNS for S3, `notification` array, port-forward and `mc` commands, Secret keys `accesskey` and `secretkey`, `mc mb minio/input`, example manifests, `hello-world.txt` upload, `argo list`) and the EventSource High Availability page (Active-Passive). Removed the example `notification.0.s3...` trigger-parameter paths and the claim that other walkthroughs reuse this EventSource, which this page does not state.
Method: documentation only; no commands were run.
