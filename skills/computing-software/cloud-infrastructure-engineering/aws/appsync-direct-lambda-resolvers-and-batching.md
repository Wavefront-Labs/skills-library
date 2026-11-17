---
id: computing-software.cloud-infrastructure-engineering.aws.appsync-direct-lambda-resolvers-and-batching
name: appsync-direct-lambda-resolvers-and-batching
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, appsync, direct-lambda-resolver, batch-invoke, n-plus-one, graphql, lambda]
level: advanced
status: docs-checked
description: "Use AppSync direct Lambda resolvers without mapping templates, batch field resolution with BatchInvoke to fix N+1 queries, error handling and the event shape."
sources: ["https://docs.aws.amazon.com/appsync/latest/devguide/resolver-reference-lambda-js.html", "https://docs.aws.amazon.com/appsync/latest/devguide/resolver-mapping-template-reference-lambda.html", "https://docs.aws.amazon.com/appsync/latest/devguide/tutorial-lambda-resolvers.html", "https://docs.aws.amazon.com/general/latest/gr/appsync.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppSync direct Lambda resolvers and batching

## 1. Direct Lambda resolvers
A unit resolver attached to a Lambda data source **without** request/response mapping templates
sends AppSync's Context object to the function as an `Invoke` operation and returns its result
directly. Event shape (the context object; see the resolver context reference):
```json
{"arguments": {"id": "42"}, "identity": {...}, "source": {...parent object...},
 "request": {"headers": {...}}, "info": {"fieldName": "order", "parentTypeName": "Query",
 "selectionSetList": ["id", "total", "items"], "variables": {}}, "prev": null, "stash": {}}
```
Use it to keep logic in one language and avoid template code. Return the object for the
field; throw an error to produce a GraphQL error. The error `errorType` and message are the
name and message of the exception you throw (a custom `UnauthorizedException` type always returns
the default message). AWS now primarily supports and documents the `APPSYNC_JS` runtime over VTL.

## 2. The N+1 problem
`query { orders { id customer { name } } }` with a Lambda resolver on `Order.customer`
invokes Lambda once per order. 100 orders = 100 invocations (latency, cost, concurrency).

## 3. BatchInvoke
Enable batching on the resolver (`maxBatchSize`, up to 2,000 per request; 0 turns batching off).
AppSync groups field resolutions within one request and invokes Lambda with an **array** of contexts:
```bash
aws appsync create-resolver --api-id <api> --type-name Order --field-name customer \
  --data-source-name CustomersLambda --max-batch-size 100
```
With JS resolvers (or any request template), the request function must return
`operation: 'BatchInvoke'`; with direct Lambda resolvers, setting `maxBatchSize` is enough.
Batching does not apply to top-level mutations, which GraphQL requires to run sequentially; use a
single mutation field that takes a list instead.
Function must return an array **in the same order and length**:
```python
def handler(events, _ctx):
    ids = [e["source"]["customerId"] for e in events]
    found = {c["id"]: c for c in batch_get_customers(set(ids))}
    return [found.get(i) for i in ids]          # same order; None for missing
```
Per-item errors: return `{"data": ..., "errorMessage": "...", "errorType": "..."}` objects
(with the error-handling format) instead of throwing, so one bad item does not fail the
batch.

## 4. When to use something else
- Simple DynamoDB reads: JS resolvers with the DynamoDB data source (`BatchGetItem` in a
  resolver) avoid Lambda entirely.
- Pipeline resolvers chain functions (auth check, fetch, transform) and pass data via
  `ctx.stash`/`ctx.prev`.
- Caching: per-resolver caching keyed on arguments/source cuts repeated calls.

## Gotchas
- Batch size too large increases payload size (Lambda 6 MB sync payload limit) and latency
  for the whole batch.
- Lambda timeout should be well below AppSync's 30-second maximum request execution time.
- `identity` contents differ by auth mode (Cognito claims, IAM ARN, API key null, Lambda
  authorizer `resolverContext`); write the function to handle the modes your API enables.

## Verify
- [ ] A list query resolving N child fields triggers about N/maxBatchSize Lambda invocations (CloudWatch `Invocations`).
- [ ] Results map to the right parents in order; missing items return null with no batch failure.
- [ ] Resolver latency p99 acceptable in AppSync metrics/X-Ray.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS AppSync Developer Guide Lambda resolver reference (JavaScript and VTL, direct Lambda section), Lambda resolver tutorial (batching), resolver context reference, and the AWS General Reference AppSync quotas page. Confirmed: BatchInvoke operation, direct Lambda resolvers send the Context object, maxBatchSize up to 2,000 (quota "Max Batch Size per request") with 0 disabling batching, per-item data/errorMessage/errorType batch response, 30-second request execution time, create-resolver --max-batch-size, identity resolverContext for Lambda authorizers. Added: top-level mutations are not batched, error type/message behaviour. Removed the cheaper-and-faster claim for DynamoDB JS resolvers.
Method: documentation only; no commands were run.
