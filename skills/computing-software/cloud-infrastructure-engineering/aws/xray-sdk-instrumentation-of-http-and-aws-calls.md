---
id: computing-software.cloud-infrastructure-engineering.aws.xray-sdk-instrumentation-of-http-and-aws-calls
name: xray-sdk-instrumentation-of-http-and-aws-calls
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, x-ray, xray-sdk, sdk-instrumentation, subsegments, annotations, patch-all, opentelemetry-migration]
level: practitioner
status: docs-checked
description: "Instrument apps with X-Ray SDKs: patching AWS SDK and HTTP clients, framework middleware, custom subsegments, annotations vs metadata, and the move to OpenTelemetry."
sources: ["https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-patching.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-nodejs-awssdkclients.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-java-awssdkclients.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-daemon-timeline.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X-Ray SDK instrumentation of HTTP and AWS SDK calls

## Python
```python
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
patch_all()                       # botocore/boto3, requests, aiohttp, httplib, sqlite3, psycopg2, pymysql, pymongo, ...
xray_recorder.configure(service="orders-api", sampling=True)
XRayMiddleware(app, xray_recorder)   # creates a segment per incoming request

@xray_recorder.capture("price_order")   # custom subsegment
def price(order):
    xray_recorder.current_subsegment().put_annotation("customer_tier", order.tier)
    xray_recorder.current_subsegment().put_metadata("order", order.to_dict())
```
In Lambda with active tracing, the function segment exists already; just `patch_all()` and add
subsegments. A patched library only creates a subsegment when a segment is available, from the
middleware or from Lambda. Some libraries (such as `httplib` and `urllib`) may need
`patch_all(double_patch=True)`.

## Node.js
```js
const AWSXRay = require('aws-xray-sdk-core');
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const ddb = AWSXRay.captureAWSv3Client(new DynamoDBClient({}));   // v3 has no captureAWS; wrap each client
AWSXRay.captureHTTPsGlobal(require('https'));
// Express: app.use(AWSXRay.express.openSegment('orders-api')) ... app.use(AWSXRay.express.closeSegment())
```
Instrumenting AWS SDK for JavaScript v3 clients records less than v2 clients (for example no
DynamoDB table name in the subsegment); use v2 with `captureAWS` if you need that detail.

## Java
`AWSXRayServletFilter` for incoming requests; the `aws-sdk-instrumentor` submodule (or a
`TracingHandler` request handler) for AWS SDK for Java clients;
`aws-xray-recorder-sdk-apache-http` for outgoing Apache HTTP calls.

## Annotations vs metadata
| | Annotations | Metadata |
|---|---|---|
| Indexed for filter expressions | yes (`annotation.customer_tier = "gold"`) | no |
| Types | string, number, boolean | any JSON |
| Limit | 50 per trace | larger objects |
Use annotations for things you will search by (tenant, order type, feature flag), metadata for debugging payloads.

## Outside Lambda
Run the X-Ray daemon (listens on UDP port 2000) or a collector that accepts X-Ray segments; set
`AWS_XRAY_DAEMON_ADDRESS` (host and port). Lambda runs the daemon for sampled requests, and
Elastic Beanstalk runs it with the `XRayEnabled` option.
`AWS_XRAY_CONTEXT_MISSING=LOG_ERROR` avoids exceptions when code runs outside a segment (background jobs).
The CloudWatch agent (version 1.300025.0 or later) can collect traces from OpenTelemetry or X-Ray
SDKs instead of the daemon.

## Plan for OpenTelemetry
The X-Ray SDKs and daemon entered **maintenance mode on 25 February 2026**: security fixes only,
no new features. AWS recommends migrating to OpenTelemetry for new instrumentation. The support
timeline page lists no end-of-support date; re-read it before planning.

## Verify
- [ ] Trace for one request shows the service segment, AWS SDK subsegments (table, bucket or queue names where the SDK adds them) and HTTP calls.
- [ ] Filter expression on an annotation returns the expected traces.

## Checked

2026-10-27, AWS documentation (current release as read on that date). X-Ray Developer Guide SDK pages for Python (patching, middleware, configuration), Node.js (AWS SDK clients, HTTP clients, middleware) and Java (AWS SDK clients, servlet filter, HTTP clients), the daemon page and the SDK and Daemon support timeline, plus the aws-xray-sdk-python source. Fixed: the SDKs and daemon entered maintenance mode on 2026-02-25 (security fixes only) and the timeline lists no end-of-support date; Node.js SDK v3 clients return less detail (no DynamoDB table name); the Express middleware is AWSXRay.express.openSegment. Confirmed: patch_all library list, double_patch, captureAWSv3Client, captureHTTPsGlobal, AWSXRayServletFilter, aws-xray-recorder-sdk-apache-http, UDP 2000, AWS_XRAY_DAEMON_ADDRESS and AWS_XRAY_CONTEXT_MISSING, 50 indexed annotations. Removed the unsourced Java SDK v2 TracingInterceptor and Spring XRayEnabled remarks.
Method: documentation only; no commands were run.
