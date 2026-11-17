---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-lambda-proxy-vs-non-proxy-and-http-proxy
name: api-gateway-lambda-proxy-vs-non-proxy-and-http-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, lambda-proxy-integration, http-proxy, aws-proxy, non-proxy-integration, payload-format-version, malformed-lambda-proxy-response]
level: practitioner
status: docs-checked
description: "Choose and debug API Gateway integration types: Lambda proxy response contract, non-proxy mapping and error regex, HTTP proxy with greedy paths, and HTTP API payload 1.0 vs 2.0."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-integration-types.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway integration types: Lambda proxy, non-proxy and HTTP proxy

## Which one
| Type | Use when | Gateway does |
|---|---|---|
| `AWS_PROXY` (Lambda proxy) | default for Lambda backends | passes the whole request as an event; returns what Lambda returns |
| `AWS` (non-proxy) | transform requests/responses in the gateway, call AWS services directly | mapping templates both ways, error mapping |
| `HTTP_PROXY` | front an existing HTTP backend unchanged | forwards method, path, headers, body |
| `HTTP` (non-proxy) | HTTP backend with transformation | mapping templates |
| `MOCK` | stubs, CORS preflight | no backend |

## Lambda proxy contract
In the documented output format the function returns:
```json
{"statusCode": 200, "headers": {"Content-Type": "application/json"},
 "multiValueHeaders": {}, "body": "{\"ok\":true}", "isBase64Encoded": false}
```
- `headers` and `multiValueHeaders` are optional; `headers` holds single-value headers only, and keys present in both are merged.
- Output in any other format returns **502 Bad Gateway**; handle errors in the function and return 4xx/5xx yourself
  (documented examples return `{"statusCode": 400, "body": "..."}` instead of throwing).
- CORS: add `Access-Control-Allow-Origin` to the output `headers`.
- Binary: base64 the body, set `isBase64Encoded: true`, and configure the binary media types (the docs use `*/*`).

## Non-proxy Lambda
- Request mapping template shapes the event; integration responses select a status by regex on
  `errorMessage`: selection pattern `.*"NotFound".*` -> 404. The default response (blank pattern) catches the rest.
- Throwing `new Error(JSON.stringify({type:"NotFound"}))` lets the regex match.

## HTTP proxy
```
Resource: /{proxy+}  Method: ANY
Integration: HTTP_PROXY  URI: https://backend.example.com/{proxy}
Request parameter mapping: integration.request.path.proxy = method.request.path.proxy
```
- `{proxy+}` is a greedy path variable on a child resource; the root resource `/` is a separate resource and needs its own method.
- Integration timeout: 29 s (REST; Regional and private REST APIs can raise it via a quota request), 30 s maximum for HTTP APIs.

## HTTP APIs (apigatewayv2)
- Lambda payload format `2.0` or `1.0`: the console uses the latest by default, but with the CLI, CloudFormation or an SDK you must set `payloadFormatVersion` yourself.
- Format `2.0` has a `cookies` array and no `multiValueHeaders`; if the function returns valid JSON without `statusCode`,
  API Gateway infers `statusCode` 200 and wraps the value as the body.
- Format `1.0` is the REST-style proxy event; pick it when sharing code with REST APIs.

## Debug
- REST: enable execution logging (INFO) on the stage; log shows "Endpoint response body before transformations" and the malformed-response error.
- Test the method in the console or with `test-invoke-method` to see the request trace.

## Verify
- [ ] Unit test asserts the handler returns string `body` and numeric `statusCode` for success and error paths.
- [ ] `curl -i` against the stage returns expected status codes for 2xx/4xx/5xx cases.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot) plus the botocore `apigateway` model (integration types AWS, AWS_PROXY, HTTP, HTTP_PROXY, MOCK).
Confirmed: proxy output fields and the 502 rule; multi-value header merging; CORS header in output; payload format 1.0 and 2.0 defaults and inference of `statusCode`; integration types; timeouts.
Fixed: payload format 2.0 is not a universal default; `headers` is optional. Removed the unconfirmed claims about client IP and `X-Forwarded-For`, and that test invoke bypasses auth.

Method: documentation only; no commands were run.
