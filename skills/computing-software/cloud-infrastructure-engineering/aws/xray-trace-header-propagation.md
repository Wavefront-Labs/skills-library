---
id: computing-software.cloud-infrastructure-engineering.aws.xray-trace-header-propagation
name: xray-trace-header-propagation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, x-ray, x-amzn-trace-id, trace-propagation, awstraceheader, w3c-traceparent, distributed-tracing]
level: practitioner
status: docs-checked
description: "Propagate X-Ray trace context end to end: X-Amzn-Trace-Id format, what ALB, API Gateway and Lambda add, SQS AWSTraceHeader, async hops, and W3C traceparent interop."
sources: ["https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-request-tracing.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-services-sqs.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-services-apigateway.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-api-sendingdata.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X-Ray trace header propagation

## The header
```
X-Amzn-Trace-Id: Root=1-67890abc-1234567890abcdef12345678;Parent=53995c3f42cd8ad8;Sampled=1
```
- `Root`: trace id = `1-<8 hex epoch seconds>-<24 hex random>`.
- `Parent`: id of the calling segment, set when the request came from an instrumented application.
- `Sampled`: the sampling decision, `1` or `0` (the Python SDK also accepts `?` for undecided).
- `Lineage` may be appended by Lambda and other AWS services; treat it as opaque and do not use it directly.
- Applications may remove `X-Amzn-Trace-Id` from incoming requests so users cannot inject trace
  IDs or sampling decisions.

## Who adds or forwards it
| Hop | Behaviour |
|---|---|
| ALB | adds the header with a `Root` field if missing; if `Root` is present it inserts a `Self` field; custom fields are preserved; the header is logged when access logs are on (no X-Ray needed) |
| API Gateway | adds a header with `Root` to incoming requests that lack one; with active tracing off it still records a segment for requests an upstream service already sampled |
| Lambda | exposes it in the `_X_AMZN_TRACE_ID` environment variable; traces requests already sampled upstream |
| SQS | carried in the `AWSTraceHeader` message system attribute (it overrides the HTTP header); Lambda consumers recover the context automatically, other consumers must do it themselves |
| SNS | passes the trace context from an instrumented publisher to subscribers |
| EventBridge | propagates context to targets when the sender is instrumented with the X-Ray SDK |
| Your HTTP client | only if instrumented (SDK patch / OTel) |

## Async hops you must handle yourself
- Kafka/Kinesis records, custom queues, cron jobs: put the header in a message attribute/record header and start a new segment with that parent on the consumer.
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.models.trace_header import TraceHeader
h = TraceHeader.from_header_str(msg_headers["X-Amzn-Trace-Id"])
seg = xray_recorder.begin_segment("worker", traceid=h.root, parent_id=h.parent, sampling=h.sampled)
```
- Batch consumers processing many messages: one segment per message, or links (OTel span links) to multiple parents.

## W3C interop
- OpenTelemetry uses the W3C `traceparent` header; configure the X-Ray propagator next to
  `tracecontext` in your OpenTelemetry SDK if services must accept and emit both formats.
- X-Ray accepts W3C trace ids formatted as an X-Ray id: `4efaaf4d1e8720b39541901950019ee5`
  becomes `1-4efaaf4d-1e8720b39541901950019ee5`. The time part need not be a real timestamp.
- Mixed estates: ensure the edge (ALB/API Gateway) header is honoured by OTel apps, otherwise traces split.

## Logging correlation
Log the trace id in every line so Logs Insights and X-Ray link; ALB access logs give the edge view.

## Verify
- [ ] One trace spans ALB -> service -> SQS -> Lambda without breaks in the trace map.
- [ ] Logs for a request can be found by its trace id.

## Checked

2026-10-27, AWS documentation (current release as read on that date). X-Ray Developer Guide concepts, API Gateway, Lambda, SNS, EventBridge, SQS and sending-data pages, ALB request tracing page, Lambda environment variable page, and the aws-xray-sdk-python source (TraceHeader and begin_segment). Fixed: ALB inserts a Self field only when Root is present and the header is logged with access logs, W3C ids need X-Ray formatting (1-<8>-<24>) and the time part is not required, Lineage must not be used directly. Removed the unsourced Step Functions row, the OTEL_PROPAGATORS value, the trace_id log field and the Lineage recursion-detection claim.
Method: documentation only; no commands were run.
