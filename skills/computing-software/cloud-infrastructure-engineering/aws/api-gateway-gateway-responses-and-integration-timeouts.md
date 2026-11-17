---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-gateway-responses-and-integration-timeouts
name: api-gateway-gateway-responses-and-integration-timeouts
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, gateway-responses, integration-timeout, http-502, http-504, cors-errors]
level: practitioner
status: docs-checked
description: "Diagnose API Gateway 4xx/5xx: gateway response types, 502 malformed proxy responses, 504 integration timeouts (29 s default and raising it), and CORS headers on errors."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-gatewayResponse-definition.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/supported-gateway-response-types.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html", "https://aws.amazon.com/about-aws/whats-new/2024/06/amazon-api-gateway-integration-timeout-limit-29-seconds/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway gateway responses and integration timeouts

## 1. Who produced the error?
- API Gateway-generated errors can carry an `x-amzn-ErrorType` header (for example `MissingAuthenticationTokenException`);
  a response without one came from the integration.
- Execution logs (REST, stage setting) and access logs with
  `$context.error.responseType`, `$context.integration.status`,
  `$context.integration.latency`, `$context.integrationErrorMessage` tell whether the
  backend answered.
- CloudWatch REST metrics include `4XXError`, `5XXError`, `IntegrationLatency` and `Latency`.

## 2. Gateway response types (REST)
API Gateway returns its own responses for failures before or around the integration:
`ACCESS_DENIED` (403, authorizer deny), `UNAUTHORIZED` (401), `MISSING_AUTHENTICATION_TOKEN`
(403, also returned for an unsupported resource or method, so often a **wrong path or method**), `THROTTLED` (429),
`QUOTA_EXCEEDED` (429, usage plan), `BAD_REQUEST_BODY`/`BAD_REQUEST_PARAMETERS` (400, request validators),
`INTEGRATION_FAILURE` (504), `INTEGRATION_TIMEOUT` (504), `REQUEST_TOO_LARGE` (413), `WAF_FILTERED` (403),
`AUTHORIZER_CONFIGURATION_ERROR`/`AUTHORIZER_FAILURE`/`API_CONFIGURATION_ERROR` (500), `DEFAULT_4XX`, `DEFAULT_5XX`.
Customise them, especially to add CORS headers so browsers can read error bodies:
```bash
aws apigateway put-gateway-response --rest-api-id a1b2c3 --response-type DEFAULT_4XX \
  --response-parameters '{"gatewayresponse.header.Access-Control-Allow-Origin":"'"'"'https://app.example.com'"'"'"}' \
  --response-templates '{"application/json":"{\"message\":$context.error.messageString,\"requestId\":\"$context.requestId\"}"}'
aws apigateway create-deployment --rest-api-id a1b2c3 --stage-name prod
```
Without this, a 401/403 from an authorizer shows in the browser as a CORS error.

## 3. 502 Bad Gateway
- Lambda proxy integration returned output not in the documented format: `statusCode`, optional `headers` and
  `multiValueHeaders`, `body` (a string in the documented format; serialise JSON yourself), optional `isBase64Encoded`.
  Any other output format gives 502.
- Lambda function error/unhandled exception with proxy integration.
- HTTP integration: backend TLS certificate not trusted (REST requires a publicly trusted
  cert for HTTPS backends unless `insecureSkipVerification` in `tlsConfig`), or backend
  closed the connection.
- `$context.integrationErrorMessage` (also usable in HTTP API access logs) carries the integration error message.

## 4. 504 Integration timeout
- REST integration timeout is 50 ms to 29 s by default; HTTP APIs allow at most 30 s. Since June 2024 Regional and
  private REST APIs can raise it above 29 s via a quota increase, which may reduce the account-level throttle quota.
- Fix properly: make long work asynchronous (return 202 with a job ID, process via
  SQS/Step Functions, poll or use WebSocket/callback).
- Lambda behind it should have a timeout slightly below the integration timeout so it fails
  cleanly with a useful error.

## 5. Other frequent ones
- 403 `Missing Authentication Token` on a valid-looking URL: stage name missing in the URL, or the resource/method
  does not exist or was not deployed (forgot `create-deployment`).
- 429: account-level throttle (10,000 RPS default with a 5,000 request bucket per Region; lower in some newer Regions), stage/
  method throttles or usage plan limits.
- 413: `REQUEST_TOO_LARGE`; the payload quota is 10 MB.

## Verify
- [ ] Access logs include error response type and integration status for every request.
- [ ] Browser shows readable JSON for 401/403/429 (CORS headers on DEFAULT_4XX/5XX).
- [ ] No 504s at p99; long operations moved to async pattern.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot), the current quotas page and the June 2024 What's New post.
Confirmed: gateway response types and default status codes (the botocore enum matches); `$context.error.*`, `$context.integration.*` and `$context.integrationErrorMessage` variables; proxy output format and 502 on other formats; `insecureSkipVerification` is REST-only; 10,000 RPS and 5,000 bucket; 10 MB payload; 29 s REST and 30 s HTTP API timeouts; June 2024 timeout increase for Regional and private REST APIs.
Fixed: `INTEGRATION_FAILURE` is 504 (not 504/500); `headers` is optional in the proxy output. Removed the unconfirmed claims about specific `x-amzn-ErrorType` values and trailing-slash mismatches.

Method: documentation only; no commands were run.
