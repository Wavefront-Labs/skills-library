---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-logging-and-cors
name: api-gateway-logging-and-cors
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, apigw-access-logs, execution-logs, apigw-cors, cloudwatch-logs, troubleshooting, http-502]
level: practitioner
status: docs-checked
description: "Configure API Gateway access and execution logs, pick useful $context fields, debug 4xx/5xx with them, and set up CORS correctly for REST and HTTP APIs."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway logging and CORS

## 1. Account prerequisite (REST execution logs)
Execution logging needs an account-level CloudWatch role, once per region:
```bash
aws apigateway update-account --patch-operations \
  op=replace,path=/cloudwatchRoleArn,value=arn:aws:iam::<ACCOUNT_ID>:role/apigw-cloudwatch
# role trusts apigateway.amazonaws.com, policy AmazonAPIGatewayPushToCloudWatchLogs
```

## 2. Access logs (both API types) — always on
```bash
aws apigateway update-stage --rest-api-id "$API" --stage-name prod --patch-operations \
  op=replace,path=/accessLogSettings/destinationArn,value=arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:apigw-orders-prod \
  "op=replace,path=/accessLogSettings/format,value='{\"requestId\":\"\$context.requestId\",\"ip\":\"\$context.identity.sourceIp\",\"method\":\"\$context.httpMethod\",\"path\":\"\$context.resourcePath\",\"status\":\"\$context.status\",\"latency\":\"\$context.responseLatency\",\"integLatency\":\"\$context.integration.latency\",\"integStatus\":\"\$context.integration.status\",\"integErr\":\"\$context.integration.error\",\"authErr\":\"\$context.authorizer.error\",\"waf\":\"\$context.waf.status\",\"errMsg\":\"\$context.error.message\",\"errType\":\"\$context.error.responseType\"}'"
```
`$context.error.responseType` (a gateway response type such as `THROTTLED`, `UNAUTHORIZED` or `INTEGRATION_TIMEOUT`) and
`$context.integration.error` help explain failures without execution logs.

## 3. Execution logs (REST only) — targeted
`loggingLevel` `ERROR` or `INFO`, `dataTraceEnabled` logs full request/response bodies —
**turn data trace off in production** (PII, secrets in headers). Log group:
`API-Gateway-Execution-Logs_<API_ID>/<STAGE>`. Method-level overrides are method settings (the stage's `methodSettings`).

## 4. Debug table
| Symptom | Look at |
|---|---|
| 502 | `integErr` and the execution log; a Lambda proxy function must return the documented output format (`statusCode`, `body`, optional headers) |
| 504 | `integLatency` near the timeout means an integration timeout (REST default 29 s; Regional and private REST APIs can request a higher quota) |
| 403 `Missing Authentication Token` | wrong path/method or stage not deployed — not an auth issue |
| 403 with WAF | `waf` field holds the status code returned from AWS WAF |
| 429 | throttling — see usage plans |

## 5. CORS
**HTTP API:** configure once on the API (`--cors-configuration AllowOrigins=https://app.example.com,AllowMethods=GET,POST,AllowHeaders=authorization,content-type,MaxAge=600`);
API Gateway answers preflight and adds headers; it ignores CORS headers returned by your backend integration, so do not add them in Lambda.
**REST API:** enabling CORS creates an `OPTIONS` mock method for preflight, but with **proxy
integrations the actual response headers must come from your backend**:
```python
return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "https://app.example.com"}, "body": "..."}
```
Also add CORS headers to gateway responses `DEFAULT_4XX`/`DEFAULT_5XX`, or browsers report
auth/throttle errors as "CORS error".

## Gotchas
- `Access-Control-Allow-Origin: *` cannot be combined with credentials (cookies/auth headers in `fetch` with `credentials: 'include'`).
- Deploy the REST API to the stage after CORS changes.

## Verify
- [ ] An access log line exists for every test request, including 4xx, with `errType` filled on failures.
- [ ] `curl -X OPTIONS -H "Origin: https://app.example.com" -H "Access-Control-Request-Method: POST" ...` returns the allow headers.
- [ ] A forced 401 in the browser shows a 401 (not a CORS error) in dev tools.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot) plus the current botocore `apigateway` model.
Confirmed: `cloudwatchRoleArn` account field and the `AmazonAPIGatewayPushToCloudWatchLogs` policy name; execution log group name; `/accessLogSettings/destinationArn` patch path; every `$context` variable in the access log format (`responseLatency`, `integration.latency`, `integration.status`, `integration.error`, `error.message`, `error.responseType`, `waf.status`, `identity.sourceIp`); `loggingLevel` (OFF, ERROR, INFO) and `dataTraceEnabled` method settings; HTTP API CORS ignores backend CORS headers; REST CORS needs an OPTIONS method and backend headers on proxy integrations.
Removed as unconfirmed: the per-method `logging/loglevel` patch path.

Method: documentation only; no commands were run.
