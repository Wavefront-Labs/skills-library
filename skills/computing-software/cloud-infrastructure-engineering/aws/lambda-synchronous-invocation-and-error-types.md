---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-synchronous-invocation-and-error-types
name: lambda-synchronous-invocation-and-error-types
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, synchronous-invocation, function-error, invoke, error-handling]
level: practitioner
status: docs-checked
description: "Invoke Lambda synchronously and tell invocation errors from function errors (HTTP 200 with a function error), with who retries and which limits surface as errors."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/invocation-sync.html", "https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html", "https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synchronous invocation and error types

## 1. Invoke
```bash
aws lambda invoke --function-name orders --cli-binary-format raw-in-base64-out \
  --payload '{"id":42}' --log-type Tail out.json
cat out.json
```
`--cli-binary-format raw-in-base64-out` is required with AWS CLI v2 (or set it once with
`aws configure set cli-binary-format raw-in-base64-out`). The CLI prints `StatusCode` and `ExecutedVersion`
(useful with aliases). `--log-type Tail` adds `LogResult`: up to 4 KB of base64-encoded logs
(`--query LogResult --output text | base64 --decode`).
Asynchronous invocation is the same call with `--invocation-type Event` and returns `StatusCode` 202 once
Lambda has queued the event.

## 2. Two kinds of error
| Kind | Looks like | Notes |
|---|---|---|
| Invocation error | Lambda could not run the function; the error is printed by the CLI/SDK (for example `InvalidRequestContentException` for a payload that is not JSON) | fix the request or retry throttles and service errors |
| Function error | the function ran; the status code is **200** even though the function returned an error, and the response body is the error object as JSON | decide per operation whether a retry is safe |
If Lambda ran the function the status code is 200 even if the function returned an error, so checking only the
HTTP status misses function errors; inspect the response body.
A function that exits cleanly returns `null` as the body unless it returns an object.

## 3. Retry ownership
When you invoke directly you check the response and retry yourself. The AWS CLI and SDKs automatically retry on
client timeouts, throttling and service errors. Event source mappings and async invocations have their own
retry behaviour (see the retries page and the mapping skills).

## 4. Limits that surface as errors
- Payload 6 MB for request and response (synchronous), 1 MB asynchronous.
- Function timeout up to 900 seconds (15 minutes); long synchronous calls need client, proxy and firewall
  timeouts long enough to hold the connection.
- A concurrency limit causes 429 throttling; reserved concurrency 0 stops the function processing events.
- External extensions can keep running after the response is returned; Lambda does not wait for them.

## Verify
- [ ] Client code checks both the invoke call result and the function error in the response.
- [ ] Alarms on function errors and on throttles both exist.

## Checked
Date 2026-10-23. Lambda Developer Guide synchronous and asynchronous invocation pages and the quotas page. Confirmed: CLI v2
`--cli-binary-format` requirement, status 200 with function errors, `LogResult` 4 KB base64, `null` body on clean
exit, `ExecutedVersion`, async `Event` type returning 202, SDK automatic retries, 6 MB and 1 MB payloads, 900 s
timeout, extensions not awaited. Removed the unconfirmed exception-name table
(`RequestEntityTooLargeException`, `KMSAccessDeniedException`), the API Gateway 29 s remark and the claim that
Lambda never retries synchronous invokes.
Method: documentation only; no commands were run.
