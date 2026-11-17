---
id: computing-software.cloud-infrastructure-engineering.observability.otel-id-generators-and-aws-xray-ids
name: otel-id-generators-and-aws-xray-ids
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, id-generator, xray-id-generator, aws-x-ray, trace-ids, otel-traces]
level: advanced
status: docs-checked
description: "Configure OpenTelemetry ID generators, including the AWS X-Ray compatible generator with timestamped trace IDs, and know when trace ID format matters for backends."
sources: ["https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators", "https://aws-otel.github.io/docs/getting-started/x-ray", "https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid", "https://www.w3.org/TR/trace-context/#trace-id"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTelemetry ID generators

**Goal:** trace and span IDs that every backend in your path accepts.

## Defaults
- W3C trace ID: 16 random bytes (32 hex chars); span ID: 8 bytes. The SDK's default **random ID generator** is right for almost every backend (Jaeger, Tempo, Zipkin, vendors).
- W3C Trace Context Level 2 defines a random trace-id flag (bit `00000010` of trace-flags) saying that at least the right-most 7 bytes of the trace ID are random; OTel consistent probability sampling uses those 56 bits of randomness (or an explicit `rv`).

## AWS X-Ray
X-Ray trace IDs have the form `1-<8 hex digits of epoch seconds>-<24 hex digits>` (`1-58406520-a006649127e371903a2de979`). The X-Ray segment document page says X-Ray now supports W3C trace IDs from OpenTelemetry: a W3C ID must be formatted in X-Ray form (`4efaaf4d1e8720b39541901950019ee5` becomes `1-4efaaf4d-1e8720b39541901950019ee5`), and the timestamp is not required when sending W3C IDs this way. The X-Ray ID generators below make the first four bytes the start time, so the ID is a native X-Ray ID. Use one when your path requires timestamp-based IDs:

Java: with the upstream SDK add `io.opentelemetry.contrib:opentelemetry-aws-xray` (it provides `AwsXrayIdGenerator`) and:
```java
SdkTracerProvider.builder().setIdGenerator(AwsXrayIdGenerator.getInstance())...
```
Python:
```python
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
trace.set_tracer_provider(TracerProvider(id_generator=AwsXRayIdGenerator()))
```
Node.js: `new NodeTracerProvider({ idGenerator: new AWSXRayIdGenerator() })` from `@opentelemetry/id-generator-aws-xray`.
Go: `sdktrace.WithIDGenerator(xray.NewIDGenerator())` from `go.opentelemetry.io/contrib/propagators/aws/xray`.
Propagators for the `X-Amzn-Trace-Id` header exist as `@opentelemetry/propagator-aws-xray` (Node) and in the Go contrib module above; add one next to W3C if AWS services in the path propagate X-Ray headers.

## Gotchas
- Custom ID generators must stay unique, and X-Ray advises generating trace IDs with a secure random algorithm so attackers cannot predict future IDs (trace IDs are visible in response headers).
- Check the X-Ray documentation for your ingestion path before dropping the generator.

## Verify
- [ ] If you use an X-Ray ID generator, the first 8 hex digits of the trace ID decode to the request time in epoch seconds; traces appear in the X-Ray service map.

## Checked

2026-10-24. AWS X-Ray developer guide (segment documents page, fetched 2026-10-24), W3C Trace Context spec, and the contrib repositories: opentelemetry-java-contrib aws-xray (AwsXrayIdGenerator), opentelemetry-python-contrib sdk-extension-aws (AwsXRayIdGenerator), opentelemetry-js-contrib id-generator-aws-xray (AWSXRayIdGenerator), opentelemetry-go-contrib propagators/aws/xray (`NewIDGenerator`). Confirmed: X-Ray trace ID format and the W3C-to-X-Ray ID formatting note, the random flag, and the four generator class and package names. Removed the unconfirmed claim that X-Ray rejects IDs older than 30 days and the ADOT agent auto-configuration claim; updated the stale statement that random IDs break X-Ray.

Method: documentation only; no commands were run.
