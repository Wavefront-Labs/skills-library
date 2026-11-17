---
id: computing-software.cloud-infrastructure-engineering.aws.xray-distributed-tracing
name: xray-distributed-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, x-ray, xray, distributed-tracing, tracing, segments, subsegments, trace-header, sampling-rules, service-map, adot, opentelemetry, x-ray-daemon, trace-id, annotations, metadata, lambda-tracing, api-gateway-tracing, transaction-search, application-signals]
level: practitioner
status: docs-checked
description: "Trace requests across API Gateway, Lambda, ECS and databases with AWS X-Ray or ADOT/OpenTelemetry: header propagation, sampling rules, annotations and common blind spots."
sources: ["https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-console-sampling.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-daemon-timeline.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-services-apigateway.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X-Ray distributed tracing — one request, every hop, with the slow one highlighted

**Goal:** a single trace id follows a request from the edge through services, queues and
databases; sampling keeps cost sane; annotations let you find the traces that matter.

## 1. Model
- **Trace** = tree of **segments** (one per service hop) containing **subsegments**
  (SDK calls, SQL, HTTP, custom code blocks). Each has start/end, `error` (4xx), `fault`
  (5xx), `throttle` flags.
- Propagation via the `X-Amzn-Trace-Id: Root=1-<epoch-hex>-<random>;Parent=<seg>;Sampled=1`
  header. API Gateway (stage `tracingEnabled`), AppSync and Step Functions support active
  tracing and sampling; ALB adds or updates the header; Lambda (`Tracing: Active`) traces
  requests already sampled upstream; SQS carries the header in the `AWSTraceHeader` message
  system attribute (Lambda consumers recover it automatically, other consumers must read it);
  SNS passes trace context from instrumented publishers; EventBridge propagates it to targets
  when the sender is instrumented.
- **Annotations** = indexed key/values (X-Ray indexes up to 50 per trace) you can filter on
  (`annotation[tenant] = "acme"`); **metadata** = non-indexed values for context. Put ids you
  search by in annotations.

## 2. Instrumentation options
| Path | How |
|---|---|
| X-Ray SDKs (maintenance mode since 2026-02-25: security fixes only) | `AWSXRay.captureAWSv3Client(client)`, `captureHTTPsGlobal`; Python `patch_all()` |
| **AWS Distro for OpenTelemetry (ADOT) / OpenTelemetry** (recommended by AWS) | OTel SDK plus a collector or the CloudWatch agent sending traces to X-Ray, or OTLP direct to the X-Ray endpoint; also feeds CloudWatch Application Signals |
- Data path: SDK → UDP 2000 to the **X-Ray daemon** (Lambda runs it for sampled requests;
  Elastic Beanstalk with the `XRayEnabled` option; elsewhere run it yourself) or an ADOT
  collector or CloudWatch agent → X-Ray. IAM: the AWS managed policy `AWSXRayDaemonWriteAccess`.
- Set `AWS_XRAY_DAEMON_ADDRESS` to the daemon host and port where it is not on localhost.
  Lambda: `Tracing: Active` plus the SDK for subsegments for downstream calls.
- Custom subsegment around slow code:
  ```python
  from aws_xray_sdk.core import xray_recorder
  with xray_recorder.in_subsegment('price-calc') as s:
      s.put_annotation('tenant', tenant_id)
      ...
  ```

## 3. Sampling
- Default: reservoir of 1 request per second + 5 % of additional requests. Add **sampling
  rules** (console or `create-sampling-rule`): priority (1-9999), `ReservoirSize`, `FixedRate`
  (0-1 in the API), matched on service name/type, host, HTTP method, URL path, attributes.
- Typical set: `/health*` → rate 0; `/checkout*` → 100 % (low volume, high value). The
  decision is made once, at the first X-Ray-enabled hop, and downstream services honour it, so
  put rules on the root service. A rule can also carry a `SamplingRateBoost` (anomaly-driven
  boost with a maximum rate and a cooldown window).
- `AWS_XRAY_CONTEXT_MISSING=LOG_ERROR` avoids exceptions when code runs outside an active segment.

## 4. Reading it
- **Service map / trace map**: choosing a node builds a filter expression from the node and its error types.
- **Trace list** filter expressions: `service("api") { fault }`, `responsetime > 2`,
  `annotation[tenant] = "acme" AND http.status = 500`, `duration >= 5 AND !ok`.
- **Transaction Search** (CloudWatch) ingests 100 % of spans as structured logs in the
  `aws/spans` log group and indexes a percentage you choose as trace summaries in X-Ray; use
  it when you need every transaction searchable.

## 5. Blind spots and how to close them
| Gap | Fix |
|---|---|
| SQS consumer trace not linked | Read the `AWSTraceHeader` system attribute (via `ReceiveMessage`) and recover the trace context; Lambda consumers do this automatically |
| DynamoDB/S3 calls missing | Patch or wrap the SDK client (`capture*`, `patch_all`) so subsegments are created |
| Database queries invisible | Use the SDK's patched database libraries or OTel instrumentation for the driver |
| HTTP calls to third parties missing | `captureHTTPsGlobal` / OTel http instrumentation |
| Async work after response | Start a new segment with the parent id captured before the handler returns |

## 6. Cost and retention
- Traces are billed (see the X-Ray pricing page); trace data and service graph data are
  retained for 30 days. Sampling and dropping health checks are the levers. Groups
  (`create-group`) with filter expressions publish CloudWatch metrics for alarms on trace data.

## Gotchas
- Segment name must be stable per service. With API Gateway HTTP integrations each distinct URL
  path becomes a service node, and too many paths can exceed the trace map limit of 10,000 nodes.
- Annotations are simple key-value pairs; nested or object values go to metadata (not indexed).
- A Node.js SDK v3 client records less than v2 (no DynamoDB table name).

## Verify
- [ ] A test request shows API Gateway → Lambda → DynamoDB in one trace with the same `Root` id.
- [ ] `/health` traces are absent (sampling rule at 0).
- [ ] Filtering `annotation[tenant] = "<id>"` returns only that tenant's traces.
- [ ] Forced 500 from a downstream appears as a fault on the correct node, not the caller.
- [ ] Daemon/collector logs show no dropped segments under load test.

## Checked

2026-10-27, AWS documentation (current release as read on that date). X-Ray Developer Guide concepts, sampling, daemon, SDK timeline, API Gateway, Lambda, SQS and IAM pages; CloudWatch Transaction Search page; botocore xray and apigateway models; aws-xray-sdk-python source. Fixed: SDKs and daemon in maintenance mode since 2026-02-25; annotation filter syntax annotation[key]; Transaction Search indexes only a chosen percentage as trace summaries; sampling decisions are made at the first hop; added the 30-day retention and the 10,000-node trace map limit. Confirmed: default 1 per second plus 5 percent, priority 1-9999, UDP 2000, AWSXRayDaemonWriteAccess, tracingEnabled, 50 indexed annotations, in_subsegment and put_annotation. Removed unsourced claims about Powertools, ADOT layer names and propagator variable, App Runner and ECS/EKS propagation, service-map colour reading, Lambda timeline subsegments, trace delay and daemon log text, and group metric names.
Method: documentation only; no commands were run.
